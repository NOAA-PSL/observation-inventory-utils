rdir='/contrib/Jessica.Knezha/home/obs-inventory/observation-inventory-utils'

cd ${rdir}/
source ${rdir}/obs_inv_utils_pw_cloud.sh
cd -

#--inventory file size
python3 ${rdir}/src/obs_inv_utils/obs_inv_cli.py get-obs-inventory -c obs_inv_config_1bmsu.yaml

python3 ${rdir}/src/obs_inv_utils/obs_inv_cli.py get-obs-count-meta-sinv -c obs_meta_sinv_1bmsu.yaml

#--plot inventory
#python3 ${rdir}/src/obs_inv_utils/obs_inv_cli.py plot-groups-filesize-timeseries -c plot_config__data_type_groupings.yaml

#python3 ${rdir}/src/obs_inv_utils/obs_inv_cli.py plot-files-filesize-vs-time -m 1


