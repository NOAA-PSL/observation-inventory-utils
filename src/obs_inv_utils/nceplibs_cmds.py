from collections import namedtuple

from obs_inv_utils import nceplibs_cmd_sinv as ncep_sinv
from obs_inv_utils.subprocess_cmd_handler import SubprocessCmd


NCEPLIBS_SINV = 'sinv'

nceplibs_cmds = {
    'sinv': SubprocessCmd(
        ['sinv'],
        ncep_sinv.validate_args,
        ncep_sinv.parse_output,
        ncep_sinv.post_obs_meta_data
    )
}

