import re
import attr
from collections import namedtuple, OrderedDict
import subprocess
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from obs_inv_utils import inventory_table_factory as tbl_factory

nl = '\n'

SubprocessCmd = namedtuple(
    'SubprocessCmd',
    [
        'command',
        'validate_args',
        'parse_output',
        'post_parsed_results'
    ],
)

CmdRawResponse = namedtuple(
    'CmdRawResponse',
    [
        'command',
        'return_code',
        'error',
        'output',
        'success',
        'args_0',
        'submitted_at',
        'latency'
    ],
)


def is_valid_subprocess_cmd(value, subprocess_cmds):
    print(f'In is_valid_hpss_cmd: value: {value}')
    if subprocess_cmds.get(value) is None:
        msg = f'subprocess command {value} is not valid. Use one of: ' \
              f'{subprocess_cmds.keys()}'
        raise KeyError(msg)
    return True


@dataclass
class SubprocessCmdHandler(object):
    command: str
    subprocess_cmds: dict 
    args: list
    cmd_obj: SubprocessCmd = field(default=SubprocessCmd, init=False)
    cmd_line: str = field(default=str, init=False)
    raw_resp: CmdRawResponse = field(default=CmdRawResponse, init=False)
    submitted_at: datetime = field(default=datetime, init=False)
    finished_at: datetime = field(default=datetime, init=False)
    cmd_id: int = field(default=int, init=False)

    def __post_init__(self):
        self.cmd_obj = self.subprocess_cmds[self.command]
        print(f'In __post_init__: self.args: {self.args}')
        print(f'In __post_init__: self.cmd_obj: {self.cmd_obj}')
        if self.cmd_obj.validate_args(self.args):
            self.cmd_line = getattr(self.cmd_obj,'command').copy()
            for arg in self.args:
                self.cmd_line.append(arg)
        print(f'cmd_line: {self.cmd_line}, args: {self.args}')


    def send(self):
        cmd_str = self.cmd_obj.command[0]

        proc = subprocess.Popen(
            self.cmd_line,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        try:
            self.submitted_at = datetime.utcnow()
            out, err = proc.communicate()
            self.finished_at = datetime.utcnow()
            print(f'return_code: {proc.returncode}, out: {out}, err: {err}')
        except FileNotFoundError as e:
            msg = f'Command: {cmd_str} was not recognized. '\
                  f'error: {e}{nl}{nl}' \
                  f'Try adding the command executable location to PATH.'
            raise FileNotFoundError(msg)
        except Exception as e:
            msg = f'Error after sending command {cmd_str}, error: {e}.'
            raise ValueError(msg)

        cmd_str = ''
        for cmd in self.cmd_obj.command:
            cmd_str += f'{cmd} '
        self.raw_resp = CmdRawResponse(
            cmd_str,
            proc.returncode,
            err.decode('utf-8'),
            out.decode('utf-8'),
            (proc.returncode == 0),
            self.args[0],
            self.submitted_at,
            float(self.get_cmd_duration())
        )

        print(f'raw_resp: {self.raw_resp}')
        
        if proc.returncode != 0:
            return False
        else:
            return True


    def can_retry_send(self):
        # for now, we'll just send false for the retry until we
        # know what kind of erors we see back.
        return False


    def get_raw_response(self):
        return self.raw_resp


    def get_cmd_duration(self):
        diff = self.finished_at - self.submitted_at
        return (diff.seconds + diff.microseconds/1000000)


    def parse_output(self, context):
        if self.raw_resp is not None:
            return self.cmd_obj.parse_output(self.raw_resp.output, context)
        else:
            return None


    def post_cmd_result(self, obs_datetime):
        cmd_result_data = tbl_factory.CmdResultData(
            self.raw_resp.command,
            self.raw_resp.args_0,
            self.raw_resp.output,
            self.raw_resp.error,
            self.raw_resp.return_code,
            obs_datetime,
            self.raw_resp.submitted_at,
            self.raw_resp.latency,
            datetime.utcnow()
        )

        self.cmd_id = tbl_factory.insert_cmd_result(cmd_result_data)
        print(f'In subproc, cmd result id: {self.cmd_id}')


    def post_parsed_result(self, parsed_data, context):
        return self.cmd_obj.post_parsed_results(self.cmd_id, parsed_data, context)
