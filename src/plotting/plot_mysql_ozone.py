#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas , matplotlib.pyplot as plt
from datetime import datetime, date
import matplotlib.dates as mdates
import os
from scipy import interpolate
import argparse
import obs_inv_utils.inventory_table_factory as itf
import re
import plot_utils as utils

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='out_dir', help="output directory for figures",default='figures',type=str)
parser.add_argument("-dev", dest='dev', help='Use this flag to add a timestamp to the filename for development', default=False, type=bool)
args = parser.parse_args()

#parameters
daterange=[date(1975,1,1), date(2026,1,1)]

def plot_one_line(dftmp, yloc):
    plt.plot(dftmp.datetime, yloc*dftmp.obs_count.astype('bool'),'|',color='black',markersize=5)

def select_subsensor_dir(subsensor, source_dir, db_frame):
    dftmp = db_frame.loc[(db_frame['subsensor']==subsensor)  & (db_frame['source_dir']==source_dir)]
    return dftmp

def select_sensor(sensor, db_frame):
    dftmp = db_frame.loc[db_frame['sensor']==sensor]
    return dftmp

def get_sensor(row):
    directory = row['parent_dir']
    sensor = directory.split("/")[2]
    return sensor

def get_source_dir(row):
    directory = row['parent_dir']
    directory = directory.replace("observations/reanalysis", "")
    source_dir = re.split("/[12][90][0-9][0-9]/[01][0-9]/", directory)[0]
    return source_dir

def get_subsensor(row):
    source_dir = get_source_dir(row)
    subsensor = source_dir.split("/")[-1]
    return subsensor

#read data from sql database of obs counts
db_frame1 = utils.get_distinct_bufr_by_sensors(['observations/reanalysis/ozone/'])
db_frame2 = utils.get_ozone_nc()

db_frame = pandas.concat([db_frame1, db_frame2], axis=0, ignore_index=True)

db_frame['datetime'] = pandas.to_datetime(db_frame.obs_day)
db_frame['sensor'] = db_frame.apply(get_sensor, axis=1)
db_frame['subsensor'] = db_frame.apply(get_subsensor, axis=1)
db_frame['source_dir'] = db_frame.apply(get_source_dir, axis=1)

db_frame.loc[db_frame['sat_id_name'].isin(['METOP-1', 'METOP-1 (Metop-B']), 'sat_id_name'] = 'METOP-B'
db_frame.loc[db_frame['sat_id_name'].isin(['METOP-2', 'METOP-2 (Metop-A']), 'sat_id_name'] = 'METOP-A'
db_frame.loc[db_frame['sat_id_name'].isin(['METOP-3', 'METOP-3 (Metop-C']), 'sat_id_name'] = 'METOP-C'

#loop and plot sensors/sat_ids
unique_sensor = db_frame[['sensor', 'subsensor', 'source_dir']].value_counts().reset_index(name='count').sort_values(by = ['subsensor', 'source_dir'], ascending=[False, False])
step=0.05
height=step*len(unique_sensor)

#check via print statements
print("check 1")
print(db_frame['subsensor'].value_counts().head(20))
print(db_frame[db_frame['subsensor'].str.len() < 3]['parent_dir'].unique())

print("check 2")
print(len(unique_sensor), "labels vs", db_frame['subsensor'].nunique(), "unique subsensors in frame")

print("check 3")
print("Missing subsensor count:", len(db_frame[db_frame['subsensor'] == '']))

print("check 4")
print(unique_sensor)

print("check 5")
print(db_frame['sensor'])

#make list of sensor&sat labels 
sensor_sub_labels = []
for index, row in unique_sensor.iterrows():
        sensor_sub_labels.append(row.sensor + " " + str(row.subsensor))

plt.close('all')
fig = plt.figure(dpi=300)
fig.patch.set_facecolor('white')
ax = fig.add_axes([0, 0.1, 1, height+step])
plt.title("Inventory of NNJA Ozone Sensors")
plt.xlabel('Observation Date')
plt.ylabel('Sensor')

print("check while plotting")

directory_labels = []
counter=0
for index, row in unique_sensor.iterrows():
    pandas.options.mode.chained_assignment = None
    dftmp = select_subsensor_dir(row['subsensor'], row['source_dir'], db_frame)
    pandas.options.mode.chained_assignment = 'warn'

    if dftmp.empty:
        print("Empty subsensor:", row['subsensor'])
        continue
    print(f"{row['sensor']} {row['subsensor']} -> {len(dftmp)} records")

    dirs = dftmp['source_dir'].unique()
    directory_labels.append(np.array2string(dirs))
    plot_one_line(dftmp, step/2+step*counter)
    counter = counter + 1

print("Lines in figure:", len(ax.lines))

# right after the plotting loop, before setting yticks/yticklabels:
print("\n--- PER-ARTIST LINE INSPECTION ---")
for i, line in enumerate(ax.lines):
    y = np.asarray(line.get_ydata())
    x = np.asarray(line.get_xdata())
    mean_y = float(np.nanmean(y)) if len(y) else float('nan')
    nonzero = np.count_nonzero(y)
    xmin, xmax = (np.nanmin(x) if len(x) else np.nan, np.nanmax(x) if len(x) else np.nan)
    print(f"line {i:02d}: mean_y={mean_y:.4f}, nonzero_points={nonzero}, x_count={len(x)}, x_range=({xmin}, {xmax})")


ax.set_yticks(step/2+step*np.arange(counter))
ax.set_yticklabels(sensor_sub_labels)
ax.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
ax.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
ax.set_xlim(daterange)
ax.set_ylim([0-step, height+step])
ax.grid(which='major',color='grey', linestyle='-', linewidth=0.5)
ax.grid(which='minor', color='grey', linestyle='--', linewidth=0.2)
ax2 = ax.twinx()
ax2.set_yticks(step/2+step*np.arange(counter))
ax2.set_yticklabels(directory_labels)
ax2.set_ylim([0-step, height+step])
ax_dup = ax.twiny()
ax_dup.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
ax_dup.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
ax_dup.set_xlim(daterange)

plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
file_name = "ozone_line_observations_inventory_all_sensor.png"
if args.dev:
    file_name = "ozone_line_observations_inventory_all_sensor_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
plt.clf()
plt.close()