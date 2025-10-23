#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas , matplotlib.pyplot as plt
from datetime import datetime, date
import matplotlib.dates as mdates
import os
import argparse
import plot_utils as utils
import obs_inv_utils.inventory_table_factory as itf
import re

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='out_dir', help="output directory for figures",default='figures',type=str)
parser.add_argument("-dev", dest='dev', help='Use this flag to add a timestamp to the filename for development', default=False, type=bool)
args = parser.parse_args()

#parameters
daterange=[date(1970,1,1), date(2026,1,1)]

def plot_one_line(dftmp, yloc, color='black'):
    mask = dftmp.var_count.astype('bool')
    plt.plot(dftmp.datetime[mask], yloc*np.ones(mask.sum()),'|',color=color,markersize=5)

def select_sensor_dir(sensor, source_dir, db_frame):
    dftmp = db_frame.loc[(db_frame['sensor']==sensor) & (db_frame['source_dir']==source_dir)]
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

#read data from sql database of obs counts
db_frame = utils.get_ioda_nc()

db_frame['datetime'] = pandas.to_datetime(db_frame.obs_day)
db_frame['sensor'] = db_frame.apply(get_sensor, axis=1)
db_frame['source_dir'] = db_frame.apply(get_source_dir, axis=1)

db_frame = db_frame[db_frame['sensor'].isin(['icec', 'icefb'])]

#loop and plot sensors by directory
unique_sensor_dir = db_frame[['source_dir', 'sensor']].value_counts().reset_index(name='count').sort_values(by = ['sensor', 'source_dir'], ascending=[False, False])
step=0.05
height=step*len(unique_sensor_dir)

#make list of sensor labels
sensor_dir_labels = []
for index, row in unique_sensor_dir.iterrows():
    sensor_dir_labels.append(row.sensor)

fig = plt.figure(dpi=300)
fig.patch.set_facecolor('white')
ax = fig.add_axes([0, 0.1, 1, height+step])
plt.title("Inventory of NNJA Ice IODA files")
plt.xlabel('Observation Date')
plt.ylabel('Sensor')

directory_labels = []
counter=0
for index, row in unique_sensor_dir.iterrows():
    pandas.options.mode.chained_assignment = None
    dftmp = select_sensor_dir(row['sensor'], row['source_dir'], db_frame)
    pandas.options.mode.chained_assignment = 'warn'

    dirs = dftmp['source_dir'].unique()
    directory_labels.append(np.array2string(dirs))
    plot_one_line(dftmp, step/2+step*counter)
    counter = counter + 1

ax.set_yticks(step/2+step*np.arange(counter))
ax.set_yticklabels(sensor_dir_labels)
ax.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
ax.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
ax.set_xlim(daterange)
ax.set_ylim([0, height])
ax.grid(which='major',color='grey', linestyle='-', linewidth=0.5)
ax.grid(which='minor', color='grey', linestyle='--', linewidth=0.2)
ax2 = ax.twinx()
ax2.set_yticks(step/2+step*np.arange(counter))
ax2.set_yticklabels(directory_labels)
ax2.set_ylim([0, height])
ax_dup = ax.twiny()
ax_dup.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
ax_dup.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
ax_dup.set_xlim(daterange)

plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
file_name = "ice_line_observations_inventory_.png"
if args.dev:
    file_name = "ice_line_observations_inventory_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
