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
parser.add_argument("-version", dest='ioda_version', help="Version of ioda to include in the plot, if not provided will include all versions inventoried. Value should be an int.", type=int, default=0)
parser.add_argument("-cat", dest='category', help="Category of sensors to plot", type=str)
parser.add_argument("--variables", dest='List of variables to plot from in the category', type=str, nargs='+')
args = parser.parse_args()

category_dicts = {
    'sst': {'sst'},
    'sss': {'sss'},
    'icec' : {'icec'},
    'icefb': {'icefb'}, 
    'adt': {'adt'}, 
    'insitu': {'insitu'},
}

category_titles = {
    'sst': 'SST',
    'sss': 'SSS',
    'icec': 'Ice Concentration',
    'icefb': 'Ice Free Board',
    'adt': 'ADT',
    'insitu': 'Ocean Insitu', 
}

variable_titles = { 
    'sea_ice_area_fraction': 'Sea Ice Area Fraction',
    'seaIceFreeboard': 'Sea Ice Freeboard',
    'sea_ice_freeboard': 'Sea Ice Freeboard',
    'seaIceFraction': 'Sea Ice Fraction',
    'obs_absolute_dynamic_topography': 'Absolute Dynamic Topography', #SSH
    'seaSurfaceSkinTemperature': 'Sea Surface Skin Temperature', 
    'seaSurfaceTemperature': 'Sea Surface Temperature',
    'sea_surface_skin_temperature': 'Sea Surface Skin Temperature',
    'sea_surface_temperature': 'Sea Surface Temperature',
    'sea_surface_salinity': 'Sea Surface Salinity',
    'seaSurfaceSalinity': 'Sea Surface Salinity', 
    'sea_water_salinity': 'Sea Water Salinity',
    'sea_water_temperature': 'Sea Water Temperature',
    'salinity': 'Salinity',
    'waterTemperature': 'Water Temperature'
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

def make_sensor_list_by_category(category):
    sensor_list = []
    if category in category_dicts:
        for cat in category_dicts[category]:
            sensor_list.append("observations/reanalysis/" + cat)
    else: 
        print(f"No category found with name {category}")
    return sensor_list


sensor_list = make_sensor_list_by_category(args.category)
#read data from sql database of obs counts
df = utils.get_ioda_nc_by_sensor(sensor_list)

df['datetime'] = pd.to_datetime(df.obs_day)
df['sensor'] = df.apply(get_sensor, axis=1)

df['date_only'] = df['datetime'].dt.date

if args.ioda_version == 2:
    df = df[df["ioda_version"] == "v2"]
if args.ioda_version == 3:
    df = df[df["ioda_version"] == "v3"]

# Group by sensor and obs_day-- date only, summing obs_count
grouped_df = df.groupby(['sensor', 'date_only'], as_index=False)['var_count'].sum()

# Convert obs_day to datetime if needed
grouped_df['date_only'] = pd.to_datetime(grouped_df['date_only'])

# Sort the grouped data
grouped_df = grouped_df.sort_values(by='date_only')

# Get unique sensors
unique_sensors = grouped_df['sensor'].unique()

# Create the plot
fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width

for sensor in unique_sensors:
    single_sensor_df = grouped_df[(grouped_df['sensor'] == sensor)]

    ax.plot(single_sensor_df['date_only'], single_sensor_df['var_count'], label=f'Sensor {sensor}')

ax.set_title(f'Time Series for {category_titles[args.category]}')
ax.set_xlabel('Observation Day')
ax.set_ylabel('Observation Count')
ax.set_yscale('log')  # log10 y-axis
ax.set_xlim(daterange)
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
file_name = f"{args.category}_v{args.ioda_version}_count_daily.png"
if args.dev:
    file_name = f"{args.category}_v{args.ioda_version}_count_daily_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
