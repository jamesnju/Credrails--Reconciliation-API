# file_recon/utils/reconciliation.py
import pandas as pd
from .normalization import normalize_data

def reconcile_files(source_df, target_df, key_columns):
    """
    Compare source and target dataframes and return reconciliation results
    """
    # Normalize both dataframes
    source_df = normalize_data(source_df)
    target_df = normalize_data(target_df)
    
    # Set index for comparison
    source_df.set_index(key_columns, inplace=True)
    target_df.set_index(key_columns, inplace=True)
    
    # Find missing records
    missing_in_target = source_df[~source_df.index.isin(target_df.index)]
    missing_in_source = target_df[~target_df.index.isin(source_df.index)]
    
    # Find common records
    common_keys = source_df.index.intersection(target_df.index)
    common_source = source_df.loc[common_keys]
    common_target = target_df.loc[common_keys]
    
    # Find discrepancies
    discrepancies = []
    for key in common_keys:
        source_row = common_source.loc[key]
        target_row = common_target.loc[key]
        
        diff_fields = []
        for col in source_df.columns:
            if col in target_df.columns:
                if source_row[col] != target_row[col]:
                    diff_fields.append({
                        'field': col,
                        'source_value': source_row[col],
                        'target_value': target_row[col]
                    })
        
        if diff_fields:
            discrepancies.append({
                'key': key,
                'differences': diff_fields
            })
    
    return {
        'missing_in_target': missing_in_target.reset_index().to_dict('records'),
        'missing_in_source': missing_in_source.reset_index().to_dict('records'),
        'discrepancies': discrepancies,
        'stats': {
            'source_count': len(source_df),
            'target_count': len(target_df),
            'missing_in_target_count': len(missing_in_target),
            'missing_in_source_count': len(missing_in_source),
            'discrepancy_count': len(discrepancies),
            'matching_count': len(common_keys) - len(discrepancies)
        }
    }