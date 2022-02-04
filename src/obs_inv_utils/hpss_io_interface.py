import attr
import os
import re
from collections import namedtuple, OrderedDict
import subprocess

nl = '\n'

HpssCommand = namedtuple(
    'HpssCommand',
    [
        'command',
        'arg_validator',
        'output_handler',
        'error_handler'
    ],
)

HpssCommandResponse = namedtuple(
    'HpssCommandResponse',
    [
        'command',
        'return_code',
        'error_msg',
        'output_msg',
        'success'
    ],
)


def inspect_tarball_args_valid(args):
    if not isinstance(args, list):
        msg = f'Args must be in the form of a list, args: {args}'
        raise TypeError(msg)
    cmd = hpss_cmds['INSPECT_TARBALL'].command
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


def hpss_htar_error_handler(return_code, cmd, out, err):
    print(f'{nl}{nl}In hpss_htar_error_handler, cmd: {cmd}, return_code: {return_code}{nl}{nl}')
    print(f'In hpss_htar_error_handler, error: {err}, output: {out}')
    # we might want to handle errors in a specific way here or repackage
    # the output depending on our needs
    if not isinstance(out, list):
        raise ValueError('Expecting command output to be a list: out: {out}')
    return HpssCommandResponse(
        cmd,
        return_code,
        err,
        out[0],
        False
    )


def hpss_htar_output_handler(return_code, cmd, out, err):
    print(f'cmd: {cmd}, return_code: {return_code}')
    print(f'error: {err}, output: {out}')
    return HpssCommandResponse(
        cmd,
        return_code,
        err,
        out,
        True
    )


hpss_cmds = {
    'INSPECT_TARBALL': HpssCommand(
        ['htar', '-tvf'],
        inspect_tarball_args_valid,
        hpss_htar_output_handler,
        hpss_htar_error_handler
    )
}

print(f'in hpss_command_handler: hpss_cmds: {hpss_cmds}')


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

        err_decoded = err.decode('utf-8').rsplit('\n')
        out_decoded = out.decode('utf-8').rsplit('\n')
        for line in out_decoded:
            print(f'output line: {line}')

        for line in err_decoded:
            print(f'error line: {line}')

        if proc.returncode != 0:
            return self.hpss_cmd_obj.error_handler(
                proc.returncode, self.hpss_cmd_line, out_decoded, err_decoded)

        return self.hpss_cmd_obj.output_handler(
            proc.returncode, self.hpss_cmd_line, out_decoded, err_decoded)
