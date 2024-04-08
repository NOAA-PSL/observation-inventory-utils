#!/bin/bash
# This script is for running the automated inventory for 
# the past 3 days to get updates for lagged data and plotting
# the new data.

SATINFO_DIR=/home/$USER/obs-inventory/build_gsinfo/satinfo
OUTPUT_LOC=/home/$USER/inventory-figures
WORK_DIR=/lustre/home/work/inventory-work

source ../../obs_inv_utils_pw_cloud.sh

#run inventory 
python3 auto_inventory.py -cat list -n_jobs 40 -work_dir $WORK_DIR --list airs_airsev airs_aqua amsua_1bamua amsua_nasa_aqua amsua_nasa_r21c \
    amsub_1bamub amv_satwnd atms_atms avhrr_avcsam avhrr_avcspm cris_cris cris_crisf4 geo_geoimr \
    geo_goesfv geo_goesnd geo_gsrasr geo_gsrcsr gmi_nasa_gmiv7 gps_eumetsat gps_gpsro hirs_1bhrs3 hirs_1bhrs4 \
    iasi_mtiasi mhs_1bmhs ozone_nasa_sbuv_v87 ozone_ncep_gome ozone_ncep_omi ozone_ncep_ompslp \
    ozone_ncep_ompsn8 ozone_ncep_ompst8 saphir_saphir seviri_sevcsr ssmi_eumetsat \
    ssmi_ssmit ssmis_ssmisu trmm_nasa_tmi &
python3 auto_inventory.py -cat list -n_jobs 8 -ago 8400 -end 20020101T000000 -work_dir $WORK_DIR --list ssu_1bssu ozone_cfsr msu_1bmsu hirs_1bhrs2 \
    conv_prepbufr_acft_profiles amv_merged conv_prepbufr ssmi_eumetsat & 
python3 auto_inventory.py -cat list -n_jobs 8 -ago 8400 -work_dir $WORK_DIR --list ssu_1bssu ozone_cfsr msu_1bmsu hirs_1bhrs2 \
    conv_prepbufr_acft_profiles amv_merged conv_prepbufr ssmi_eumetsat    

#run all plots in parallel
python3 ../plotting/plot_mysql_dir_sensor_sat.py --sidb $SATINFO_DIR -o $OUTPUT_LOC &
python3 ../plotting/plot_mysql_sensor.py -o $OUTPUT_LOC &
python3 ../plotting/plot_mysql_sensor_sat_amv.py --sidb $SATINFO_DIR -o $OUTPUT_LOC &
python3 ../plotting/plot_mysql_sensor_sat_geo.py --sidb $SATINFO_DIR -o $OUTPUT_LOC &
python3 ../plotting/plot_mysql_sensor_sat_gps.py --sidb $SATINFO_DIR -o $OUTPUT_LOC &
python3 ../plotting/plot_mysql_typ.py -o $OUTPUT_LOC 