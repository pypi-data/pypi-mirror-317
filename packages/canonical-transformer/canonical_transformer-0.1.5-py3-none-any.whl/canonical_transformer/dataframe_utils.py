import pandas as pd
from .format_utils import capitalize_column_names_in_df

def map_df_to_data(df, capitalize=False):
    """
    Convert a DataFrame to a list of dictionaries.

    Parameters:
    df (pd.DataFrame): The DataFrame to convert.
    capitalize (bool): Whether to capitalize the column names. Default is False.

    Returns:
    list: A list of dictionaries representing the DataFrame.
    """
    df = df.reset_index() if df.index.name else df
    df = df.fillna('')    
    if capitalize:
        df = capitalize_column_names_in_df(df)
    data = df.to_dict(orient='records')
    return data

def map_data_to_df(data):
    """
    Convert a list of dictionaries to a DataFrame.

    Parameters:
    data (list): A list of dictionaries to convert.

    Returns:
    pd.DataFrame: The resulting DataFrame.
    """
    df = pd.DataFrame(data)
    return df
