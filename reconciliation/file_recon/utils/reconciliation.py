import pandas as pd
import numpy as np
from datetime import datetime

def reconcile_files(source_df, target_df, key_columns):
    """Compare source and target dataframes and return reconciliation results"""
    try:
        # Initialize results
        results = {
            'missing_in_target': [],
            'missing_in_source': [],
            'discrepancies': [],
            'stats': {}
        }
        
        # Normalize both dataframes
        source_df = normalize_data(source_df)
        target_df = normalize_data(target_df)
        
        # Set index for comparison
        source_df.set_index(key_columns, inplace=True)
        target_df.set_index(key_columns, inplace=True)
        
        # Find missing records
        results['missing_in_target'] = source_df[~source_df.index.isin(target_df.index)]\
            .reset_index().to_dict('records')
        results['missing_in_source'] = target_df[~target_df.index.isin(source_df.index)]\
            .reset_index().to_dict('records')
        
        # Find common records
        common_keys = source_df.index.intersection(target_df.index)
        
        # Find discrepancies
        for key in common_keys:
            differences = []
            source_row = source_df.loc[key]
            target_row = target_df.loc[key]
            
            for col in source_df.columns:
                if col in target_df.columns:
                    # Convert to string for safe comparison
                    source_val = str(source_row[col])
                    target_val = str(target_row[col])
                    
                    if source_val != target_val:
                        differences.append({
                            'field': col,
                            'source_value': source_val,
                            'target_value': target_val
                        })
            
            if differences:
                results['discrepancies'].append({
                    'key': str(key),  # Ensure key is string
                    'differences': differences
                })
        
        # Calculate statistics
        results['stats'] = {
            'source_count': len(source_df),
            'target_count': len(target_df),
            'missing_in_target_count': len(results['missing_in_target']),
            'missing_in_source_count': len(results['missing_in_source']),
            'discrepancy_count': len(results['discrepancies']),
            'matching_count': len(common_keys) - len(results['discrepancies'])
        }
        
        return results
        
    except Exception as e:
        return {
            'error': str(e),
            'status': 'FAILED'
        }

def normalize_data(df):
    """Normalize dataframe by standardizing formats"""
    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()
    
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
                    # Convert datetime to string for consistency
                    df[col] = df[col].dt.strftime('%Y-%m-%d')
                    break
                except:
                    continue
    
    return df