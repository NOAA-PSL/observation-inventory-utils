from collections import namedtuple, OrderedDict
import subprocess
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from obs_inv_utils import inventory_table_factory as tbl_factory

import score_hv

nl = '\n'

ScoreHVCmd = namedtuple(
    'ScoreHVCmd',
    [
        'harvester_command',
        'parse_output',
        'post_parsed_results'
    ],
)

ScoreHVResponse = namedtuple(
    'ScoreHVResponse',
    [
        'response'
    ]
)

@dataclass
class ScoreHVCmdHandler(object):
    harvest_command: str
    cmd_obt: ScoreHVCmd = field(default=ScoreHVCmd, init=False)
    cmd_dict: dict
    hv_response: ScoreHVResponse = field(default=ScoreHVResponse, init=False)
    