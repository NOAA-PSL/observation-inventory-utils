from obs_inv_utils.score_hv_cmd_handler import ScoreHVCmd
from obs_inv_utils import score_hv_cmd_ioda

HV_IODA_META = 'ioda_meta_netcdf'

score_hv_cmds = {
    HV_IODA_META: ScoreHVCmd(
        HV_IODA_META, 
        score_hv_cmd_ioda.build_harvest_dict,
        score_hv_cmd_ioda.post_harvest_results
    )
}