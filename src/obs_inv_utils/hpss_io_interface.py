import attr
import os
import re
from collections import namedtuple, OrderedDict
import subprocess
from datetime import datetime

nl = '\n'

HpssCommand = namedtuple(
    'HpssCommand',
    [
        'command',
        'arg_validator',
        'output_parser'
    ],
)

HpssCommandRawResponse = namedtuple(
    'HpssCommandRawResponse',
    [
        'command',
        'return_code',
        'error',
        'output',
        'success'
    ],
)


HpssFileInfo = namedtuple(
    'HpssFileInfo',
    [
        'name',
        'permissions',
        'time',
        'size'
    ],
)


HpssTarballContents = namedtuple(
    'HpssParsedTarballContents',
    [
        'parent_dir',
        'expected_count',
        'files'
    ],
)

EXPECTED_COMPONENTS_HTAR_TVF_FILE_OBJ = 7
CMD_INSPECT_TARBALL = 'inspect_tarball'

def inspect_tarball_args_valid(args):
    if not isinstance(args, list):
        msg = f'Args must be in the form of a list, args: {args}'
        raise TypeError(msg)
    cmd = hpss_cmds[CMD_INSPECT_TARBALL].command
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

    return True


def hpss_inspect_tarball_parser(response):
    if not isinstance(response, HpssCommandRawResponse):
        msg = f'Response needs to be an instance type HpssCommandRawResponse.'\
              f'Received type: {type(response)}'
        raise TypeError(msg)

    try:
        output = response.output.rsplit('\n')
    except Exception as e:
        raise ValueError('Problem parsing response.output. Error: {e}')

    expected_count = 0
    parent_dir = ''
    files = []
    for output_line in output:
        print(f'out_line: {output_line}')
        components = output_line.split()
        if len(components) < EXPECTED_COMPONENTS_HTAR_TVF_FILE_OBJ:
            continue
        if components[1] == 'Listing':
            parent_dir = components[4].replace(',','')
            expected_count = int(components[5])
            continue

        permissions = components[1]
        size = int(components[3])
        date_str = components[4]
        time_str = components[5]
        filetime_str = f'{date_str}T{time_str}:00Z'
        try:
            file_datetime = datetime.strptime(filetime_str, '%Y-%m-%dT%H:%M:00Z')
        except Exception as e:
            msg = 'Problem parsing file timestamp: {filetime_str}, error: {e}'
            raise ValueError(msg)

        fn = components[6]
        files.append(
            HpssFileInfo(fn, permissions, file_datetime, size))

    return HpssTarballContents(parent_dir, expected_count, files)


hpss_cmds = {
    'inspect_tarball': HpssCommand(
        ['htar', '-tvf'],
        inspect_tarball_args_valid,
        hpss_inspect_tarball_parser,
    )
}


def is_valid_hpss_cmd(instance, attribute, value):
    print(f'In is_valid_hpss_cmd: value: {value}')
    if value not in hpss_cmds:
        msg = f'HPSS command {value} is not valid. Use one of: ' \
              f'{hpss_cmds.keys()}'
        raise KeyError(msg)
    return True


@attr.s(slots=True)
class HpssCommandHandler(object):

    command = attr.ib(validator=is_valid_hpss_cmd)
    args = attr.ib(default=attr.Factory(list))
    hpss_cmd_obj = attr.ib(init=False)
    hpss_cmd_line = attr.ib(init=False)
    raw_resp = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.hpss_cmd_obj = hpss_cmds[self.command]
        print(f'In __attrs_post_init__: self.args: {self.args}')
        if self.hpss_cmd_obj.arg_validator(self.args):
            self.hpss_cmd_line = getattr(self.hpss_cmd_obj,'command').copy()
            for arg in self.args:
                self.hpss_cmd_line.append(arg)
        print(f'hpss_cmd_line: {self.hpss_cmd_line}, args: {self.args}')


    def send(self):
        cmd_str = self.hpss_cmd_obj.command[0]

        proc = subprocess.Popen(
            self.hpss_cmd_line,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        try:
            out, err = proc.communicate()
            print(f'return_code: {proc.returncode}, out: {out}, err: {err}')
        except FileNotFoundError as e:
            msg = f'Command: {cmd_str} was not recognized. '\
                  f'error: {e}{nl}{nl}' \
                  f'Try loading the hpss module.  $ module load hpss'
            raise FileNotFoundError(msg)
        except Exception as e:
            msg = f'Error after sending command {cmd_str}, error: {e}.'
            raise ValueError(msg)

        self.raw_resp = HpssCommandRawResponse(
            self.hpss_cmd_line,
            proc.returncode,
            err.decode('utf-8'),
            out.decode('utf-8'),
            (proc.returncode == 0)
        )

        print(f'raw_resp: {self.raw_resp}')
        
        if proc.returncode != 0:
            return False
        else:
            return True


    def get_raw_response(self):
        return self.raw_resp


    def parse_response(self):
        if self.raw_resp is not None:
            return self.hpss_cmd_obj.output_parser(self.raw_resp)
        else:
            return None
