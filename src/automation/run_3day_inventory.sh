#!/bin/bash
# This script is for running the automated inventory for 
# the past 3 days to get updates for lagged data and plotting
# the new data.

SATINFO_DIR=/home/Jessica.Knezha/obs-inventory/build_gsinfo/satinfo
OUTPUT_LOC=/home/Jessica.Knezha/inventory-figures
WORK_DIR=/lustre/home/work/inventory-work

source ../../obs_inv_utils_pw_cloud.sh

#run inventory 
python3 auto_inventory.py -cat atmosphere -ago 3 -n_jobs 50 -work_dir $WORK_DIR 

#run all plots in parallel
python3 ../plotting/plot_mysql_dir_sensor_sat.py --sidb $SATINFO_DIR -o $OUTPUT_LOC &
python3 ../plotting/plot_mysql_sensor.py -o $OUTPUT_LOC 
python3 ../plotting/plot_mysql_sensor_sat_amv.py --sidb $SATINFO_DIR -o $OUTPUT_LOC &
python3 ../plotting/plot_mysql_sensor_sat_geo.py --sidb $SATINFO_DIR -o $OUTPUT_LOC 
python3 ../plotting/plot_mysql_sensor_sat_gps.py --sidb $SATINFO_DIR -o $OUTPUT_LOC &
python3 ../plotting/plot_mysql_typ.py -o $OUTPUT_LOC 
