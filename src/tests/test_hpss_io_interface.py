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
from obs_inv_utils.hpss_io_interface import HpssCommandRawResponse
from tests.cmd_outputs import hpss_cmd_outputs as hpss_outputs
from tests.cmd_outputs import hpss_cmd_helpers as hpss_helpers

VALID_CONFIG_PATH = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'configs'
)

VALID_FILE_PATH_FILE_NOT_FOUND = '/foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789'
VALID_FILE_PATH_1 = '/3year/NCEPDEV/GEFSRR/GDAS_OBS/convbufr.nr/OP_BUFR/2020/gdas.20200120_convbufr.nr.tar'
VALID_FILE_PATH_2 = '/3year/NCEPDEV/GEFSRR/GDAS_OBS/grib/OP_BUFR/2020/gdas.20200120_grib.tar'
VALID_FILE_PATH_3 = '/3year/NCEPDEV/GEFSRR/GDAS_OBS/satbufr/OP_BUFR/2020/gdas.20200120_satbufr.tar'



CMD_INSPECT_TARBALL = hpss.CMD_INSPECT_TARBALL

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
        args.append(VALID_FILE_PATH_1)
        hpss_command = hpss.HpssCommandHandler(
            CMD_INSPECT_TARBALL, args
        )
    except Exception as e:
        msg = f'Unexpected exception encountered when registering command: {e}'
        assert False, msg


def test_send_command__hpss_module_not_loaded():
    hpss_command = None
    args = []
    args.append(VALID_FILE_PATH_1)

    with patch.dict(os.environ, hpss_helpers.SUBPROCESS_POPEN_ERROR_ENV):
        subprocess.Popen = hpss_helpers.MockPopen
        with pytest.raises(FileNotFoundError):
            hpss_command  = hpss.HpssCommandHandler(
                CMD_INSPECT_TARBALL, args)

            hpss_command.send()


def test_send_command__htar_tvf_file_not_found():
    hpss_command = None
    args = []
    args.append(VALID_FILE_PATH_FILE_NOT_FOUND)
    expected_output = hpss_helpers.STDOUT_HTAR_FAILED
    with patch.dict(os.environ, hpss_helpers.SUBPROCESS_COMMUNICATE_FILE_NOT_FOUND):
        subprocess.Popen = hpss_helpers.MockPopen
        try:
            hpss_command = hpss.HpssCommandHandler(
                CMD_INSPECT_TARBALL, args)
            success = hpss_command.send()
        except Exception as e:
            msg = f'Unexpected exception encountered when registering command: {e}'
            assert False, msg

        assert success == False

        raw_resp = hpss_command.get_raw_response()
        assert raw_resp.return_code == hpss_helpers.RETURN_CODE_FILE_NOT_FOUND

        print(f'raw_resp.error: {raw_resp.error}')
        print(f'raw_resp.output: {raw_resp.output}')
        assert raw_resp.output == expected_output


def test_send_command__htar_tvf_valid_filepath_1():
    hpss_command = None
    args = []
    args.append(VALID_FILE_PATH_1)
    with patch.dict(os.environ, hpss_helpers.SUBPROCESS_COMMUNICATE_HTAR_TVF_SUCCEEDED_GDAS_CONVBUFR):
        hpss_command = hpss.HpssCommandHandler(CMD_INSPECT_TARBALL, args)
        success = hpss_command.send()
        assert success == True

        tarball_contents = hpss_command.parse_response()
        assert len(tarball_contents.files) == tarball_contents.expected_count
        assert tarball_contents.parent_dir == VALID_FILE_PATH_1


def test_send_command__htar_tvf_valid_filepath_2():
    hpss_command = None
    args = []
    args.append(VALID_FILE_PATH_2)
    with patch.dict(os.environ, hpss_helpers.SUBPROCESS_COMMUNICATE_HTAR_TVF_SUCCEEDED_GDAS_GRIB):
        hpss_command = hpss.HpssCommandHandler(CMD_INSPECT_TARBALL, args)
        success = hpss_command.send()
        assert success == True

        tarball_contents = hpss_command.parse_response()
        assert len(tarball_contents.files) == tarball_contents.expected_count
        assert tarball_contents.parent_dir == VALID_FILE_PATH_2


def test_send_command__htar_tvf_valid_filepath_3():
    hpss_command = None
    args = []
    args.append(VALID_FILE_PATH_3)
    with patch.dict(os.environ, hpss_helpers.SUBPROCESS_COMMUNICATE_HTAR_TVF_SUCCEEDED_GDAS_SATBUFR):
        hpss_command = hpss.HpssCommandHandler(CMD_INSPECT_TARBALL, args)
        success = hpss_command.send()
        assert success == True

        tarball_contents = hpss_command.parse_response()
        assert len(tarball_contents.files) == tarball_contents.expected_count
        assert tarball_contents.parent_dir == VALID_FILE_PATH_3
