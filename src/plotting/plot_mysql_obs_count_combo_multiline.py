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
parser.add_argument("-title", dest='title', help='Title for the plot', type=str, default="Time Series of Observation Count")
parser.add_argument("-cats", dest='cat_list', help="Categories of sensors to plot", type=str, nargs='+')
args = parser.parse_args()

category_dicts = {
    'AMV': {'amv'},
    'GPS': {'gps'},
    'geo_rad' : {'geo'},
    'hyper_infrared': {'cris', 'iasi', 'airs'}, 
    'multi_infrared': {'ssu', 'hirs'}, 
    'micro_imagers': {'gmi', 'amsr2', 'tmi', 'amsre', 'ssmi', 'ssmis'},
    'micro_sounders': {'saphir', 'mhs', 'atms', 'msu', 'amsub', 'amsua'}, 
    'ozone': {'ozone'},
    'polar_orbit_BT': {'cris', 'iasi', 'airs', 'ssu', 'hirs', 'gmi', 'amsr2', 'tmi', 'amsre', 'ssmi', 'ssmis', 'saphir', 'mhs', 'atms', 'msu', 'amsub', 'amsua'}
}

category_titles = {
    'AMV': 'AMV',
    'GPS': 'GPS',
    'geo_rad': 'Geostationary Radiances',
    'hyper_infrared': 'Hyperspectral Infrared',
    'multi_infrared': 'Multispectral Infrared',
    'micro_imagers': 'Microwave Imagers', 
    'micro_sounders': 'Microwave Sounders', 
    'ozone': 'Ozone',
    'polar_orbit_BT': 'Polar Orbiting Brightness Temperature'
}


#parameters
daterange=[date(1975,1,1), date(2026,1,1)]

def plot_one_line(dftmp, yloc):
    plt.plot(dftmp.datetime, yloc*dftmp.obs_count.astype('bool'),'|',color='black',markersize=5)

def select_sensor(sensor, db_frame):
    dftmp = db_frame.loc[db_frame['sensor']==sensor]
    return dftmp

def get_category(row):
    sensor = row['sensor']
    for cat in args.cat_list:
        if sensor in category_dicts.get(cat, set()):
            return cat
    return None

def get_sensor(row):
    directory = row['parent_dir']
    sensor = directory.split("/")[2]
    return sensor

def make_sensor_list_by_categories(cat_list):
    sensor_list = []
    for category in cat_list:
        if category in category_dicts:
            for cat in category_dicts[category]:
                sensor_list.append("observations/reanalysis/" + cat)
        else: 
            print(f"No category found with name {category}")
    return sensor_list


sensor_list = make_sensor_list_by_categories(args.cat_list)
#read data from sql database of obs counts
df = utils.get_distinct_bufr_by_sensors(sensor_list)

df['datetime'] = pd.to_datetime(df.obs_day)
df['sensor'] = df.apply(get_sensor, axis=1)
df['category'] = df.apply(get_category, axis=1)

df['date_only'] = df['datetime'].dt.date

# Group by sensor and obs_day-- date only, summing obs_count
grouped_df = df.groupby(['category', 'date_only'], as_index=False)['obs_count'].sum()

# Convert obs_day to datetime if needed
grouped_df['date_only'] = pd.to_datetime(grouped_df['date_only'])

# Sort the grouped data
grouped_df = grouped_df.sort_values(by=['category','date_only'])

grouped_df['rolling_avg'] = grouped_df.groupby('category')['obs_count'].transform(lambda x: x.rolling(window=args.window, min_periods=1).mean())

# Get unique sensors
unique_categories = grouped_df['category'].unique()

# Create the plot
fig, ax = plt.subplots(figsize=(14, 8))  # Increase figure width

for category in unique_categories:
    single_category_df = grouped_df[(grouped_df['category'] == category)]

    ax.plot(single_category_df['date_only'], single_category_df['rolling_avg'], label=f'{category_titles[category]}')

ax.set_title(f'{args.title}', fontsize = 16)
ax.set_xlabel('Observation Day', fontsize = 14)
ax.set_ylabel('Observation Count', fontsize = 14)
ax.set_yscale('log')  # log10 y-axis
# Formatting the x-axis for dates (display only the year)
ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
#ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
plt.xticks(rotation=45, ha='right')

# Add grid and legend
ax.grid(True)
ax.legend(fontsize = 12)

plt.tight_layout()
plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
file_name = f"atm_time_series_combo_avg_{args.window}_days.png"
if args.dev:
    file_name = f"atm_time_series_combo_avg_{args.window}_days_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
