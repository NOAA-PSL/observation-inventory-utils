#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas , matplotlib.pyplot as plt
from datetime import datetime, date
import matplotlib.dates as mdates
import os
import argparse
import obs_inv_utils.inventory_table_factory as itf

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='out_dir', help="output directory for figures",default='figures',type=str)
args = parser.parse_args()

#parameters
daterange=[date(1975,1,1), date(2024,1,1)]

typ_dictionary = {
    111:"SYNDAT (110)", 112:"n/a (112)", 120:"ADPUPA (120)", 122:"ADPUPA (122)", 126:"RASSDA (126)", 130:"AIRCFT (130)", 
    131:"AIRCFT (131)", 132:"ADPUPA (132)", 133:"AIRCAR (133)", 134:"AIRCFT (134)", 135:"AIRCFT (135)", 150: "SPSSMI (150)",
    151:"GOESND (151)", 152:"SPSSMI (152)", 153:"GPSIPW (153)", 156:"GOESND (156)", 157:"GOESND (157)", 158:"GOESND (158)", 
    159:"GOESND (159)", 164:"GOESND (164)", 165:"GOESND (165)", 174:"GOESND (174)", 175:"GOESND (175)", 180:"SFCSHP (180)", 
    181:"ADPSFC (181)", 182:"SFCSHP (182)", 183:"ADPSFC,SFCSHP (183)", 187:"ADPSFC (187)", 188:"MSONET (188)", 191:"SFCBOG (191)",
    192:"ADPSFC (192)", 193:"ADPSFC (193)", 194:"SFCSHP (194)", 195:"MSONET (195)", 210:"SYNDAT (210)", 220:"ADPUPA (220)", 
    221:"ADPUPA (221)", 222:"ADPUPA (222)", 223:"PROFLR (223)", 224:"VADWND (224)", 227:"PROFLR (227)", 228:"PROFLR (228)",
    229:"PROFLR (229)", 230:"AIRCFT (230)", 231:"AIRCFT (231)", 232:"ADPUPA (232)", 233:"AIRCAR (233)", 234:"AIRCFT (234)",
    235:"AIRCFT (235)", 240:"SATWND (240)", 241:"SATWND (241)", 242:"SATWND (242)", 243:"SATWND (243)", 244:"SATWND (244)",
    245:"SATWND (245)", 246:"SATWND (246)", 247:"SATWND (247)", 248:"SATWND (248)", 249:"SATWND (249)", 250:"SATWND (250)",
    251:"SATWND (251)", 252:"SATWND (252)", 253:"SATWND (253)", 254:"SATWND (254)", 255:"SATWND (255)", 256:"SATWND (256)",
    257:"SATWND (257)", 258:"SATWND (258)", 259:"SATWND (259)", 260:"SATWND (260)", 270:"(270)", 271:"(271)",
    280:"SFCSHP (280)", 281:"ADPSFC (281)", 282:"SFCSHP (282)", 283:"SPSSMI (283)", 284:"ADPSFC,SFCSHP (284)", 
    285:"QKSWND (285)", 286:"ERS1DA (286)", 287:"ADPSFC (287)", 288:"MSONET (288)", 289:"WDSATR (289)", 
    290:"ASCATW (290)", 291:"(291)", 292:"ADPSFC (292)", 293:"ADPSFC (293)", 294:"SFCSHP (294)", 295:"MSONET (295)"
}

def plot_one_line(dftmp, yloc):
    plt.plot(dftmp.datetime, yloc*dftmp.tot.astype('bool'),'s',color='gray',markersize=5)

def select_variable(variable, db_frame):
    dftmp = db_frame.loc[db_frame['variable']==variable]
    return dftmp

def get_sensor(row):
    directory = row['parent_dir']
    sensor = directory.split("/")[2]
    return sensor


#read data from sql database of obs counts
print('connecting to mysql db')
mysql_conn = itf.engine.connect()
#BUFR FILE INFO
# sql = f"""select m.*, o.parent_dir from obs_meta_nceplibs_bufr as m inner join obs_inventory as o on m.obs_id = o.obs_id"""
# data = pandas.read_sql(sql, mysql_conn)
# db_frame1 = data.sort_values('inserted_at'
#         ).drop_duplicates(['filename', 'obs_day', 'sat_id', 'sat_inst_id'],keep='last')

#PREPBUFR FILE INFO 
sql2 = f"""select m.*, o.parent_dir from obs_meta_nceplibs_prepbufr_aggregate as m inner join obs_inventory as o on m.obs_id = o.obs_id"""
data2 = pandas.read_sql(sql2, mysql_conn)
db_frame = data2.sort_values('inserted_at').drop_duplicates(['filename', 'obs_day', 'variable', 'tot', 'file_size'], keep='last')

# db_frame = pandas.concat([db_frame1, db_frame2], axis=0, ignore_index=True)

db_frame['datetime'] = pandas.to_datetime(db_frame.obs_day)
db_frame['sensor'] = db_frame.apply(get_sensor, axis=1)

#loop and plot typ
unique_var = db_frame.sort_values('variable', ascending=False).drop_duplicates('variable')
step=0.05
height=step*len(unique_var)

#make list of typ labels
var_labels = []
for index, row in unique_var.iterrows():
    var_labels.append(row.variable)

fig = plt.figure(dpi=300)
fig.patch.set_facecolor('white')
ax = fig.add_axes([0, 0.1, 1, height+step])
plt.title("Inventory of Clean Bucket Conventional Variables by Time")
plt.xlabel('Observation Date')
plt.ylabel('Variable')

counter=0
# for index, row in unique_sat_id.iterrows():
for index, row in unique_var.iterrows():
    pandas.options.mode.chained_assignment = None
    dftmp = select_variable(row['variable'], db_frame)
    pandas.options.mode.chained_assignment = 'warn'

    plot_one_line(dftmp, step/2+step*counter)
    counter = counter + 1

ax.set_yticks(step/2+step*np.arange(counter))
ax.set_yticklabels(var_labels)
ax.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
ax.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
ax.set_xlim(daterange)
ax.set_ylim([0, height])
ax.grid(which='major',color='grey', linestyle='-', linewidth=0.5)
ax.grid(which='minor', color='grey', linestyle='--', linewidth=0.2)

file_name = "all_line_observations_inventory_variable_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')
mysql_conn.close()
