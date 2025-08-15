import pandas as pd
from datetime import datetime

def normalize_data(df):
    """Normalize dataframe by standardizing formats"""
    # Convert all string columns to lowercase and strip whitespace
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip().str.lower()
    
    # Attempt to parse dates in common formats
    date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y%m%d']
    for col in df.columns:
        if 'date' in col.lower():
            for fmt in date_formats:
                try:
                    df[col] = pd.to_datetime(df[col], format=fmt)
                    break
                except:
                    continue
    
    return df