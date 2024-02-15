#!/bin/bash
# This script is for running the automated inventory for 
# the past 3 days to get updates for lagged data and plotting
# the new data.

SATINFO_LOC=/home/info/something_here

source ../../obs_inv_utils_pw_cloud.sh

#run inventory 
python3 auto_inventory.py -cat atmosphere -ago 3 -n_jobs 40 -work_dir /lustre/home/work/inventory-work 

#run all plots in parallel
python3 ../plotting/plot_mysql_dir_sensor_sat.py --sidb $SATINFO_LOC -o /inventory_figures &
python3 ../plotting/plot_mysql_sensor.py -o /inventory_figures &
python3 ../plotting/plot_mysql_sensor_sat_amv.py --sidb $SATINFO_LOC -o /inventory_figures &
python3 ../plotting/plot_mysql_sensor_sat_geo.py --sidb $SATINFO_LOC -o /inventory_figures &
python3 ../plotting/plot_mysql_sensor_sat_gps.py --sidb $SATINFO_LOC -o /inventory_figures &
python3 ../plotting/plot_mysql_typ.py -o /inventory_figures 
