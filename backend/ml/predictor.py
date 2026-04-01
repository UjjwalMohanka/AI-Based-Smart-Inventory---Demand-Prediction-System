import numpy as np
from .data_prep import prepare_sales_data, create_future_features, get_feature_columns
from .trainer import train_demand_model

def predict_demand(sales_records, months_ahead=3):
    """
    Predict demand for the next N months
    
    Args:
        sales_records: List of Sales model objects (historical data)
        months_ahead: Number of months to predict (default 3)
        
    Returns:
        dict with:
            - predictions: List of dicts [{month, year, predicted_qty}, ...]
            - accuracy: R² score from training
            - mae: Mean Absolute Error
            - model_type: 'linear_regression' or 'average_fallback'
    """
    
    # Train or retrain model
    model_info = train_demand_model(sales_records)
    
    # If using average fallback
    if model_info['use_average']:
        predictions = []
        
        # Get last sale date or use current date
        if sales_records:
            last_sale = max(sales_records, key=lambda s: (s.year, s.month))
            current_month = last_sale.month
            current_year = last_sale.year
        else:
            from datetime import datetime
            now = datetime.now()
            current_month = now.month
            current_year = now.year
        
        # Generate predictions using average
        for i in range(1, months_ahead + 1):
            future_month = (current_month + i - 1) % 12 + 1
            future_year = current_year + (current_month + i - 1) // 12
            
            predictions.append({
                'month': future_month,
                'year': future_year,
                'predicted_qty': max(0, round(model_info['average_value']))
            })
        
        return {
            'predictions': predictions,
            'accuracy': 0.0,
            'mae': 0.0,
            'model_type': 'average_fallback'
        }
    
    # Use ML model for prediction
    df = prepare_sales_data(sales_records)
    
    if df is None or len(df) == 0:
        return {
            'predictions': [],
            'accuracy': 0.0,
            'mae': 0.0,
            'model_type': 'no_data'
        }
    
    # Get last data point info for creating future features
    last_row = df.iloc[-1]
    last_date_info = {
        'year': int(last_row['year']),
        'month': int(last_row['month']),
        'month_index': int(last_row['month_index']),
        'rolling_avg_3': float(last_row['rolling_avg_3']),
        'lag_1': float(last_row['lag_1']),
        'lag_2': float(last_row['lag_2'])
    }
    
    # Create future features
    future_df = create_future_features(last_date_info, months_ahead)
    
    # Make predictions
    feature_cols = model_info['feature_cols']
    X_future = future_df[feature_cols].values
    
    predictions_raw = model_info['model'].predict(X_future)
    
    # Format predictions
    predictions = []
    for idx, pred_qty in enumerate(predictions_raw):
        predictions.append({
            'month': int(future_df.iloc[idx]['month']),
            'year': int(future_df.iloc[idx]['year']),
            'predicted_qty': max(0, round(pred_qty))  # Ensure non-negative
        })
    
    return {
        'predictions': predictions,
        'accuracy': model_info['accuracy'],
        'mae': model_info['mae'],
        'model_type': 'linear_regression'
    }


def calculate_restock_suggestion(predictions, current_stock, reorder_point, lead_time_days):
    """
    Calculate if restocking is needed and suggest order quantity
    
    Args:
        predictions: List of prediction dicts
        current_stock: Current inventory quantity
        reorder_point: Minimum stock level before reorder
        lead_time_days: Days to receive new stock
        
    Returns:
        dict with restocking recommendations
    """
    if not predictions:
        return {
            'restock_needed': False,
            'suggested_order_qty': 0,
            'reason': 'No predictions available'
        }
    
    # Calculate total predicted demand
    total_predicted_demand = sum(p['predicted_qty'] for p in predictions)
    
    # Check if current stock is below reorder point
    below_reorder = current_stock < reorder_point
    
    # Check if predicted demand exceeds current stock
    demand_exceeds_stock = total_predicted_demand > current_stock
    
    if below_reorder or demand_exceeds_stock:
        # Calculate suggested order quantity
        # Order enough to cover predicted demand + safety buffer (reorder point)
        needed_qty = max(0, total_predicted_demand - current_stock + reorder_point)
        
        return {
            'restock_needed': True,
            'suggested_order_qty': int(np.ceil(needed_qty)),
            'reason': 'Current stock insufficient for predicted demand' if demand_exceeds_stock else 'Stock below reorder point',
            'total_predicted_demand': int(total_predicted_demand),
            'current_stock': current_stock,
            'reorder_point': reorder_point
        }
    else:
        return {
            'restock_needed': False,
            'suggested_order_qty': 0,
            'reason': 'Current stock sufficient',
            'total_predicted_demand': int(total_predicted_demand),
            'current_stock': current_stock,
            'reorder_point': reorder_point
        }
