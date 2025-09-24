from obs_inv_utils.score_hv_cmd_handler import ScoreHVCmd
from obs_inv_utils import score_hv_cmd_ioda
from obs_inv_utils import score_hv_cmd_wod_nc
from obs_inv_utils import score_hv_cmd_ozone_nc

HV_IODA_META = 'ioda_meta_netcdf'
HV_WOD_NC_META = 'wod_insitu_meta_netcdf'
HV_OZONE_NC_META = 'ozone_meta_netcdf'

score_hv_cmds = {
    HV_IODA_META: ScoreHVCmd(
        HV_IODA_META, 
        score_hv_cmd_ioda.build_harvest_dict,
        score_hv_cmd_ioda.post_harvest_results
    ),
    HV_WOD_NC_META: ScoreHVCmd(
        HV_WOD_NC_META,
        score_hv_cmd_wod_nc.build_harvest_dict,
        score_hv_cmd_wod_nc.post_harvest_results
    ),
    HV_OZONE_NC_META: ScoreHVCmd(
        HV_OZONE_NC_META,
        score_hv_cmd_ozone_nc.build_harvest_dict,
        score_hv_cmd_ozone_nc.post_harvest_results
    )
}