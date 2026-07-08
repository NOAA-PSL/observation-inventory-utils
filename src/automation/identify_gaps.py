import pandas
import automation_utils as au
import atm_dicts
import ocn_dicts
import ice_dicts
import ozone_dicts
import obs_inv_utils.inventory_table_factory as itf
from obs_inv_utils.inventory_table_factory import ObsInventory as oi


def identify_cycle_gaps(inv_infos, output_filename="cycle_time_gaps.csv"):
    # ==========================================
    # 1. Database Query using ORM
    # ==========================================
    session = itf.Session()

    # Query only the necessary columns for gap identification, ordered appropriately
    query = session.query(
        oi.parent_dir,
        oi.prefix,
        oi.data_type,
        oi.data_format,
        oi.suffix,
        oi.obs_day,
        oi.cycle_time
    ).order_by(
        oi.prefix,
        oi.data_type,
        oi.data_format,
        oi.suffix,
        oi.obs_day,
        oi.cycle_time
    )

    # Execute the query
    results = query.all()

    # Convert results to a list of dictionaries
    result_dicts = [
        {
            'parent_dir': result.parent_dir,
            'prefix': result.prefix,
            'data_type': result.data_type,
            'data_format': result.data_format,
            'suffix': result.suffix,
            'obs_day': result.obs_day,
            'cycle_time': result.cycle_time
        }
        for result in results
    ]

    # Convert the list of dictionaries to a pandas DataFrame
    df = pandas.DataFrame(result_dicts)

    # Close the session
    session.close()

    # Early exit if the table is empty
    if df.empty:
        print("No records found in OBS_INVENTORY_TABLE.")
        return df

    # ==========================================
    # 2. Build the Interval Mapping
    # ==========================================
    def get_base_prefix(s3_prefix):
        # Strips wildcard date formatting (e.g., %Y, %m)
        return s3_prefix.split('%')[0]

    interval_map = {}
    for info in inv_infos:
        base_dir = get_base_prefix(info.s3_prefix)
        interval_map[base_dir] = info.cycling_interval

    # ==========================================
    # 3. Process & Map Dynamic Intervals
    # ==========================================
    # Handle NULL values for stream identification
    stream_cols = ['prefix', 'data_type', 'data_format', 'suffix']
    df[stream_cols] = df[stream_cols].fillna('NULL')
    df['stream_id'] = df['prefix'] + "_" + df['data_type'] + "_" + df['data_format'] + "_" + df['suffix']

    # Calculate the exact timestamp of the observation
    df['exact_obs_time'] = pandas.to_datetime(df['obs_day']) + pandas.to_timedelta(df['cycle_time'], unit='s')

    # Map the correct cycling interval to each row based on the parent_dir
    def map_interval(parent_dir):
        if parent_dir:
            for base_dir, interval in interval_map.items():
                if parent_dir.startswith(base_dir):
                    return interval
        # Fallback default if a stream isn't in your inventory dicts (e.g., 6 hours)
        return 21600 

    df['expected_interval_seconds'] = df['parent_dir'].apply(map_interval)
    df['expected_timedelta'] = pandas.to_timedelta(df['expected_interval_seconds'], unit='s')

    # Sort to ensure chronological order within each stream
    df = df.sort_values(by=['stream_id', 'exact_obs_time'])

    # Calculate the actual time difference between consecutive rows in a stream
    df['time_diff'] = df.groupby('stream_id')['exact_obs_time'].diff()

    # ==========================================
    # 4. Identify Gaps & Save to File
    # ==========================================
    # A gap exists if the actual time difference is strictly greater than the expected timedelta
    gaps_df = df[df['time_diff'] > df['expected_timedelta']].copy()

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

    return gaps_df

def main():
    print("Starting cycle gap analysis...")
    
    # Define a custom output filename if desired
    report_file = "reanalysis_cycle_gaps.csv"
    
    infos = atm_dicts.atm_infos + ocn_dicts.ocn_infos + ice_dicts.ice_infos + ozone_dicts.ozone_infos

    # Run the gap identification function
    gaps_dataframe = identify_cycle_gaps(
        inv_infos=infos, 
        output_filename=report_file
    )
    
    # Optional: Do something else with the returned DataFrame if needed
    if not gaps_dataframe.empty:
        print("\nAnalysis complete. Please review the generated CSV file for details.")
    else:
        print("\nAnalysis complete. All streams look good!")

if __name__ == "__main__":
    main()