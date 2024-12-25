import pandas as pd
import dask.dataframe as dd
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import journey_orchestrate as js




def last_touch(df,key,timestamp_column , n_partition):
    df['time'] = pd.to_datetime(df['timestamp_column'])
    ddf = dd.from_pandas(df, npartitions=n_partition)
    ddf = ddf.sort_values(by=[key, 'time'], ascending=[True, False])
    last_touch = ddf.groupby(key).head(1).compute()
    return last_touch




    
def first_touch(df, key, timestamp_column, n_partition):
    df['time'] = pd.to_datetime(df[timestamp_column])
    ddf = dd.from_pandas(df, npartitions=n_partition)
    ddf = ddf.sort_values(by=[key, 'time'], ascending=[True, True])
    first_touch = ddf.groupby(key).head(1).compute()
    return first_touch





def linear_attribution(df, key,timestamp_column, npartitions, value=1.0):
    df['time'] = pd.to_datetime(df[timestamp_column])
    df = dd.from_pandas(df, npartitions=npartitions)

    df = df.sort_values(by=[key, 'time'], ascending=[True, True])

    # Define a function to apply the linear attribution within each group (customer)
    def assign_attribution(group):
        n_touchpoints = len(group)
        attribution_value = value / n_touchpoints if n_touchpoints > 0 else 0
        group['attribution'] = attribution_value
        return group

    # Define metadata that includes the new 'attribution' column
    meta = df
    meta['attribution'] = pd.Series(dtype='float64')  # Add 'attribution' column to metadata

    # Apply the attribution calculation for each customer group, providing explicit metadata
    attributed_df = df.groupby(key).apply(assign_attribution, meta=meta)

    return attributed_df.compute()





def time_decay_attribution(df, id_column, timestamp_column, channel_column, npartition, decay_factor):
    # Convert the 'time' column to datetime format
    df['time'] = pd.to_datetime(df[timestamp_column])
    
    # Create a Dask DataFrame from the Pandas DataFrame
    ddf = dd.from_pandas(df, npartitions=npartition)
    
    # Sort the Dask DataFrame by ID and time (in descending order for time decay)
    ddf = ddf.sort_values(by=[id_column, 'time'], ascending=[True, False])
    
    # Define the function to apply time decay attribution to each group
    def apply_time_decay(group):
        group['time_diff'] = (group['time'].iloc[0] - group['time']).dt.total_seconds()
        group['decay'] = decay_factor ** (group['time_diff'] / 3600)  # Decay per hour
        group['attribution'] = group['decay'] / group['decay'].sum()  # Normalize attribution
        return group

    # Define the metadata (meta) schema to match the final DataFrame structure
    meta = df[[id_column, 'time', channel_column]].copy()  # Keep the original columns
    meta['time_diff'] = pd.Series(dtype='float64')
    meta['decay'] = pd.Series(dtype='float64')
    meta['attribution'] = pd.Series(dtype='float64')

    # Apply the time decay attribution function to each group and pass the metadata schema
    attributed_df = ddf.groupby(id_column).apply(apply_time_decay, meta=meta)
    
    return attributed_df.compute()





def position_u_shaped_attribution_dask(df, id_column, timestamp_column, journey_column, npartitions , decay_factor ):
    attribution_results = []
    df['time'] = pd.to_datetime(df[timestamp_column])  # Ensure time column is datetime
    ddf = dd.from_pandas(df, npartitions=npartitions)
    
    # Sort the data by 'time' for each ID
    ddf = ddf.sort_values(by=['ID', 'time'], ascending=[True, True])

    def apply_u_shaped_attribution(group):
        # Calculate the number of touchpoints
        n = len(group)
        
        if n == 1:
            # If there's only one touchpoint, it gets all the attribution
            group['attribution'] = 1.0
        elif n == 2:
            # If there are two touchpoints, both get 50% attribution
            group['attribution'] = 0.5
        else:
            # Allocate attribution: 40% to the first and last touchpoint, 20% to the middle
            group['attribution'] = 0.0  # Start by assigning 0 attribution to all touchpoints
            # First touchpoint gets 40% of attribution
            group.loc[group.index[0], 'attribution'] = decay_factor
            # Last touchpoint gets 40% of attribution
            group.loc[group.index[-1], 'attribution'] = decay_factor
            # Remaining attribution is 20% to be equally distributed among the middle touchpoints
            if n > 2:
                middle_attribution = (1 - 2 * decay_factor) / (n - 2)
                group.loc[group.index[1:-1], 'attribution'] = middle_attribution
        
        # Normalize attribution to ensure it sums to 1
        group['attribution'] /= group['attribution'].sum()
        
        return group
    
    # Apply attribution for each group (group by 'ID')
    meta = df[[id_column, 'time', journey_column]].copy()  # Original columns
    meta['attribution'] = pd.Series(dtype='float64')  # Add attribution column to the meta
    attributed_ddf = ddf.groupby(id_column).apply(apply_u_shaped_attribution, meta=meta)
    
    return attributed_ddf.compute()




def w_shaped_attribution_dask(df, id_column,timestamp_column, journey_column, npartitions, decay_factor):
    """
    Apply a W-shaped attribution model to a Dask DataFrame where the first, middle, and last touchpoints
    receive the highest attribution. The remaining attribution is distributed evenly across any middle touchpoints.
    
    Parameters:
    - df: Dask DataFrame containing the dataset with customer IDs, journey path, and touchpoint channels.
    - id_column: The name of the column that identifies each customer (e.g., 'ID').
    - journey_column: The name of the column containing the journey path or touchpoint channel.
    - npartitions: The number of partitions for the Dask DataFrame.
    - decay_factor: The factor for allocating the attribution to first, middle, and last touchpoints. Default is 0.3.
    
    Returns:
    - Dask DataFrame with the attribution values assigned to each touchpoint for each customer.
    """
    
    # Sort the data by time for each ID (ascending order)
    df['time'] = pd.to_datetime(df[timestamp_column])
    ddf = dd.from_pandas(df, npartitions=npartitions)
    ddf = ddf.sort_values(by=['ID', 'time'], ascending=[True, True])

    def apply_w_shaped_attribution(group):
        # Get number of touchpoints
        n = len(group)
        
        # Initialize attribution column to 0
        group['attribution'] = 0.0
        
        if n == 1:
            # If only one touchpoint, it gets all the attribution
            group['attribution'] = 1.0
        else:
            # Apply W-shaped attribution
            group.loc[group.index[0], 'attribution'] = decay_factor  # First touchpoint
            group.loc[group.index[-1], 'attribution'] = decay_factor  # Last touchpoint
            
            if n > 2:
                middle_attribution = (1 - 2 * decay_factor) / (n - 2)
                group.loc[group.index[1:-1], 'attribution'] = middle_attribution
        
        # Normalize attribution to ensure it sums to 1
        group['attribution'] /= group['attribution'].sum()
        
        return group

    # Define the metadata (`meta`) with all required columns
    meta = df[[id_column, 'time', journey_column]].copy()  # Original columns
    meta['attribution'] = pd.Series(dtype='float64')  # Add attribution column to the meta
    
    # Apply the attribution logic to each group (group by 'ID')
    attributed_ddf = ddf.groupby(id_column).apply(apply_w_shaped_attribution, meta=meta)
    
    return attributed_ddf.compute()
    




def last_nondirect_click_attribution(df, id_column,timestamp_column, journey_column,direct_channel_name, npartitions):
    # Convert the 'time' column to datetime
    df['time'] = pd.to_datetime(df[timestamp_column])
    
    # Convert to Dask DataFrame for parallel processing
    ddf = dd.from_pandas(df, npartitions=npartitions)
    
    # Sort the dataframe by ID and time
    ddf = ddf.sort_values(by=[id_column, 'time'], ascending=[True, True])

    def apply_last_nondirect_attribution(group):
        # Identify the last non-direct click
        nondirect_group = group[group[journey_column] != direct_channel_name]
        
        if len(nondirect_group) > 0:
            # The last non-direct click gets all attribution (1.0)
            last_nondirect_index = nondirect_group.index[-1]
            group['attribution'] = 0.0
            group.loc[last_nondirect_index, 'attribution'] = 1.0
        else:
            # If no non-direct click exists, no attribution (NaN or 0.0) for the user
            group['attribution'] = 0.0
        
        return group
    
    # Apply the function to each group by ID
    meta = df[[id_column, 'time', journey_column]].copy()  # Prepare metadata for Dask
    meta['attribution'] = pd.Series(dtype='float64')  # Add the attribution column
    attributed_ddf = ddf.groupby(id_column).apply(apply_last_nondirect_attribution, meta=meta)
    
    return attributed_ddf.compute()   
    