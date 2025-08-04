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
parser.add_argument("-variable", dest='var', help="Variable of conventional data to plot", type=str)
parser.add_argument("-window", dest='window', help="Category of sensors to plot", type=int, default=1)
args = parser.parse_args()

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
    'temperature': 'Conventional Temperature',
    'spec humid': 'Conventional Specific Humidity',
    'precip': 'Conventional Precipitable H20',
    'pressure': 'Conventional Pressure',
    'wind comp': 'Conventional Wind Components',
    'height': 'Conventional Height', 
    'conv': 'Conventional Data',
}


#parameters
daterange=[date(1979,1,1), date(2026,1,1)]

#read data from sql database of obs counts
df = utils.get_distinct_prepbufr_by_variable(variable_dicts[args.var])

df['datetime'] = pd.to_datetime(df.obs_day)

df['date_only'] = df['datetime'].dt.date

# Group by sensor and obs_day-- date only, summing obs_count
grouped_df = df.groupby(['variable', 'date_only'], as_index=False)['tot'].sum()

# Convert obs_day to datetime if needed
grouped_df['date_only'] = pd.to_datetime(grouped_df['date_only'])

# Sort the grouped data
grouped_df = grouped_df.sort_values(by='date_only')

#Rolling average
grouped_df['rolling_avg'] = grouped_df['tot'].rolling(window=args.window, min_periods=1).mean()

# Get unique sensors
unique_vars = grouped_df['variable'].unique()

# Create the plot
fig, ax = plt.subplots(figsize=(14, 8))  # Increase figure width

#This handles if dictionaries are increased to have mulitple variables at once 
for var in unique_vars:
    single_var_df = grouped_df[(grouped_df['variable'] == var)]

    ax.plot(single_var_df['date_only'], single_var_df['rolling_avg'],  label=f'{var}')

ax.set_title(f'Time Series of {variable_titles[args.var]}', fontsize = 16)
ax.set_xlabel('Observation Day', fontsize = 14)
ax.set_ylabel('Daily Observation Count', fontsize = 14)
ax.set_yscale('log')  # log10 y-axis
ax.set_xlim(daterange)
# Formatting the x-axis for dates (display only the year)
ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
plt.xticks(rotation=45, ha='right')

# Add grid and legend
ax.grid(True)
ax.legend(fontsize = 12) #only need to add legend if we add variable names for multiple variables

plt.tight_layout()
plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
file_name = f"{args.var}_conv_count_avg_{args.window}_days.png"
if args.dev:
    file_name = f"{args.var}_conv_count_avg_{args.window}_days_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
