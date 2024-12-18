from collections import namedtuple, OrderedDict
import subprocess
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from obs_inv_utils import inventory_table_factory as tbl_factory

from score_hv.harvester_base import harvest 

nl = '\n'

ScoreHVCmd = namedtuple(
    'ScoreHVCmd',
    [
        'harvester_command',
        'build_harvest_dict', 
        'post_harvest_results'
    ],
)

CmdRawResponse = namedtuple(
    'CmdRawResponse',
    [
        'command',
        'arg0',
        'output',
        'error',
        'error_code',
        'submitted_at',
        'latency'
    ],
)

@dataclass
class ScoreHVCmdHandler(object):
    command: str
    hv_cmds: dict
    args: dict
    cmd_obj: ScoreHVCmd = field(default=ScoreHVCmd, init=False)
    harvest_dict: dict = field(default=dict, init=False)
    hv_response: dict = field(default=dict, init=False)
    raw_resp: CmdRawResponse = field(default=CmdRawResponse, init=False)
    submitted_at: datetime = field(default=datetime, init=False)
    finished_at: datetime = field(default=datetime, init=False)
    cmd_id: int = field(default=int, init=False)

    def __post_init__(self):
        self.cmd_obj = self.hv_cmds[self.command]
        self.build_harvest_dict()

    def harvest(self):
        try:
            self.submitted_at = datetime.now(datetime.timezone.utc)
            self.hv_response = harvest(self.harvest_dict)
            self.finished_at = datetime.now(datetime.timezone.utc)
        except Exception as e:
            msg = f'Error harvesting using dict {self.harvest_dict}, error: {e}'
            raise ValueError(msg)
        
        self.raw_resp = CmdRawResponse(
            self.cmd_obj.harvester_command,
            self.harvest_dict,
            self.hv_response,
            '',
            0,
            self.submitted_at,
            float(self.get_cmd_duration())
        )

    def build_harvest_dict(self):
        self.harvest_dict = self.cmd_obj.build_harvest_dict(self.command, self.args)
            
    def get_cmd_duration(self):
        diff = self.finished_at - self.submitted_at
        return (diff.seconds + diff.microseconds/1000000)

    def post_cmd_result(self, obs_datetime):
        cmd_result_data = tbl_factory.CmdResultData(
            self.raw_resp.command,
            self.raw_resp.arg0,
            self.raw_resp.output,
            self.raw_resp.error,
            self.raw_resp.error_code,
            obs_datetime,
            self.raw_resp.submitted_at,
            self.raw_resp.latency,
            datetime.now(datetime.timezone.utc)
        )

        self.cmd_id = tbl_factory.insert_cmd_result(cmd_result_data)

    def post_harvest_results(self, context):
        return self.cmd_obj.post_harvest_results(self.cmd_id, self.hv_response, context)