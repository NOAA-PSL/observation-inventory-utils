#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas , matplotlib.pyplot as plt
from datetime import datetime, date
import matplotlib.dates as mdates
from IPython.display import display
import os
from scipy import interpolate
import argparse
import glob
import obs_inv_utils.inventory_table_factory as itf
import re

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='out_dir', help="output directory for figures",default='figures',type=str)
parser.add_argument("--sidb", dest='satinfo_db_root', help="root for sat info db files",default='satellites/satinfo/',type=str)
parser.add_argument("-dev", dest='dev', help='Use this flag to add a timestamp to the filename for development', default=False, type=bool)
args = parser.parse_args()

#parameters
satinfo_db_root=args.satinfo_db_root
daterange=[date(1975,1,1), date(2025,1,1)]

sat_dictionary={"NOAA 5": "n05", "NOAA 6": "n06", "NOAA 7": "n07", "NOAA 8": "n08", "NOAA 9": "n09", 
                "NOAA 10":"n10", "NOAA 11":"n11","NOAA 12":"n12","NOAA 13":"n13","NOAA 14":"n14",
               "NOAA 15":"n15","NOAA 16":"n16","NOAA 17":"n17","NOAA 18":"n18","NOAA 19":"n19","NOAA 20":"n20", "NOAA 21":"n21",
               "METOP-1":"metop-b","METOP-2":"metop-a","METOP-3":"metop-c",
               "METOP-1 (Metop-A":"metop-b","METOP-2 (Metop-B":"metop-a","METOP-3 (Metop-C":"metop-c",
               "METOP-1 (Metop-B":"metop-b","METOP-2 (Metop-A":"metop-a",
               "AQUA":"aqua", "NPP":"npp",
               "GOES 7" : "g07", "GOES 8": "g08", "GOES 9": "g09", "GOES 10": "g10","GOES 11": "g11","GOES 12": "g12",
               "GOES 13": "g13", "GOES 14": "g14", "GOES 15": "g15", "GOES 16" : "g16", "GOES 17":"g17",
               "MTSAT-2":"MTSAT-2", "MTSAT-1R":"MTSAT-1R",
               "METEOSAT 2" : "m02", "METEOSAT 3": "m03", "METEOSAT 4": "m04","METEOSAT 5": "m05", "METEOSAT 6": "m06", "METEOSAT 7": "m07",
               "METEOSAT 8": "m08", "METEOSAT 9": "m09", "METEOSAT 10": "m10", "METEOSAT 11": "m11",
               "":"",
               "DMSP 8":"f08", "DMSP 9":"f09", "DMSP 10": "f10", "DMSP 11": "f11", "DMSP 12": "f12", "DMSP 13": "f13", 
               "DMSP 14": "f14", "DMSP 15": "f15","DMSP 16": "f16", "DMSP17": "f17", "DMSP18": "f18",
               "CHAMP":"CHAMP","COSMIC-1":"COSMIC-1","COSMIC-2":"COSMIC-2","COSMIC-3":"COSMIC-3","COSMIC-4":"COSMIC-4",
               "COSMIC-5":"COSMIC-5","COSMIC-6":"COSMIC-6","COSMIC-7":"COSMIC-7",
               "COSMIC-2 E1":"COSMIC-2 E1", "COSMIC-2 E2":"COSMIC-2 E2", "COSMIC-2 E3":"COSMIC-2 E3",
                "COSMIC-2 E4":"COSMIC-2 E4", "COSMIC-2 E5":"COSMIC-2 E5", "COSMIC-2 E6":"COSMIC-2 E6",
               "GRACE A":"GRACE A","GRACE B":"GRACE B","SAC-C":"SAC C","TerraSAR-X":"TerraSAR-X","TERRA":"TERRA",
               "ERS 2":"ERS 2", "GMS 3" : "GMS 3 ","GMS 4":"GMS 4","GMS 5":"GMS 5",
               "INSAT 3A":"INSAT 3A","INSAT 3D":"INSAT 3D","INSAT 3DR":"INSAT 3DR",
               "TIROS-N": "TIROS-N",  "Megha-Tropiques": "meghat",
                "TanDEM-X": "TanDEM-X", "PAZ":"PAZ", "KOMPSAT-5": "KOMPSAT-5",
               "LANDSAT 5":"LANDSAT 5", "GPM-core":"GPM-core", "TRMM":"TRMM",
               "Himawari-8":"himawari8", "Himawari-9":"himawari9"}

satinfo_translate_dictionary={
    "hirs_n06":"hirs2_n06", "hirs_n07":"hirs2_n07", "hirs_n08":"hirs2_n08", "hirs_n09":"hirs2_n09", "hirs_n10":"hirs2_n10",
    "hirs_n11":"hirs2_n11", "hirs_n12":"hirs2_n12", "hirs_n14":"hirs2_n14", "hirs_n15":"hirs3_n15",
    "hirs_n16":"hirs3_n16", "hirs_n17":"hirs3_n17", "hirs_metop-a":"hirs4_metop-a", 
    "hirs_metop-b":"hirs4_metop-b", "hirs_n19":"hirs4_n19", "hirs_tirosn":"hirs2_tirosn", "avhrr_n14":"avhrr2_n14",
    "avhrr_metop-a":"avhrr3_metop-a", "avhrr_metop-b":"avhrr3_metop-b", "avhrr_n15":"avhrr3_n15",
    "avhrr_n16":"avhrr3_n16", "avhrr_n17":"avhrr3_n17", "avhrr_n18":"avhrr3_n18", "avhrr_n19":"avhrr3_n19"
}

#read raw satinfo files
def read_satinfo_files(satinfo_db_root,satinfo_string):
    if satinfo_string in satinfo_translate_dictionary:
            satinfo_string = satinfo_translate_dictionary[satinfo_string]
    satinfo=pandas.DataFrame(columns=['datetime','status','status_nan'])
#    for fn in os.listdir(os.path.join(satinfo_db_root,satinfo_string,'??????????')):
    for fn in glob.glob(os.path.join(satinfo_db_root,satinfo_string,'??????????')):
        pd_tmp = pandas.read_csv(os.path.join(satinfo_db_root,satinfo_string,os.path.basename(fn))
            ,header=None,sep='\s+'
            ,names=['sensor','ch_num','status','error','o1','o2','o3','o4','o5','o6','o7'])
        tmp_frame=pandas.DataFrame([[datetime.strptime(os.path.basename(fn),'%Y%m%d%H'), (pd_tmp['status']>0).any()]]
            ,columns=['datetime','status'])
        satinfo=pandas.concat([satinfo,tmp_frame])
    #if empty make 
    if (satinfo.empty):
      satinfo.loc[len(satinfo.index)] = [date(1900,1,1), False, np.nan]
      satinfo.loc[len(satinfo.index)] = [date(2100,1,1), False, np.nan]
    #convert logical to floats with nans for plotting
    satinfo['status_nan'] = satinfo.status.astype('int')
    satinfo['status_nan'].replace(0, np.nan, inplace=True)
    #make sure the end of the series is in the future
    satinfo.loc[len(satinfo.index)]=[date(2100,1,1), satinfo.status.iat[-1], satinfo.status_nan.iat[-1]]    
    satinfo.datetime = pandas.to_datetime(satinfo.datetime)
    display(satinfo)
    return satinfo


def plot_one_line(satinfo, dftmp, yloc):
    f=interpolate.interp1d(satinfo.datetime.to_numpy().astype('float'),
          satinfo.status_nan.to_numpy().astype('float'),
          kind='previous')
    satinfo_tmp = pandas.DataFrame()
    satinfo_tmp['datetime']=pandas.date_range(start='1/1/1900', end='1/1/2050')
    satinfo_tmp['status_nan']=f(satinfo_tmp.datetime.to_numpy().astype('float')).tolist()
    
    plt.plot(satinfo_tmp.datetime, yloc*satinfo_tmp.status_nan,'b')
    plt.plot(dftmp.datetime, yloc*dftmp.obs_count.astype('bool'),'|',color='black',markersize=5)
    plt.plot(dftmp.datetime, yloc*dftmp.active,'|',color='blue',markersize=5)

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


#read data from sql database of obs counts
print('connecting to mysql db')
mysql_conn = itf.engine.connect()
#BUFR FILE INFO
sql = f"""select m.*, o.parent_dir from obs_meta_nceplibs_bufr as m inner join obs_inventory as o on m.obs_id = o.obs_id"""
data = pandas.read_sql(sql, mysql_conn)
db_frame1 = data.sort_values('inserted_at'
        ).drop_duplicates(['filename', 'obs_day', 'sat_id', 'sat_inst_id'],keep='last')

#PREPBUFR FILE INFO 
sql2 = f"""select m.*, o.parent_dir from obs_meta_nceplibs_prepbufr as m inner join obs_inventory as o on m.obs_id = o.obs_id"""
data2 = pandas.read_sql(sql2, mysql_conn)
db_frame2 = data2.sort_values('inserted_at').drop_duplicates(['filename', 'obs_day', 'variable', 'file_size', 'typ'], keep='last')

print("Data pulled from mysql database")

db_frame = pandas.concat([db_frame1, db_frame2], axis=0, ignore_index=True)

db_frame['datetime'] = pandas.to_datetime(db_frame.obs_day)
db_frame['sensor'] = db_frame.apply(get_sensor, axis=1)
db_frame['source_dir'] = db_frame.apply(get_source_dir, axis=1)

#remove gps, amv, and geo rows to be plotted separately
index_gps = db_frame[(db_frame['sensor']=='gps')].index
db_frame.drop(index_gps, inplace=True)

index_amv = db_frame[(db_frame['sensor']=='amv')].index
db_frame.drop(index_amv, inplace=True)

index_geo = db_frame[(db_frame['sensor']=='geo')].index
db_frame.drop(index_geo, inplace=True)

#loop and plot sensors/sat_ids
unique_dir_sensor_sats = db_frame[['source_dir', 'sensor', 'sat_id', 'sat_id_name']].value_counts().reset_index(name='count').sort_values(by = ['sensor', 'source_dir', 'sat_id_name'], ascending=[False, False, False])
step=0.05
height=step*len(unique_dir_sensor_sats)

#make list of sensor&sat labels 
sensor_sat_labels = []
for index, row in unique_dir_sensor_sats.iterrows():
    source_string = row.source_dir.replace('/', ' ')
    if row.sat_id_name.strip():
        sensor_sat_labels.append(source_string +  " " + str(row.sat_id_name))
    else:
        sensor_sat_labels.append(source_string + " " + str(row.sat_id))

print(f"Identified {len(sensor_sat_labels)} unique dir, sensor, sat combos. Generating plot now.")

fig = plt.figure(dpi=300)
fig.patch.set_facecolor('white')
ax = fig.add_axes([0, 0.1, 1, height+step])
plt.title("Inventory of Clean Bucket Atmosphere Sensors by Satellite")
plt.xlabel('Observation Date')
plt.ylabel('Sensor & Satellite')


directory_labels = []
counter=0
# for index, row in unique_sat_id.iterrows():
for index, row in unique_dir_sensor_sats.iterrows():
    satinfo_string_ = row['sensor']+"_"+sat_dictionary[row['sat_id_name']]
    satinfo = read_satinfo_files(satinfo_db_root,satinfo_string_)

    pandas.options.mode.chained_assignment = None
    dftmp = select_sensor_satellite_dir_combo(row['sensor'], row['sat_id'], row['source_dir'], db_frame, satinfo)
    pandas.options.mode.chained_assignment = 'warn'

    #dirs = dftmp['source_dir'].unique()
    #directory_labels.append(np.array2string(dirs))
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
# ax2 = ax.twinx()
# ax2.set_yticks(step/2+step*np.arange(counter))
# ax2.set_yticklabels(directory_labels)
# ax2.set_ylim([0, height])
ax_dup = ax.twiny()
ax_dup.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
ax_dup.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
ax.set_xlim(daterange)
# sec_ax = ax.secondary_xaxis('top')

plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}', y=-0.01)
file_name = "all_line_observations_inventory_dir_sensor_sat.png"
if args.dev:
    file_name = "all_line_observations_inventory_dir_sensor_sat_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
mysql_conn.close()
