"""
Copyright 2022 NOAA
All rights reserved.

Unit tests for io_utils

"""
import os
import pathlib
import pytest
from obs_inv_utils import config_handler as conf
from datetime import datetime
from collections import namedtuple, OrderedDict
from obs_inv_utils import time_utils

PYTEST_CALLING_DIR = pathlib.Path(__file__).parent.resolve()
DATA_DIR = 'data'
CONFIGS_DIR = 'configs'


DEFAULT_FN = os.path.join(
        PYTEST_CALLING_DIR,
        'data',
        'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789'
)

DEFAULT_ACCESS = 0o0777

DEFAULT_CONTENTS = 'Hello World!!'

OBS_INV_YAML_CONFIG__VALID = 'obs_inv_config__valid.yaml'
OBS_INV_YAML_CONFIG__INVALID_DATE_RANGE = 'obs_inv_config__missing_date_range.yaml'
OBS_INV_YAML_CONFIG__INVALID_START_OLDER_THAN_END = 'obs_inv_config__start_newer_than_end.yaml'

TEST_GOOD_DATETIME = '20190101T000000Z'
TEST_GOOD_DATETIME_END = '20190103T000000Z'
TEST_GOOD_DATE_FORMAT_STR = '%Y%m%dT%H%M%SZ'
TEST_INVALID_DATETIME = 'foo'
TEST_INVALID_DATE_FORMAT_STR = 'bar'
TEST_DEFAULT_OBS_CYCLE_INTERVALS = [0, 21600, 43200, 64800]

DEFAULT_START_TIME = datetime(year=1990, month=1, day=1)
DEFAULT_END_TIME = datetime.utcnow()
DEFAULT_DATE_STR = '%Y%m%dT%H%M%SZ'

DEFAULT_DATE_RANGE = {
    'datestr': DEFAULT_DATE_STR,
    'end': DEFAULT_END_TIME,
    'start': DEFAULT_START_TIME
}

OBS_CONFIGS_HASH = [
    "hera_hpss-/3year/NCEPDEV/GEFSRR/GDAS_OBS/convbufr.nr/OP_BUFR/%Y/gdas.%Y%m%d_convbufr.nr.tar",
    "hera_hpss-/3year/NCEPDEV/GEFSRR/GDAS_OBS/grib/OP_BUFR/%Y/gdas.%Y%m%d_grib.tar",
    "hera_hpss-/3year/NCEPDEV/GEFSRR/GDAS_OBS/satbufr/OP_BUFR/%Y/gdas.%Y%m%d_satbufr.tar"
]


def create_dummy_file(
    filepath=DEFAULT_FN,
    access=DEFAULT_ACCESS,
    contents=DEFAULT_CONTENTS
):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filepath, 'w') as fp:
        if contents is not None and isinstance(contents, str):
            fp.write(contents)
        pass
    print(f'Creating dummy file: {filepath}')

    try:
        os.chmod(filepath, access)
    except Exception as e:
        raise ValueError(f'Problem setting access permissions "{access}"')

    status = os.stat(filepath)
    permissions = oct(status.st_mode)[-3:]
    print(f'File: {filepath}, permissions: {permissions}')


def test_file_exists_validator__no_file():
    """
    Test the 'file_exists' validator with non existant file
    """
    file = '\0fake_file.yaml'

    with pytest.raises(ValueError):
        obs_conf = conf.ObservationsConfig(file)


def test_file_exists_validator__invalid_filename():
    """
    Test the 'file_exists' validator with non existant file
    """
    file = {}
    print(f'testing file_exists validator with: {file}')
    with pytest.raises(ValueError):
        obs_conf = conf.ObservationsConfig(file)

    file = []
    print(f'testing file_exists validator with: {file}')
    with pytest.raises(ValueError):
        obs_conf = conf.ObservationsConfig(file)

    file = 'rm -rf'
    print(f'testing file_exists validator with: {file}')
    with pytest.raises(ValueError):
        obs_conf = conf.ObservationsConfig(file)

    file = 6
    print(f'testing file_exists validator with: {file}')
    with pytest.raises(ValueError):
        obs_conf = conf.ObservationsConfig(file)


def test_file_exists_validator__valid_filename_and_exists():
    """
    Test the 'file_exists' validator with non existant file
    """
    file = 'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789'
    filepath = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'data',
        file
    )

    create_dummy_file()

    obs_conf = conf.ObservationsConfig(filepath)
    assert obs_conf.config_yaml == filepath

    os.remove(filepath)


def test_file_exists_validator__zero_bytes():
    """
    Test the 'file_exists' validator with 0 bytes file
    """
    file = 'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789'
    filepath = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'data',
        file
    )

    create_dummy_file(contents={})

    with pytest.raises(ValueError):
        obs_conf = conf.ObservationsConfig(filepath)

    os.remove(filepath)


def test_file_exists_validator__no_read_access():
    """
    Test the 'file_exists' validator with file with no read access
    """
    file = 'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789'
    filepath = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'data',
        file
    )

    create_dummy_file(access=0o0200)

    # change permissions of file to write only
    with pytest.raises(ValueError):
        obs_conf = conf.ObservationsConfig(filepath)

    os.remove(filepath)


def test_set_datetime__invalid_date_or_format_str():

    test_datetime = datetime.strptime(TEST_GOOD_DATETIME, TEST_GOOD_DATE_FORMAT_STR)
    assert time_utils.set_datetime(
        TEST_GOOD_DATETIME, TEST_GOOD_DATE_FORMAT_STR) == test_datetime
    
    assert time_utils.set_datetime(
        TEST_GOOD_DATETIME, TEST_INVALID_DATE_FORMAT_STR) is None

    assert time_utils.set_datetime(
        TEST_INVALID_DATETIME, TEST_GOOD_DATE_FORMAT_STR) is None



def test_set_datetime__invalid_format_str():
    assert time_utils.set_datetime('foo', 'bar') is None


def test_get_obs_inv_search_configs__invalid_date_range():
    """
    Test the 'get_hpss_obs_inv_configs' validator with file that contains
    filepaths and invalid datetime range (invalid datetime strings)
    """
    conf_filepath = os.path.join(
        PYTEST_CALLING_DIR,
        CONFIGS_DIR,
        OBS_INV_YAML_CONFIG__INVALID_DATE_RANGE
    )

    obs_conf = conf.ObservationsConfig(conf_filepath)
    with pytest.raises(ValueError):
        obs_conf.load()


def test_get_obs_inv_search_configs__invalid_start_older_than_end():
    """
    Test the 'get_hpss_obs_inv_configs' validator with file that contains
    filepaths and invalid datetime range (start newer than end)
    """
    conf_filepath = os.path.join(
        PYTEST_CALLING_DIR,
        CONFIGS_DIR,
        OBS_INV_YAML_CONFIG__INVALID_START_OLDER_THAN_END
    )

    obs_conf = conf.ObservationsConfig(conf_filepath)
    with pytest.raises(ValueError):
        obs_conf.load()


def test_get_obs_inv_search_configs__good_config():
    conf_filepath = os.path.join(
        PYTEST_CALLING_DIR,
        CONFIGS_DIR,
        OBS_INV_YAML_CONFIG__VALID
    )

    obs_conf = conf.ObservationsConfig(conf_filepath)
    try:
        obs_conf.load()
    except Exception as e:
        raise ValueError(f'Unexpected error encountered: {e}')

    obs_search_configs = obs_conf.get_obs_inv_search_configs()
    
    assert len(obs_search_configs) == len(OBS_CONFIGS_HASH)
    for config_hash, config in obs_search_configs.items():
        assert (config_hash in OBS_CONFIGS_HASH) 
        assert config.get_date_range().start == datetime.strptime(TEST_GOOD_DATETIME, TEST_GOOD_DATE_FORMAT_STR)
        assert config.get_date_range().end == datetime.strptime(TEST_GOOD_DATETIME_END, TEST_GOOD_DATE_FORMAT_STR)
        assert config.get_cycle_intervals() == time_utils.DEFAULT_OBS_CYCLE_INTERVALS
               
        print(f'config_hash {config_hash}, start: {config.get_date_range().start}')
