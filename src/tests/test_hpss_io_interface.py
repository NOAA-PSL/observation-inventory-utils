"""
Copyright 2022 NOAA
All rights reserved.

Unit tests for io_utils

"""
import os
import pathlib
import pytest
from obs_inv_utils import hpss_io_interface as hpss
import subprocess
from unittest.mock import patch


VALID_CONFIG_PATH = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'configs'
)

VALID_FILE_PATH_FILE_NOT_FOUND = '/foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789'
VALID_FILE_PATH = '/3year/NCEPDEV/GEFSRR/GDAS_OBS/convbufr.nr/OP_BUFR/2020/gdas.20200120_convbufr.nr.tar'


CMD_INSPECT_TARBALL = 'INSPECT_TARBALL'


FILE_NOT_FOUND = 'file_not_found'

SUBPROCESS_POPEN_ERROR_ENV = {
    'SUBPROCESS_ERROR_TYPE': FILE_NOT_FOUND
}

STDOUT_FILE_NOT_FOUND = 'HTAR: HTAR FAILED\n'
STDERR_FILE_NOT_FOUND = '[connecting to hpsscore1.fairmont.rdhpcs.noaa.gov/1217]\nERROR: No such file: /foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789.idx\nERROR: Fatal error opening index file: /foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789.idx\n###WARNING  htar returned non-zero exit status.\n            72 = /apps/hpss/bin/htar -tvf /foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789\n'

SUBPROCESS_COMMUNICATE_FILE_NOT_FOUND = {
    'SUBPROCESS_COMMUNICATE_STDOUT': STDOUT_FILE_NOT_FOUND,
    'SUBPROCESS_COMMUNICATE_STDERR': STDERR_FILE_NOT_FOUND,
    'SUBPROCESS_COMMUNICATE_RETURNCODE': '72'
}


def test_is_valid_hpss_cmd__invalid_cmd():
    hpss_command = None
    with pytest.raises(KeyError):
        hpss_command  = hpss.HpssCommandHandler(
            'foo', ['foo', 'bar'])


def test_inspect_tarball_args_valid__invalid_instance_type():
    """
    Test the 'inspect_tarball_args_valid' validator with 
    various invalid instance types.
    """
    hpss_command = None
    with pytest.raises(ValueError):
        hpss_command  = hpss.HpssCommandHandler(
            CMD_INSPECT_TARBALL, ['foo', 'bar'])

    hpss_command = None
    with pytest.raises(TypeError):
        hpss_command  = hpss.HpssCommandHandler(
            CMD_INSPECT_TARBALL, {})

    hpss_command = None
    with pytest.raises(TypeError):
        hpss_command  = hpss.HpssCommandHandler(
            CMD_INSPECT_TARBALL, 5)

    hpss_command = None
    with pytest.raises(TypeError):
        hpss_command  = hpss.HpssCommandHandler(
            CMD_INSPECT_TARBALL, 'foo')


def test_inspect_tarball_args_valid__invalid_file_path():
    hpss_command = None
    with pytest.raises(ValueError):
        hpss_command = hpss.HpssCommandHandler(
            CMD_INSPECT_TARBALL, ['foo bar'])

    hpss_command = None
    with pytest.raises(ValueError):
        hpss_command = hpss.HpssCommandHandler(
            CMD_INSPECT_TARBALL, ['foo-bar$%#@!&*()][[]\''])


def test_inspect_tarball_args_valid__valid_file_path():
    hpss_command = None
    try:
        args = []
        args.append(VALID_FILE_PATH)
        hpss_command = hpss.HpssCommandHandler(
            CMD_INSPECT_TARBALL, args
        )
    except Exception as e:
        msg = f'Unexpected exception encountered when registering command: {e}'
        assert False, msg


class MockPopen(object):
    def __init__(self, args, stdout=None, stderr=None, returncode=None):
        self.args = args
        print(f'In subprocess mock, received args: {args}')
        self.stdout = None
        self.stderr = None
        self.returncode = 0
        if os.environ.get('SUBPROCESS_ERROR_TYPE') == FILE_NOT_FOUND:
            msg = '[Errno 2] No such file or directory: "htar"'
            raise FileNotFoundError(msg)


    def communicate(self):
        print(f'In MockOpen: stdout: {self.stdout}')
        stdout = os.environ.get('SUBPROCESS_COMMUNICATE_STDOUT')
        if stdout is None:
            stdout = b''
        stderr = os.environ.get('SUBPROCESS_COMMUNICATE_STDERR')
        if stderr is None:
            stderr = b''
        returncode = os.environ.get('SUBPROCESS_COMMUNICATE_RETURNCODE')
        if returncode is not None:
            self.returncode = int(returncode)
        return (stdout.encode('utf-8'),stderr.encode('utf-8'),)
    

def test_send_command__hpss_module_not_loaded():
    hpss_command = None
    args = []
    args.append(VALID_FILE_PATH)

    with patch.dict(os.environ, SUBPROCESS_POPEN_ERROR_ENV):
        # subprocess.Popen = MockPopen
        with pytest.raises(FileNotFoundError):
            hpss_command  = hpss.HpssCommandHandler(
                CMD_INSPECT_TARBALL, args)

            hpss_command.send()


def test_send_command__htar_tvf_file_not_found():
    hpss_command = None
    args = []
    args.append(VALID_FILE_PATH_FILE_NOT_FOUND)
    expected_output = 'HTAR: HTAR FAILED'
    with patch.dict(os.environ, SUBPROCESS_COMMUNICATE_FILE_NOT_FOUND):
        # subprocess.Popen = MockPopen
        try:
            hpss_command = hpss.HpssCommandHandler(
                CMD_INSPECT_TARBALL, args)
            response = hpss_command.send()
            assert response.output_msg == expected_output
        except Exception as e:
            msg = f'Unexpected exception encountered when registering command: {e}'
            assert False, msg

    print(f'Response: {response}')


def test_send_command__htar_tvf_valid_file():
    hpss_command = None
    args = []
    args.append(VALID_FILE_PATH)
    hpss_command = hpss.HpssCommandHandler(
        CMD_INSPECT_TARBALL, args)
    response = hpss_command.send()
    print(f'Response: {response}')
