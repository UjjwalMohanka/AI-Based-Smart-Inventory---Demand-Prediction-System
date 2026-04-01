import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from .data_prep import prepare_sales_data, get_feature_columns

def train_demand_model(sales_records):
    """
    Train Linear Regression model on sales data
    
    Args:
        sales_records: List of Sales model objects
        
    Returns:
        dict with:
            - model: Trained sklearn model (or None if insufficient data)
            - accuracy: R² score
            - mae: Mean Absolute Error
            - feature_cols: List of feature column names
            - use_average: Boolean, True if using simple average fallback
            - average_value: Average sales (if use_average is True)
    """
    
    # Prepare data
    df = prepare_sales_data(sales_records)
    
    if df is None or len(df) < 3:
        # Insufficient data - use simple average
        if sales_records:
            avg_qty = np.mean([s.quantity_sold for s in sales_records])
        else:
            avg_qty = 0
        
        return {
            'model': None,
            'accuracy': 0.0,
            'mae': 0.0,
            'feature_cols': get_feature_columns(),
            'use_average': True,
            'average_value': avg_qty
        }
    
    # Prepare features and target
    feature_cols = get_feature_columns()
    X = df[feature_cols].values
    y = df['quantity_sold'].values
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate accuracy metrics
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    
    # Ensure R² is not negative (can happen with very poor fits)
    r2 = max(0.0, r2)
    
    return {
        'model': model,
        'accuracy': r2,
        'mae': mae,
        'feature_cols': feature_cols,
        'use_average': False,
        'average_value': None
    }


def retrain_if_needed(sales_records, existing_model=None):
    """
    Retrain model if needed (currently always retrains for simplicity)
    
    Args:
        sales_records: Latest sales data
        existing_model: Previously trained model (not used currently)
        
    Returns:
        New trained model dict
    """
    return train_demand_model(sales_records)
