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
args = parser.parse_args()

#parameters
daterange=[date(1975,1,1), date(2026,1,1)]

def plot_one_line(dftmp, yloc):
    plt.plot(dftmp.datetime, yloc*dftmp.obs_count.astype('bool'),'|',color='black',markersize=5)

def select_sensor(sensor, db_frame):
    dftmp = db_frame.loc[db_frame['sensor']==sensor]
    return dftmp

def get_sensor(row):
    directory = row['parent_dir']
    sensor = directory.split("/")[2]
    return sensor


#read data from sql database of obs counts
df = utils.get_distinct_bufr_by_sensors(['observations/reanalysis/ssu', 'observations/reanalysis/hirs'])

df['datetime'] = pd.to_datetime(df.obs_day)
df['sensor'] = df.apply(get_sensor, axis=1)

unique_sensor = df.sort_values('sensor', ascending=False).drop_duplicates('sensor')

# Convert obs_day to datetime if it is not already in datetime format
if not pd.api.types.is_datetime64_any_dtype(df['obs_day']):
    df['obs_day'] = pd.to_datetime(df['obs_day'])

# Sort the data by obs_day to ensure proper plotting
df = df.sort_values(by='obs_day')

# Create the plot
fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width

for index, row in unique_sensor.iterrows():
    sensor = row['sensor']
    single_sensor_df = df[(df['sensor'] == sensor)]

    ax.scatter(single_sensor_df['obs_day'], single_sensor_df['obs_count'], marker='o', label=f'Sensor {sensor}')

ax.set_title('Time Series for Multispectral Infrared')
ax.set_xlabel('Observation Day')
ax.set_ylabel('Observation Count')
ax.set_yscale('log')  # log10 y-axis

# Formatting the x-axis for dates (display only the year)
ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
plt.xticks(rotation=45, ha='right')

# Add grid and legend
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
file_name = "multispectral_infrared_count.png"
if args.dev:
    file_name = "multispectral_infrared_count_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
