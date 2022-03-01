from datetime import datetime
import os
from unittest.mock import patch
from obs_inv_utils.hpss_io_interface import HpssCommandRawResponse
from tests.cmd_outputs import hpss_cmd_outputs as hpss_outputs


FILE_NOT_FOUND = 'file_not_found'

SUBPROCESS_POPEN_ERROR_ENV = {
    'SUBPROCESS_ERROR_TYPE': FILE_NOT_FOUND
}

STDOUT_HTAR_FAILED = 'HTAR: HTAR FAILED\n'
STDERR_FILE_NOT_FOUND = '[connecting to hpsscore1.fairmont.rdhpcs.noaa.gov/1217]\nERROR: No such file: /foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789.idx\nERROR: Fatal error opening index file: /foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789.idx\n###WARNING  htar returned non-zero exit status.\n            72 = /apps/hpss/bin/htar -tvf /foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789\n'
RETURN_CODE_FILE_NOT_FOUND = 72

EXPECTED_FILE_NOT_FOUND_RESPONSE = HpssCommandRawResponse(
    'htar -tvf /foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789.idx',
    72,
    STDERR_FILE_NOT_FOUND,
    STDOUT_HTAR_FAILED,
    False,
    '/foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789.idx',
    datetime(2022, 2, 17),
    3.2351    
)

SUBPROCESS_COMMUNICATE_FILE_NOT_FOUND = {
    'SUBPROCESS_COMMUNICATE_STDOUT': STDOUT_HTAR_FAILED,
    'SUBPROCESS_COMMUNICATE_STDERR': STDERR_FILE_NOT_FOUND,
    'SUBPROCESS_COMMUNICATE_RETURNCODE': '72'
}

SUBPROCESS_COMMUNICATE_HTAR_TVF_SUCCEEDED_GDAS_CONVBUFR = {
    'SUBPROCESS_COMMUNICATE_STDOUT': hpss_outputs.STDOUT_HTAR_TVF_SUCCEEDED_GDAS_CONVBUFR,
    'SUBPROCESS_COMMUNICATE_STDERR': hpss_outputs.STDERR_HTAR_TVF_SUCCEEDED,
    'SUBPROCESS_COMMUNICATE_RETURNCODE': '0'
}

SUBPROCESS_COMMUNICATE_HTAR_TVF_SUCCEEDED_GDAS_SATBUFR = {
    'SUBPROCESS_COMMUNICATE_STDOUT': hpss_outputs.STDOUT_HTAR_TVF_SUCCEEDED_GDAS_SATBUFR,
    'SUBPROCESS_COMMUNICATE_STDERR': hpss_outputs.STDERR_HTAR_TVF_SUCCEEDED,
    'SUBPROCESS_COMMUNICATE_RETURNCODE': '0'
}

SUBPROCESS_COMMUNICATE_HTAR_TVF_SUCCEEDED_GDAS_GRIB = {
    'SUBPROCESS_COMMUNICATE_STDOUT': hpss_outputs.STDOUT_HTAR_TVF_SUCCEEDED_GDAS_GRIB,
    'SUBPROCESS_COMMUNICATE_STDERR': hpss_outputs.STDERR_HTAR_TVF_SUCCEEDED,
    'SUBPROCESS_COMMUNICATE_RETURNCODE': '0'
}


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
            stdout = ''
        stderr = os.environ.get('SUBPROCESS_COMMUNICATE_STDERR')
        if stderr is None:
            stderr = ''
        returncode = os.environ.get('SUBPROCESS_COMMUNICATE_RETURNCODE')
        if returncode is not None:
            self.returncode = int(returncode)
        return (stdout.encode('utf-8'),stderr.encode('utf-8'),)

