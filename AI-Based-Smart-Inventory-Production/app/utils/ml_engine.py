import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, date

def train_and_predict(historical_sales, months_to_predict=3):
    """
    Train a simple Linear Regression model and predict future demand.
    
    Args:
        historical_sales (list): List of Sales model objects
        months_to_predict (int): Number of future months to forecast
        
    Returns:
        dict: Predictions and model accuracy
    """
    if len(historical_sales) < 6:
        # Fallback to simple average if not enough data
        avg_sales = np.mean([s.quantity_sold for s in historical_sales]) if historical_sales else 0
        predictions = []
        last_date = historical_sales[-1].sale_date if historical_sales else date.today()
        
        for i in range(1, months_to_predict + 1):
            future_month = (last_date.month + i - 1) % 12 + 1
            future_year = last_date.year + (last_date.month + i - 1) // 12
            predictions.append({
                'month': future_month,
                'year': future_year,
                'qty': round(avg_sales, 2)
            })
        return {'predictions': predictions, 'accuracy': 0.0, 'method': 'Average Fallback'}

    # Prepare DataFrame
    data = []
    for s in historical_sales:
        data.append({
            'month': s.month,
            'year': s.year,
            'qty': s.quantity_sold,
            'time_index': (s.year - historical_sales[0].year) * 12 + s.month
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('time_index')

    # Features: time_index, month (categorical-like)
    X = df[['time_index', 'month']].values
    y = df['qty'].values

    # Train Model
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate R-squared for confidence
    r2_score = model.score(X, y)

    # Predict Future
    last_time_index = df['time_index'].max()
    last_month = df['month'].iloc[-1]
    last_year = df['year'].iloc[-1]
    
    predictions = []
    for i in range(1, months_to_predict + 1):
        future_time_index = last_time_index + i
        future_month = (last_month + i - 1) % 12 + 1
        future_year = last_year + (last_month + i - 1) // 12
        
        pred_qty = model.predict([[future_time_index, future_month]])[0]
        predictions.append({
            'month': int(future_month),
            'year': int(future_year),
            'qty': float(max(0, round(pred_qty, 2)))
        })

    return {
        'predictions': predictions,
        'accuracy': float(round(r2_score, 3)),
        'method': 'Linear Regression'
    }
