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
    'temperature': {'TEMPERATURE'},
    'spec humid': {'SPECIFIC HUMIDITY'},
    'precip' : {'PRECIPITABLE H20'},
    'pressure': {'PRESSURE'}, 
    'wind comp': {'WIND COMPONENTS'}, 
    'height': {'HEIGHT'},
    'conv': {'TEMPERATURE', 'SPECIFIC HUMIDITY', 'PRESSURE', 'WIND COMPONENTS', 'HEIGHT'}
}

category_titles = {
    'temperature': 'Temperature',
    'spec humid': 'Specific Humidity',
    'precip': 'Precipitable H20',
    'pressure': 'Pressure',
    'wind comp': 'Wind Components',
    'height': 'Height', 
    'conv': 'Conventional Data',
}


#parameters
daterange=[date(1979,1,1), date(2026,1,1)]

def select_variable(variable, db_frame):
    dftmp = db_frame.loc[db_frame['variable']==variable]
    return dftmp

def get_category(row):
    variable = row['variable']
    for cat in args.cat_list:
        if variable in category_dicts.get(cat, set()):
            return cat
    return None

def make_variable_list_by_categories(cat_list):
    variable_list = []
    for category in cat_list:
        if category in category_dicts:
            for cat in category_dicts[category]:
                variable_list.append(cat)
        else: 
            print(f"No category found with name {category}")
    return variable_list


variable_list = make_variable_list_by_categories(args.cat_list)
#read data from sql database of obs counts
df = utils.get_distinct_prepbufr_by_variable(variable_list)

df['datetime'] = pd.to_datetime(df.obs_day)
df['category'] = df.apply(get_category, axis=1)

df['date_only'] = df['datetime'].dt.date

# Group by sensor and obs_day-- date only, summing obs_count
grouped_df = df.groupby(['category', 'date_only'], as_index=False)['tot'].sum()

# Convert obs_day to datetime if needed
grouped_df['date_only'] = pd.to_datetime(grouped_df['date_only'])

# Sort the grouped data
grouped_df = grouped_df.sort_values(by=['category','date_only'])

grouped_df['rolling_avg'] = grouped_df.groupby('category')['tot'].transform(lambda x: x.rolling(window=args.window, min_periods=1).mean())

# Get unique sensors
unique_categories = grouped_df['category'].unique()

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8))  # Increase figure width

for category in unique_categories:
    single_category_df = grouped_df[(grouped_df['category'] == category)]

    ax.plot(single_category_df['date_only'], single_category_df['rolling_avg'], label=f'{category_titles[category]}')

ax.set_title(f'{args.title}', fontsize = 20) #16
ax.set_xlabel('Observation Day', fontsize = 18) #14
ax.set_ylabel('Average Daily Observation Count', fontsize = 18) #14
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
ax.legend(fontsize = 15) #11

plt.tight_layout()
# plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
file_name = f"conv_time_series_combo_avg_{args.window}_days.png"
if args.dev:
    file_name = f"conv_time_series_combo_avg_{args.window}_days_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
