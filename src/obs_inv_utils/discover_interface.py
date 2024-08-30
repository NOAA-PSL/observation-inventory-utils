# 2024-04-16
# discover_interface.py
# Seth Cohen

import os
import subprocess
import re
from pathlib import Path
from collections import namedtuple, OrderedDict
import attr
from datetime import datetime

nl = '\n'

DiscoverCommand = namedtuple(
    'DiscoverCommand',
    [
        'command',
        'arg_validator',
        'output_parser'
    ],
)

DiscoverCommandRawResponse = namedtuple(
    'DiscoverCommandRawResponse',
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

DiscoverListContents = namedtuple(
    'DiscoverListContents',
    [
        'prefix',
        'files_count',
        'files_meta',
        'obs_cycle_time',
        'submitted_at',
        'latency'
    ],
)

HpssTarballContents = namedtuple(
    'HpssParsedTarballContents',
    [
        'parent_dir',
        'expected_count',
        'inspected_files',
        'observation_day',
        'submitted_at',
        'latency'
    ],
)



HpssFileMeta = namedtuple(
    'HpssFileMeta',
    [
        'name',
        'permissions',
        'last_modified',
        'size'
    ],
)

DiscoverFileMeta = namedtuple(
    'DiscoverFileMeta',
    [
        'name',
        'permissions',
        'last_modified',
        'size',
        'etag'
    ],
)


CMD_GET_DISCOVER_OBJ_LIST = 'list_discover'
EXPECTED_COMPONENTS_DISCOVER_OBJ_LIST = 8

def inspect_discover_args_valid(args):
    if not isinstance(args, list):
        msg = f'Args must be in the form of a list, args: {args}'
        raise TypeError(msg)
    cmd = discover_cmds[CMD_GET_DISCOVER_OBJ_LIST].command
    print(f'{nl}{nl}In inspect tarball args valid: cmd: {cmd}{nl}{nl}')
    if (len(args) > 1 or len(args) == 0):
        msg = f'Command "{cmd}" accepts exactly 1 argument, received ' \
              f'{len(args)}.'
        raise ValueError(msg)

    arg = args[0]

    try:
        m = re.search(r'[^A-Za-z0-9\._\-\/]', arg)
        if m is not None and m.group(0) is not None:
            print('Only a-z A-Z 0-9 and - . / _ characters allowed in filepath')
            raise ValueError(f'Invalid characters found in file path: {arg}')
    except Exception as e:
        raise ValueError(f'Invalid file path: {e}')

    #return {'bucket': AWS_BDP_BUCKET, 'prefix': args[0]}
    return {'platform':'DISCOVER', 'prefix': args[0]}

    return True

def inspect_discover_parser(response, obs_day):
    print(f' --------- Running inspect_discover_parser -------- ')
    print(f'reponse.output: {response.output}')
    try:
        output = response.output.rsplit('\n')
        print(f' --- output: {output}')
    except Exception as e:
        raise ValueError('Problem parsing response.output. Error: {e}')

    if output[0] == 'total':
        print(f' !!! output[0] equals total. Deleting output[0] before proceeding. !!!')
        del output[0]  
    
    files_meta = list()
    output_line = output[0]
    components = output_line.split()

    parent_dir = os.path.dirname(components[7])
    expected_count = 1
    fn = output[0].split("/")[-1]
    prefix = parent_dir
    obs_cycle_time = fn.split(".")[1:3]
    if len(obs_cycle_time[0]) == 6:
        obs_day = datetime.strptime('.'.join(obs_cycle_time), "%y%m%d.t%Hz")
    if len(obs_cycle_time[0]) == 8:
        obs_day = datetime.strptime('.'.join(obs_cycle_time), "%Y%m%d.t%Hz")
    permissions = '' #components[0]
    size = int(components[4])
    date_str = components[5]
    time_str = components[6]
    etag = ''
    filetime_str = f'{date_str} {time_str}'
    try:
        file_datetime = datetime.strptime(filetime_str, '%Y-%m-%d %H:%M') # '%Y-%m-%dT%H:%M:00Z')
    except Exception as e:
        msg = 'Problem parsing file timestamp: {filetime_str}, error: {e}'
        raise ValueError(msg)
    files_count = 1
    files_meta.append(
        DiscoverFileMeta(fn, permissions, file_datetime, size, etag))
    return DiscoverListContents( 
        prefix, 
        files_count, 
        files_meta,
        obs_day, 
        response.submitted_at,
        response.latency
    )

discover_cmds = {
    'list_discover': DiscoverCommand(
        ['ls', '-l', '--time-style=long-iso'],
        inspect_discover_args_valid,
        inspect_discover_parser,
        
    )
}

def post_discover_cmd_result(raw_response, obs_day):
    if not isinstance(raw_response, DiscoverCommandRawResponse):
        msg = 'raw_response must be of type DiscoverCommandRawResponse. It is'\
              f' actually of type: {type(raw_response)}'
        raise TypeError(msg)

    cmd_result_data = tbl_factory.CmdResultData(
        raw_response.command,
        raw_response.args_0,
        raw_response.output,
        raw_response.error,
        raw_response.return_code,
        obs_day,
        raw_response.submitted_at,
        raw_response.latency,
        datetime.utcnow()
    )

    print(f'Discover cmd_result: {cmd_result_data}')
    cmd_result_id = tbl_factory.insert_cmd_result(cmd_result_data)

    return cmd_result_id



def is_valid_discover_cmd(instance, attribute, value):
    print(f'In is_valid_discover_cmd: value: {value}')
    if value not in discover_cmds:
        msg = f'Discover command {value} is not valid. Use one of: ' \
              f'{discover_cmds.keys()}'
        raise KeyError(msg)
    return True

@attr.s(slots=True)
class DiscoverCommandHandler(object):

    command = attr.ib(validator=is_valid_discover_cmd)
    args = attr.ib(default=attr.Factory(list))
    cmd_obj = attr.ib(init=False)
    cmd_line = attr.ib(init=False)
    raw_resp = attr.ib(default=None)
    submitted_at = attr.ib(default=None)
    finished_at = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.cmd_obj = discover_cmds[self.command]
        print(f'In __attrs_post_init__: self.args: {self.args}')
        if self.cmd_obj.arg_validator(self.args):
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
                  f'Try loading the hpss module.  $ module load hpss'
            raise FileNotFoundError(msg)
        except Exception as e:
            msg = f'Error after sending command {cmd_str}, error: {e}.'
            raise ValueError(msg)

        cmd_str = ''
        for cmd in self.cmd_obj.command:
            cmd_str += f'{cmd} '
        
        self.raw_resp = DiscoverCommandRawResponse(
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


    def parse_response(self, obs_day):
        if self.raw_resp is not None:
            return self.cmd_obj.output_parser(self.raw_resp, obs_day)
        else:
            return None


