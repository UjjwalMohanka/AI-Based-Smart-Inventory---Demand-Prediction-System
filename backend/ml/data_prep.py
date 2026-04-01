import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def prepare_sales_data(sales_records):
    """
    Convert sales records to time-series DataFrame with features
    
    Args:
        sales_records: List of Sales model objects
        
    Returns:
        DataFrame with features for ML training
    """
    if not sales_records or len(sales_records) == 0:
        return None
    
    # Convert to DataFrame
    data = []
    for sale in sales_records:
        data.append({
            'year': sale.year,
            'month': sale.month,
            'quantity_sold': sale.quantity_sold,
            'sale_date': sale.sale_date
        })
    
    df = pd.DataFrame(data)
    
    # Sort by date
    df = df.sort_values(['year', 'month'])
    
    # Create time index (months since start)
    df['month_index'] = (df['year'] - df['year'].min()) * 12 + df['month'] - 1
    
    # Aggregate by month (sum quantities sold in same month)
    df_agg = df.groupby(['year', 'month', 'month_index'], as_index=False).agg({
        'quantity_sold': 'sum'
    })
    
    # Create features
    df_agg['month_num'] = df_agg['month']  # 1-12 for seasonality
    
    # Rolling averages (if enough data)
    if len(df_agg) >= 3:
        df_agg['rolling_avg_3'] = df_agg['quantity_sold'].rolling(window=3, min_periods=1).mean()
    else:
        df_agg['rolling_avg_3'] = df_agg['quantity_sold']
    
    # Lag features
    df_agg['lag_1'] = df_agg['quantity_sold'].shift(1).fillna(df_agg['quantity_sold'].mean())
    df_agg['lag_2'] = df_agg['quantity_sold'].shift(2).fillna(df_agg['quantity_sold'].mean())
    
    # Trend feature (normalized time index)
    df_agg['trend'] = df_agg['month_index'] / df_agg['month_index'].max() if df_agg['month_index'].max() > 0 else 0
    
    return df_agg


def create_future_features(last_date_info, months_ahead):
    """
    Create feature DataFrame for future predictions
    
    Args:
        last_date_info: dict with 'year', 'month', 'month_index', 'rolling_avg_3', 'lag_1', 'lag_2'
        months_ahead: Number of months to predict
        
    Returns:
        DataFrame with features for prediction
    """
    future_data = []
    
    for i in range(1, months_ahead + 1):
        # Calculate future month and year
        future_month = (last_date_info['month'] + i - 1) % 12 + 1
        future_year = last_date_info['year'] + (last_date_info['month'] + i - 1) // 12
        
        future_row = {
            'year': future_year,
            'month': future_month,
            'month_index': last_date_info['month_index'] + i,
            'month_num': future_month,
            'rolling_avg_3': last_date_info['rolling_avg_3'],
            'lag_1': last_date_info['lag_1'],
            'lag_2': last_date_info['lag_2'],
            'trend': (last_date_info['month_index'] + i) / last_date_info['month_index'] if last_date_info['month_index'] > 0 else i
        }
        
        future_data.append(future_row)
    
    return pd.DataFrame(future_data)


def get_feature_columns():
    """Return list of feature column names used for training"""
    return ['month_index', 'month_num', 'rolling_avg_3', 'lag_1', 'lag_2', 'trend']
