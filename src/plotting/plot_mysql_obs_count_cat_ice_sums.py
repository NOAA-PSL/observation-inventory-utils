#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, date
import matplotlib.dates as mdates
import os
import argparse
import plot_utils as utils
import obs_inv_utils.inventory_table_factory as itf

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='out_dir', help="output directory for figures",default='figures',type=str)
parser.add_argument("-dev", dest='dev', help='Use this flag to add a timestamp to the filename for development', default=False, type=bool)
parser.add_argument("-window", dest='window', help=" Rolling average of window size", type=int, default=1)
parser.add_argument("-version", dest='ioda_version', help="Version of ioda to include in the plot, if not provided will include all versions inventoried. Value should be an int.", type=int, default=0)
parser.add_argument("-title", dest='title', help='Title for the plot', type=str, default="Time Series of Observation Count")
parser.add_argument("-cats", dest='cat_list', help="Categories of sensors to plot", type=str, nargs='+')
args = parser.parse_args()

category_dicts = {
    'icec_nsidc_nh' : {'observations/reanalysis/icec/nsidc/nh'},
    'icec_nsidc_sh' : {'observations/reanalysis/icec/nsidc/sh'},
    'icec_emc' : {'observations/reanalysis/icec/emc'},
    'icefb': {'observations/reanalysis/icefb'},
    'icec_nsidc': {'observations/reanalysis/icec/nsidc'},
    'icec_glore_nh' : {'observations/reanalysis/icec/GLORe/nh'},
    'icec_glore_sh' : {'observations/reanalysis/icec/GLORe/sh'},
    'icec_glore': {'observations/reanalysis/icec/GLORe'},
    'icec_emc_nhsh': {'observations/reanalysis/icec/emc'},
    'icec_glore_nh-short' : {'observations/reanalysis/icec/GLORe/nh'},
    'icec_glore_sh-short' : {'observations/reanalysis/icec/GLORe/sh'}
}

category_titles = {
    'icec_nsidc_nh': 'Ice Concentration NSIDC NH',
    'icec_nsidc_sh': 'Ice Concentration NSIDC SH',
    'icec_emc': 'Ice Concentration EMC Combined',
    'icefb': 'Ice Free Board',
    'icec_nsidc': 'Ice Concentration NSIDC', 
    'icec_glore_nh': 'Ice Concentration GLORe NH',
    'icec_glore_sh': 'Ice Concentration GLORe SH',
    'icec_glore': 'Ice Concentration GLORe',
    'icec_emc_nhsh': 'Ice Concentration NH+SH',
    'icec_glore_nh-short': 'Ice Concentration NH',
    'icec_glore_sh-short': 'Ice Concentration SH'
}


#parameters
daterange=[date(1979,1,1), date(2026,1,1)]

def select_sensor(sensor, db_frame):
    dftmp = db_frame.loc[db_frame['sensor']==sensor]
    return dftmp

def get_sensor(row):
    directory = row['parent_dir']
    sensor = directory.split("/")[2]
    return sensor

def get_category(row):
    parent_dir = row['parent_dir']        
    for category, prefixes in category_dicts.items():
        if category in args.cat_list:
            for prefix in prefixes:
                if parent_dir.startswith(prefix):
                    return category
    return None

def make_sensor_list_by_category(cat_list):
    sensor_list = []
    for category in cat_list:
        if category in category_dicts:
            for cat in category_dicts[category]:
                sensor_list.append(cat)
        else: 
            print(f"No category found with name {category}")
    return sensor_list

sensor_list = make_sensor_list_by_category(args.cat_list)
#read data from sql database of obs counts
df = utils.get_ioda_nc_by_sensor(sensor_list)

df['datetime'] = pd.to_datetime(df.obs_day)
df['category'] = df.apply(get_category, axis=1)

df['date_only'] = df['datetime'].dt.date

if args.ioda_version == 2:
    df = df[df["ioda_version"] == "v2"]
if args.ioda_version == 3:
    df = df[df["ioda_version"] == "v3"]

# Group by sensor and obs_day-- date only, summing obs_count
grouped_df = df.groupby(['category', 'date_only'], as_index=False)['var_count'].sum()

# Convert obs_day to datetime if needed
grouped_df['date_only'] = pd.to_datetime(grouped_df['date_only'])

# Sort the grouped data
grouped_df = grouped_df.sort_values(by='date_only')

grouped_df['rolling_avg'] = grouped_df.groupby('category')['var_count'].transform(lambda x: x.rolling(window=args.window, min_periods=1).mean())

print(grouped_df)

# Get unique sensors
unique_categories = grouped_df['category'].unique()

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8))  # Increase figure width

for category in unique_categories:
    single_category_df = grouped_df[(grouped_df['category'] == category)]

    ax.plot(single_category_df['date_only'], single_category_df['rolling_avg'], label=f'{category_titles[category]}')

# Calculate the total of the rolling averages and apply a final smoothing
total_series = grouped_df.groupby('date_only')['rolling_avg'].sum()
smoothed_total = total_series.rolling(window=args.window, min_periods=1).mean().reset_index()

# Plot the total line
ax.plot(smoothed_total['date_only'], smoothed_total['rolling_avg'], label='Total', color='black', linestyle='--', linewidth=3)

ax.set_title(f'{args.title}', fontsize = 18) #16
ax.set_xlabel('Observation Day', fontsize = 17) #14
ax.set_ylabel('Average Daily Observation Count', fontsize = 17) #14
ax.set_yscale('log')  # log10 y-axis
ax.set_xlim(daterange)
# Formatting the x-axis for dates (display only the year)
ax.xaxis.set_major_locator(mdates.YearLocator(5))  # Major ticks every 5 years
ax.xaxis.set_minor_locator(mdates.YearLocator())  # Minor ticks every year
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
plt.xticks(rotation=45, ha='right')
ax.tick_params(labelsize=12)

# Add grid and legend
ax.grid(True)
ax.legend(fontsize = 12, loc='upper left') #11

plt.tight_layout()
# plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
file_name = f"ice_time_series_combo_v{args.ioda_version}_sum_{args.window}_days.png"
if args.dev:
    file_name = f"ice_time_series_combo_v{args.ioda_version}_sum_{args.window}_days_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
