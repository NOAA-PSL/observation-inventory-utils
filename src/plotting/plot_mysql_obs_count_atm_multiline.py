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
parser.add_argument("-conv-cats", dest='conv_cat_list', help="Categories of conventional variables to plot", type=str, nargs='+')
args = parser.parse_args()

category_dicts = {
    'AMV': {'amv'},
    'AMV-long': {'amv'},
    'GPS': {'gps'},
    'GPS-long': {'gps'},
    'geo_rad' : {'geo/ahicsr', 'geo/geoimr', 'geo/goesfv', 'geo/goesnd', 'geo/gsrasr'},
    'hyper_infrared': {'cris', 'iasi', 'airs/nasa'}, 
    'multi_infrared': {'ssu', 'hirs/1bhrs2', 'hirs/1bhrs3', 'hirs/1bhrs4'}, 
    'micro_imagers': {'gmi', 'amsr2', 'tmi', 'amsre', 'ssmi', 'ssmis'},
    'micro_sounders': {'saphir', 'mhs', 'atms', 'msu', 'amsub', 'amsua/1bamua'}, 
    'ozone': {'ozone'},
    'polar_orbit_BT': {'cris', 'iasi', 'airs/nasa', 'ssu', 'hirs/1bhrs2', 'hirs/1bhrs3', 'hirs/1bhrs4' , 'gmi', 'amsr2', 'tmi', 'amsre', 'ssmi', 'ssmis', 'saphir', 'mhs', 'atms', 'msu', 'amsub', 'amsua/1bamua'},
    'tovs': {'hirs/1bhrs2', 'ssu', 'msu'},
    'atovs': {'hirs/1bhrs3', 'hirs/1bhrs4', 'amsua/1bamua', 'amsub', 'mhs'},
    'post-atovs': {'cris', 'atms', 'iasi'},
    'geo-imager': {'geo/geoimr', 'geo/goesfv'},
    'geo-sounder': {'geo/goesnd'},
    'geo-adv-img': {'geo/ahicsr', 'geo/gsrasr'},
}

category_titles = {
    'AMV': 'AMV',
    'AMV-long': 'Atmospheric Motion Vectors',
    'GPS': 'GPS',
    'GPS-long': 'Global Positioning System',
    'geo_rad': 'Geostationary Radiances',
    'hyper_infrared': 'Hyperspectral Infrared',
    'multi_infrared': 'Multispectral Infrared',
    'micro_imagers': 'Microwave Imagers', 
    'micro_sounders': 'Microwave Sounders', 
    'ozone': 'Ozone',
    'polar_orbit_BT': 'Polar Orbiting Brightness Temperature',
    'tovs': 'TOVS',
    'atovs': 'ATOVS',
    'post-atovs': 'Post-ATOVS',
    'geo-imager': 'GEO Imager',
    'geo-sounder': 'GEO Sounder',
    'geo-adv-img': 'GEO Advanced Imager',
}

variable_dicts = {
    'temperature': {'TEMPERATURE'},
    'spec humid': {'SPECIFIC HUMIDITY'},
    'precip' : {'PRECIPITABLE H20'},
    'pressure': {'PRESSURE'}, 
    'wind comp': {'WIND COMPONENTS'}, 
    'height': {'HEIGHT'},
    'conv': {'TEMPERATURE', 'SPECIFIC HUMIDITY', 'PRESSURE', 'WIND COMPONENTS', 'HEIGHT'}
}

variable_titles = {
    'temperature': 'Temperature',
    'spec humid': 'Specific Humidity',
    'precip': 'Precipitable H20',
    'pressure': 'Pressure',
    'wind comp': 'Wind Components',
    'height': 'Height', 
    'conv': 'Conventional Data',
}

#parameters
daterange=[date(1975,1,1), date(2026,1,1)]

def select_sensor(sensor, db_frame):
    dftmp = db_frame.loc[db_frame['sensor']==sensor]
    return dftmp

def select_variable(variable, db_frame):
    dftmp = db_frame.loc[db_frame['variable']==variable]
    return dftmp

def get_category(row):
    sensor = row['sensor']
    for cat in args.cat_list:
        if sensor in category_dicts.get(cat, set()):
            return cat
    return None

def get_variable(row):
    variable = row['variable']
    for cat in args.conv_cat_list:
        if variable in variable_dicts.get(cat, set()):
            return cat
    return None

def get_sensor(row):
    directory = row['parent_dir']
    parts = directory.split("/")
    sensor = parts[2]
    if sensor == 'hirs':
        sensor = 'hirs/' + parts[3]
    if sensor == 'geo':
        sensor = 'geo/' + parts[3]
    if sensor == 'airs':
        sensor = 'airs/' + parts[3]
    if sensor == 'amsua':
        sensor = 'amsua/' + parts[3]
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

def make_variable_list_by_conv_categories(cat_list):
    variable_list = []
    for category in cat_list:
        if category in variable_dicts:
            for cat in variable_dicts[category]:
                variable_list.append(cat)
        else: 
            print(f"No category found with name {category}")
    return variable_list


sensor_list = make_sensor_list_by_categories(args.cat_list)
#read data from sql database of obs counts
df = utils.get_distinct_bufr_by_sensors(sensor_list)

variable_list = make_variable_list_by_conv_categories(args.conv_cat_list)
df_conv = utils.get_distinct_prepbufr_by_variable(variable_list)

df['datetime'] = pd.to_datetime(df.obs_day)
df['sensor'] = df.apply(get_sensor, axis=1)
df['category'] = df.apply(get_category, axis=1)

df_conv['datetime'] = pd.to_datetime(df_conv.obs_day)
df_conv['category'] = df_conv.apply(get_variable, axis=1)

df['date_only'] = df['datetime'].dt.date
df_conv['date_only'] = df_conv['datetime'].dt.date

cris_cutoff = pd.to_datetime("2018-01-16 18:00:00")
cris_prefix = "observations/reanalysis/cris/cris/"
df = df.loc[~(df['parent_dir'].str.startswith(cris_prefix) & (df["datetime"] > cris_cutoff))]

# Group by sensor and obs_day-- date only, summing obs_count
grouped_df = df.groupby(['category', 'date_only'], as_index=False)['obs_count'].sum()
grouped_df_conv = df_conv.groupby(['category', 'date_only'], as_index=False)['tot'].sum()

# Convert obs_day to datetime if needed
grouped_df['date_only'] = pd.to_datetime(grouped_df['date_only'])
grouped_df_conv['date_only'] = pd.to_datetime(grouped_df_conv['date_only'])

# Sort the grouped data
grouped_df = grouped_df.sort_values(by=['category','date_only'])
grouped_df_conv = grouped_df_conv.sort_values(by=['category','date_only'])

grouped_df['rolling_avg'] = grouped_df.groupby('category')['obs_count'].transform(lambda x: x.rolling(window=args.window, min_periods=1).mean())
grouped_df_conv['rolling_avg'] = grouped_df_conv.groupby('category')['tot'].transform(lambda x: x.rolling(window=args.window, min_periods=1).mean())

# Get unique sensors
unique_categories = grouped_df['category'].unique()
unique_conv_categories = grouped_df_conv['category'].unique()

# Create the plot
fig, ax = plt.subplots(figsize=(18, 14))  # Increase figure width

for category in unique_categories:
    single_category_df = grouped_df[(grouped_df['category'] == category)]

    ax.plot(single_category_df['date_only'], single_category_df['rolling_avg'], label=f'{category_titles[category]}')

for category in unique_conv_categories:
    single_category_df = grouped_df_conv[(grouped_df_conv['category'] == category)]

    ax.plot(single_category_df['date_only'], single_category_df['rolling_avg'], label=f'{variable_titles[category]}')

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
ax.legend(fontsize = 12) #11

plt.tight_layout()
file_name = f"all_atm_time_series_combo_avg_{args.window}_days.png"
if args.dev:
    file_name = f"all_atm_time_series_combo_avg_{args.window}_days_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
