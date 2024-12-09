import requests
import pandas as pd
from app.utils.auth import get_auth_header


def merge_and_filter(csv_data, vehicles_data):
    """
    Merge CSV and JSON data keeping all columns from both datasets.
    
    Args:
        csv_data (pd.DataFrame): CSV source data
        vehicles_data (pd.DataFrame): Vehicle data from API
    Returns:
        list: List of dictionaries containing all merged data
    """
    # Convert vehicles_data to DataFrame if it's not already
    vehicles_df = vehicles_data.copy()
    
    # Create copies to avoid modifying original DataFrames
    csv_data_copy = csv_data.copy()
    
    # Merge DataFrames on 'kurzname'
    merged_df = pd.merge(
        csv_data_copy,
        vehicles_df,
        on='kurzname',
        how='outer',
        suffixes=('_csv', '_api')
    )
    
    # Get all columns that exist in both DataFrames (except kurzname)
    common_columns = [col for col in csv_data.columns 
                     if col in vehicles_df.columns and col != 'kurzname']
    
    # For each common column, combine the values, preferring the API data when available
    for col in common_columns:
        csv_col = f"{col}_csv"
        api_col = f"{col}_api"
        if csv_col in merged_df.columns and api_col in merged_df.columns:
            merged_df[col] = merged_df[api_col].fillna(merged_df[csv_col])
            # Drop the duplicate columns
            merged_df = merged_df.drop([csv_col, api_col], axis=1)
    
    # Convert DataFrame to JSON-serializable format
    result = merged_df.replace({pd.NA: None, pd.NaT: None}).to_dict('records')
    
    return result




