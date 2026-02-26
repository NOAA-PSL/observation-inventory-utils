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
parser.add_argument("--sidb", dest='satinfo_db_root', help="root for sat info db files",default='satellites/satinfo/',type=str)
parser.add_argument("-dev", dest='dev', help='Use this flag to add a timestamp to the filename for development', default=False, type=bool)
parser.add_argument("--list", dest="sensor_list", help="List of sensors to include on the plot", type=str, nargs="+")
args = parser.parse_args()

#parameters
satinfo_db_root=args.satinfo_db_root
daterange=[date(2000,1,1), date(2027,1,1)]

def plot_one_line(satinfo, dftmp, yloc):
    f=interpolate.interp1d(satinfo.datetime.to_numpy().astype('float'),
          satinfo.status_nan.to_numpy().astype('float'),
          kind='previous')
    satinfo_tmp = pandas.DataFrame()
    satinfo_tmp['datetime']=pandas.date_range(start='1/1/1900', end='1/1/2050')
    satinfo_tmp['status_nan']=f(satinfo_tmp.datetime.to_numpy().astype('float')).tolist()
    
    plt.plot(satinfo_tmp.datetime, yloc*satinfo_tmp.status_nan,'#1f77b4')
    plt.plot(dftmp.datetime, yloc*dftmp.obs_count.astype('bool'),'|',color='black',markersize=5)
    plt.plot(dftmp.datetime, yloc*dftmp.active,'|',color='#1f77b4',markersize=5)

def select_sensor_satellite_dir_combo(sensor, sat_id, source_dir, db_frame, satinfo):
    dftmp = db_frame.loc[(db_frame['sat_id']==sat_id) & (db_frame['sensor']==sensor) & (db_frame['source_dir']==source_dir)]
    f=interpolate.interp1d(satinfo.datetime.to_numpy().astype('float'),
          satinfo.status_nan.to_numpy().astype('float'),
          kind='previous')
    dftmp['active']=f(dftmp.datetime.to_numpy().astype('float')).tolist()
    dftmp['obs_count_nan']=dftmp.obs_count*dftmp.active
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

def make_sensor_list(sensor_list):
    search_list = []
    for sensor in sensor_list: 
        search_list.append("observations/reanalysis/" + sensor)
    return search_list

#read data from sql database of obs counts
search_list = make_sensor_list(args.sensor_list)
db_frame = utils.get_distinct_bufr_by_sensors(search_list)

db_frame['datetime'] = pandas.to_datetime(db_frame.obs_day)
db_frame['sensor'] = db_frame.apply(get_sensor, axis=1)
db_frame['source_dir'] = db_frame.apply(get_source_dir, axis=1)

db_frame.loc[db_frame['sat_id_name'].isin(['METOP-1', 'METOP-1 (Metop-B']), 'sat_id_name'] = 'METOP-B'
db_frame.loc[db_frame['sat_id_name'].isin(['METOP-2', 'METOP-2 (Metop-A']), 'sat_id_name'] = 'METOP-A'
db_frame.loc[db_frame['sat_id_name'].isin(['METOP-3', 'METOP-3 (Metop-C']), 'sat_id_name'] = 'METOP-C'
db_frame.loc[db_frame['sat_id_name'].isin(['GRACE C (GRACE-F']), 'sat_id_name'] = 'GRACE C'
db_frame.loc[db_frame['sat_id_name'].isin(['GRACE D (GRACE-F']), 'sat_id_name'] = 'GRACE D'

first_datetime = db_frame.groupby(['sensor', 'source_dir', 'sat_id'])['datetime'].min().reset_index()
first_datetime.rename(columns={'datetime': 'first_datetime'}, inplace=True)

df = db_frame[['source_dir', 'sensor', 'sat_id', 'sat_id_name']].value_counts().reset_index(name='count')
df = df.merge(first_datetime, on=['sensor', 'source_dir', 'sat_id'], how='left')

df_sorted = df.sort_values(by=['sensor', 'source_dir', 'first_datetime'], ascending=[False, False, False])

#loop and plot sensors/sat_ids
unique_dir_sensor_sats = df_sorted
step=0.05
height=step*len(unique_dir_sensor_sats)

#make list of sensor&sat labels 
sensor_sat_labels = []
for index, row in unique_dir_sensor_sats.iterrows():
    sensor_name = str(row.sensor)
    if(row.sensor == 'airs'):
        sensor_name = "AIRS"
    if(row.sensor == 'cris'):
        if "crisf4" in row['source_dir']:
            sensor_name = "CrIS-FSR"
        else:
            sensor_name = "CrIS"
    if(row.sensor == 'iasi'):
        sensor_name = 'IASI'

    if row.sat_id_name.strip():
        sensor_sat_labels.append(sensor_name +  " " + str(row.sat_id_name))
    else:
        sensor_sat_labels.append(sensor_name + " " + str(row.sat_id))

print(f"Identified {len(sensor_sat_labels)} unique dir, sensor, sat combos. Generating plot now.")

fig = plt.figure(dpi=300)
fig.patch.set_facecolor('white')
ax = fig.add_axes([0, 0.1, 1, height+step])
plt.title("Inventory of NNJA Atmosphere Sensors by Satellite")
plt.xlabel('Observation Date')
plt.ylabel('Sensor & Satellite')

directory_labels = []
counter=0
for index, row in unique_dir_sensor_sats.iterrows():
    try:
        satinfo_string_ = row['sensor']+"_"+ utils.sat_dictionary[row['sat_id_name']]
        if "crisf4" in row['source_dir']:
            satinfo_string_ = "crisf4_" + utils.sat_dictionary[row['sat_id_name']]
    except KeyError as err:
        print(f'unable to get satinfo string for row: {row}')
        print(f'Error: {err}')
        satinfo_string_ = row['sensor']
    satinfo = utils.read_satinfo_files(satinfo_db_root,satinfo_string_)

    pandas.options.mode.chained_assignment = None
    dftmp = select_sensor_satellite_dir_combo(row['sensor'], row['sat_id'], row['source_dir'], db_frame, satinfo)
    pandas.options.mode.chained_assignment = 'warn'

    dirs = dftmp['source_dir'].unique()
    directory_labels.append(np.array2string(dirs))
    plot_one_line(satinfo, dftmp, step/2+step*counter)
    counter = counter + 1

ax.set_yticks(step/2+step*np.arange(counter))
ax.set_yticklabels(sensor_sat_labels)
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
count = len(sensor_sat_labels)
file_name = f"specified_line_observations_inventory_dir_sensor_sat_{count}.png"
if args.dev:
    file_name = f"specified_line_observations_inventory_dir_sensor_sat_{count}_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
