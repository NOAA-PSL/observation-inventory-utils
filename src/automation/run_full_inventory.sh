#!/bin/bash
# This script is for running the automated inventory for 
# the full period of each variable to get updates for added data

SATINFO_DIR=/contrib/$USER/home/obs-inventory/build_gsinfo/satinfo
OZINFO_DIR=/contrib/$USER/home/obs-inventory/build_gsinfo/ozinfo
OUTPUT_LOC=/contrib/$USER/home/inventory-figures
WORK_DIR=/lustre/home/work/inventory-work

cd $(dirname $0)

source ../../obs_inv_utils_pw_inv_cluster.sh

#run inventory 
python3 auto_inventory.py -cat list -n_jobs 80 -work_dir $WORK_DIR --list airs_airsev airs_aqua amsua_1bamua amsua_nasa_aqua amsua_nasa_r21c \
    amsub_1bamub amv_satwnd atms_atms avhrr_avcsam avhrr_avcspm cris_cris cris_crisf4 geo_ahicsr geo_geoimr \
    geo_goesfv geo_goesnd geo_gsrasr geo_gsrcsr gmi_nasa_gmiv7 gps_gpsro hirs_1bhrs3 hirs_1bhrs4 \
    iasi_mtiasi mhs_1bmhs ozone_nasa_sbuv_v87 ozone_ncep_gome ozone_ncep_mls ozone_ncep_omi ozone_ncep_ompslp \
    ozone_ncep_ompsn8 ozone_ncep_ompst8 saphir_saphir seviri_sevasr seviri_sevcsr \
    ssmi_ssmit ssmis_ssmisu trmm_nasa_tmi amsr2_nasa amsre_nasa avhrr_avcspm_n16 \
    conv_convbufr_adpsfc conv_convbufr_adpupa conv_convbufr_aircar conv_convbufr_aircft conv_convbufr_ascatt \
    conv_convbufr_ascatw conv_convbufr_hdob conv_convbufr_proflr conv_convbufr_rassda conv_convbufr_vadwnd &
python3 auto_inventory.py -cat list -n_jobs 8 -ago 8400 -end 20020101T000000Z -work_dir $WORK_DIR --list ssu_1bssu ozone_cfsr msu_1bmsu hirs_1bhrs2 \
    conv_prepbufr_acft_profiles conv_prepbufr & 
python3 auto_inventory.py -cat list -n_jobs 8 -ago 8400 -work_dir $WORK_DIR --list ssu_1bssu ozone_cfsr msu_1bmsu hirs_1bhrs2 \
    conv_prepbufr_acft_profiles conv_prepbufr   

#run all plots in parallel
python3 ../plotting/plot_mysql_dir_sensor_sat.py --sidb $SATINFO_DIR -o $OUTPUT_LOC
python3 ../plotting/plot_mysql_sensor.py -o $OUTPUT_LOC 
python3 ../plotting/plot_mysql_sensor_sat_amv.py --sidb $SATINFO_DIR -o $OUTPUT_LOC
python3 ../plotting/plot_mysql_sensor_sat_geo.py --sidb $SATINFO_DIR -o $OUTPUT_LOC 
python3 ../plotting/plot_mysql_sensor_sat_gps.py --sidb $SATINFO_DIR -o $OUTPUT_LOC
python3 ../plotting/plot_mysql_sensor_sat_ozone.py --sidb $OZINFO_DIR -o $OUTPUT_LOC
python3 ../plotting/plot_mysql_typ.py -o $OUTPUT_LOC 