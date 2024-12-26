"""
This module provides alias functions for saving data in different formats.
"""

from .save_utils import save_df_as_csv, save_df_as_json, save_data_as_json
from .dataframe_utils import map_df_to_data, map_data_to_df

# Aliases for saving DataFrame as CSV
map_df_to_csv = save_df_as_csv
map_dataframe_to_csv = save_df_as_csv
save_dataframe_as_csv = save_df_as_csv

# Aliases for saving DataFrame as JSON
map_df_to_json = save_df_as_json
map_dataframe_to_json = save_df_as_json
save_dataframe_as_json = save_df_as_json

# Alias for saving data as JSON
map_data_to_json = save_data_as_json

# Aliases for mapping DataFrame to data
map_dataframe_to_data = map_df_to_data
map_data_to_dataframe = map_data_to_df