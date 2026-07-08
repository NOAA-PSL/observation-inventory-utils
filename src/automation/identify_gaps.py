import pandas as pd
from sqlalchemy import create_engine
import re
import automation_utils as au
import atm_dicts
import ocn_dicts
import ice_dicts
import ozone_dicts
import obs_inv_utils.obs_inv_cli as cli

# ==========================================
# 1. Configuration & Setup
# ==========================================
engine = cli.get_engine()  # Ensure the database engine is initialized

# ==========================================
# 2. Build the Interval Mapping
# ==========================================
print("Building dynamic interval mapping from configurations...")

def get_base_prefix(s3_prefix):
    """
    Strips wildcard date formatting (e.g., %Y, %m) from the s3_prefix 
    so we can match it against the database parent_dir.
    """
    # Cuts off the prefix right before the first wildcard
    return s3_prefix.split('%')[0]

# Create a dictionary mapping the base directory path to its cycling interval in seconds.
# (Assuming au.CYCLING_DAILY etc., resolve to integers like 86400, 21600, 3600)
interval_map = {}
for info in atm_dicts.atm_infos + ocn_dicts.ocn_infos + ice_dicts.ice_infos + ozone_dicts.ozone_infos:
    base_dir = get_base_prefix(info.s3_prefix)
    interval_map[base_dir] = info.cycling_interval

# ==========================================
# 3. Extract Data
# ==========================================
query = """
    SELECT 
        parent_dir,
        prefix, 
        data_type, 
        data_format, 
        suffix, 
        obs_day, 
        cycle_time 
    FROM OBS_INVENTORY_TABLE
    ORDER BY prefix, data_type, data_format, suffix, obs_day, cycle_time
"""

print("Fetching data from the database...")
df = pd.read_sql(query, engine)

# ==========================================
# 4. Process & Map Dynamic Intervals
# ==========================================
print("Processing streams and calculating dynamic gaps...")

# Handle NULL values for stream identification
stream_cols = ['prefix', 'data_type', 'data_format', 'suffix']
df[stream_cols] = df[stream_cols].fillna('NULL')
df['stream_id'] = df['prefix'] + "_" + df['data_type'] + "_" + df['data_format'] + "_" + df['suffix']

# Calculate the exact timestamp of the observation
df['exact_obs_time'] = pd.to_datetime(df['obs_day']) + pd.to_timedelta(df['cycle_time'], unit='s')

# Map the correct cycling interval to each row based on the parent_dir
def map_interval(parent_dir):
    for base_dir, interval in interval_map.items():
        if parent_dir.startswith(base_dir):
            return interval
    # Fallback default if a stream isn't in your inventory dicts (e.g., 6 hours)
    return 21600 

df['expected_interval_seconds'] = df['parent_dir'].apply(map_interval)
df['expected_timedelta'] = pd.to_timedelta(df['expected_interval_seconds'], unit='s')

# Sort to ensure chronological order within each stream
df = df.sort_values(by=['stream_id', 'exact_obs_time'])

# Calculate the actual time difference between consecutive rows in a stream
df['time_diff'] = df.groupby('stream_id')['exact_obs_time'].diff()

# ==========================================
# 5. Identify Gaps & Save to File
# ==========================================
# A gap exists if the actual time difference is strictly greater than the expected timedelta
gaps_df = df[df['time_diff'] > df['expected_timedelta']].copy()

output_filename = "cycle_time_gaps.csv"

if gaps_df.empty:
    print("\nNo cycle gaps found! All streams are continuous based on their configured intervals.")
else:
    # Calculate the exact missing windows
    gaps_df['missed_start'] = gaps_df['exact_obs_time'] - gaps_df['time_diff'] + df['expected_timedelta']
    gaps_df['missed_end'] = gaps_df['exact_obs_time'] - df['expected_timedelta']
    
    # Select the most relevant columns for the output file
    output_cols = [
        'stream_id', 
        'expected_interval_seconds', 
        'exact_obs_time', 
        'missed_start', 
        'missed_end', 
        'time_diff'
    ]
    
    # Filter the DataFrame and rename columns for better readability in the CSV
    clean_df = gaps_df[output_cols].rename(columns={
        'exact_obs_time': 'gap_detected_before',
        'time_diff': 'gap_duration'
    })
    
    # Save the dataframe to a CSV file (excluding the index)
    clean_df.to_csv(output_filename, index=False)
    
    print(f"\nFound {len(gaps_df)} gap(s) in the data streams.")
    print(f"Detailed results successfully saved to: {output_filename}")