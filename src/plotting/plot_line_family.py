#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import sqlite3, pandas , matplotlib.pyplot as plt
from datetime import datetime, date
import matplotlib.dates as mdates
from IPython.display import display
import os
from scipy import interpolate
import argparse
import glob

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='out_dir', help="output directory for figures",default='figures',type=str)
parser.add_argument("-d", dest='root_dir', help="directory with observations_inventory.db",type=str)
parser.add_argument("-n", dest='obs_stream', help="obs stream name",default='1bamua',type=str)
parser.add_argument("-s", dest='sensor_name', help="sensor name",default='amsua',type=str)
parser.add_argument("--sidb", dest='satinfo_db_root', help="root for sat info db files",default='satellites/satinfo/',type=str)
args = parser.parse_args()

#parameters
#obs_stream='1bamua'
#sensor_name='amsua'
#satinfo_db_root='satellites/'
obs_stream=args.obs_stream
sensor_name=args.sensor_name
satinfo_db_root=args.satinfo_db_root
daterange=[date(1990,1,1), date(2022,1,1)]

sat_dictionary={"NOAA 10":"n10","NOAA 11":"n11","NOAA 12":"n12","NOAA 13":"n13","NOAA 14":"n14",
               "NOAA 15":"n15","NOAA 16":"n16","NOAA 17":"n17","NOAA 18":"n18","NOAA 19":"n19","NOAA 20":"n20",
               "METOP-1":"metop-b","METOP-2":"metop-a","METOP-3":"metop-c",
               "METOP-1 (Metop-A":"metop-b","METOP-2 (Metop-B":"metop-a","METOP-3 (Metop-C":"metop-c",
               "METOP-1 (Metop-B":"metop-b","METOP-2 (Metop-A":"metop-a",
               "AQUA":"aqua", "NPP":"npp",
               "GOES 8": "g08", "GOES 9": "g09", "GOES 10": "g10","GOES 11": "g11","GOES 12": "g12",
               "GOES 13": "g13", "GOES 14": "g14", "GOES 15": "g15",
               "MTSAT-2":"MTSAT-2",
               "METEOSAT 5": "m05", "METEOSAT 6": "m06", "METEOSAT 7": "m7","MTSAT-1R":"MTSAT-1R",
               "METEOSAT 8": "m08", "METEOSAT 9": "m09", "METEOSAT 10": "m10", "METEOSAT 11": "m11",
               "":"",
               "DMSP 10": "f10", "DMSP 11": "f11", "DMSP 12": "f12", "DMSP 13": "f13", "DMSP 14": "f14", "DMSP 15": "f15",
               "DMSP 16": "f16", "DMSP17": "f17", "DMSP18": "f18",
               "CHAMP":"CHAMP","COSMIC-1":"COSMIC-1","COSMIC-2":"COSMIC-2","COSMIC-3":"COSMIC-3","COSMIC-4":"COSMIC-4",
               "COSMIC-5":"COSMIC-5","COSMIC-6":"COSMIC-6","COSMIC-7":"COSMIC-7",
               "GRACE A":"GRACE A","GRACE B":"GRACE B","SAC-C":"SAC C","TerraSAR-X":"TerraSAR-X","TERRA":"TERRA",
               "ERS 2":"ERS 2","GMS 4":"GMS 4","GMS 5":"GMS 5","INSAT 3A":"INSAT 3A","INSAT 3D":"INSAT 3D"}


#read raw satinfo files
def read_satinfo_files(satinfo_db_root,satinfo_string):
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
    plt.plot(dftmp.datetime, yloc*dftmp.obs_count.astype('bool'),'s',color='gray',markersize=5)
    plt.plot(dftmp.datetime, yloc*dftmp.active,'s',color='blue',markersize=5)

def select_sensor_satelite_combo(sat_id, db_frame, satinfo):
    dftmp = db_frame.loc[db_frame['sat_id']==sat_id]
    f=interpolate.interp1d(satinfo.datetime.to_numpy().astype('float'),
          satinfo.status_nan.to_numpy().astype('float'),
          kind='previous')
    dftmp['active']=f(dftmp.datetime.to_numpy().astype('float')).tolist()
    dftmp['obs_count_nan']=dftmp.obs_count*dftmp.active
    return dftmp


#read data from sql database of obs counts
fnin=os.path.join(args.root_dir,"observations_inventory.db")
print(f"opeinign db file {fnin}")
conn = sqlite3.connect(fnin)
sql = f"""select * from obs_meta_nceplibs_bufr where filename like '%{obs_stream}%' """
data = pandas.read_sql(sql, conn)
db_frame = data.sort_values('inserted_at'
        ).drop_duplicates(['filename', 'obs_day', 'sat_id', 'sat_inst_id'],keep='last')
db_frame['datetime'] = pandas.to_datetime(db_frame.obs_day)

#loop and plot satelites
unique_sat_id = db_frame.sort_values('sat_id_name').drop_duplicates('sat_id')
step=0.05
height=step*len(unique_sat_id)

#make list of sat labels
sat_labels=[]
for index, row in unique_sat_id.iterrows():
  if row.sat_id_name.strip():
    sat_labels.append(row.sat_id_name)
  else:
    sat_labels.append(row.sat_id)

fig = plt.figure(dpi=300)
fig.patch.set_facecolor('white')
ax = fig.add_axes([0, 0.1, 1, height+step])
plt.title(f"{sensor_name} sensor from obs stream {obs_stream}")
plt.xlabel('Observation Date')

counter=0
for index, row in unique_sat_id.iterrows():
    satinfo_string_ = sensor_name+"_"+sat_dictionary[row['sat_id_name']]
    satinfo = read_satinfo_files(satinfo_db_root,satinfo_string_)

    pandas.options.mode.chained_assignment = None
    dftmp = select_sensor_satelite_combo(row['sat_id'], db_frame, satinfo)
    pandas.options.mode.chained_assignment = 'warn'
    
    l=len(dftmp)
    sid=row['sat_id']
    print(f"{satinfo_string_} sat_id = {sid} dftmp len={l}")
    #display(satinfo)

    plot_one_line(satinfo, dftmp, step/2+step*counter)
    counter = counter + 1

ax.set_yticks(step/2+step*np.arange(counter))
#ax.set_yticklabels(unique_sat_id.sat_id_name)
ax.set_yticklabels(sat_labels)
ax.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
ax.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
ax.set_xlim(daterange)
ax.set_ylim([0, height])
ax.grid(which='major',color='grey', linestyle='-', linewidth=0.5)
ax.grid(which='minor', color='grey', linestyle='--', linewidth=0.2)
#ax.yaxis.grid(False)

fnout=os.path.join(args.out_dir,f"{obs_stream}_line_observations_inventory.png")
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')

