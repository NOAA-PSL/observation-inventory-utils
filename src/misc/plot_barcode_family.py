#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import sqlite3, pandas , matplotlib.pyplot as plt
from datetime import datetime, date
import matplotlib.dates as mdates
#from IPython.display import display
import os
from scipy import interpolate
import argparse
import glob

#argparse section
parser = argparse.ArgumentParser()
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
               "METOP-1":"metop-a","METOP-2":"metop-b","METOP-3":"metop-c",
               "METOP-1 (Metop-A":"metop-a","METOP-2 (Metop-B":"metop-b","METOP-3 (Metop-C":"metop-c"}


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
    #convert logical to floats with nans for plotting
    satinfo['status_nan'] = satinfo.status.astype('int')
    satinfo['status_nan'].replace(0, np.nan, inplace=True)
    #make sure the end of the series is in the future
    satinfo.loc[len(satinfo.index)]=[date(2100,1,1), satinfo.status.iat[-1], satinfo.status_nan.iat[-1]]    
    satinfo.datetime = pandas.to_datetime(satinfo.datetime)
    return satinfo


def plot_one_barcode(ax, satinfo, dftmp, daterange, sat_name_to_plot):
    pixel_per_bar = 1
    dpi = 100

    f=interpolate.interp1d(satinfo.datetime.to_numpy().astype('float'),
          satinfo.status_nan.to_numpy().astype('float'),
          kind='previous')
    satinfo_tmp = pandas.DataFrame()
    satinfo_tmp['datetime']=pandas.date_range(start='1/1/1900', end='1/1/2050')
    satinfo_tmp['status_nan']=f(satinfo_tmp.datetime.to_numpy().astype('float')).tolist()
    plt.plot(satinfo_tmp.datetime, 0.5*satinfo_tmp.status_nan,'m')

    extent=mdates.date2num(min(pandas.to_datetime(dftmp.obs_day))), mdates.date2num(max(pandas.to_datetime(dftmp.obs_day))),0, 1
    barcode = ax.imshow(dftmp.obs_count.to_numpy().reshape(1,-1), cmap='binary', aspect='auto',
              interpolation='nearest',extent=extent)
    barcode2 = ax.imshow(dftmp.obs_count_nan.to_numpy().reshape(1,-1), cmap='Blues', aspect='auto',
              interpolation='nearest',extent=extent)

    #ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
    ax.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
    ax.set_xlim(daterange)
    ax.grid(which='major',color='grey', linestyle='-', linewidth=0.5)
    ax.grid(which='minor', color='grey', linestyle='--', linewidth=0.2)
    ax.set_yticks([.5],labels=[sat_name_to_plot])
    ax.yaxis.grid(False)
    #fig.autofmt_xdate()


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
fig = plt.figure(dpi=300)
fig.patch.set_facecolor('white')
fig.suptitle('Observation Date', y=0)
counter=0
step=1/(len(unique_sat_id))
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
    
    ax = fig.add_axes([0, counter*step+step, 1, step])
    plot_one_barcode(ax, satinfo, dftmp, daterange, row['sat_id_name'])
    if counter>0: ax.set_xticklabels([])
    counter = counter + 1

ax.set_title(f"{sensor_name} sensor from obs stream {obs_stream}", y=1)
fnout=os.path.join(args.root_dir,"observations_inventory.png")
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')

