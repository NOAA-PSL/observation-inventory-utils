"""
Copyright 2022 NOAA
All rights reserved.

Unit tests for io_utils

"""
import os
import pathlib
import pytest
from datetime import datetime, timedelta
from collections import namedtuple, OrderedDict
import obs_inv_utils
import config_handlers
from config_handlers.obs_search_conf import ObservationsConfig
from obs_inv_utils import time_utils
from obs_inv_utils import search_engine as se
from tests.cmd_outputs import hpss_cmd_helpers as hpss_helpers
from unittest.mock import patch
import subprocess


PYTEST_CALLING_DIR = pathlib.Path(__file__).parent.resolve()
OBS_INV_YAML_CONFIG__VALID = 'obs_inv_config__valid_s3.yaml'

DATA_DIR = 'data'
CONFIGS_DIR = 'configs'
originalPopen = subprocess.Popen

def test_search_engine__init():

    #subprocess.Popen = hpss_helpers.MockPopen
    conf_filepath = os.path.join(
        PYTEST_CALLING_DIR,
        CONFIGS_DIR,
        OBS_INV_YAML_CONFIG__VALID
    )

    obs_conf = ObservationsConfig(conf_filepath)
    obs_conf.load()
    print(f'obs_conf: {obs_conf}')
    inv_search = se.ObsInventorySearchEngine(obs_conf)

    with patch.dict(os.environ, hpss_helpers.SUBPROCESS_COMMUNICATE_HTAR_TVF_SUCCEEDED_GDAS_SATBUFR):
        inv_search.get_obs_file_info()


def test_get_cycle_tag():
    parts = ['gdas','t00Z','sstgrb']
    assert se.get_cycle_tag(parts) == parts[se.CYCLE_TAG]

    parts = ['gdas']
    assert se.get_cycle_tag(parts) == None

    parts = 26
    assert se.get_cycle_tag(parts) == None

    parts = {}
    assert se.get_cycle_tag(parts) == None


def test_get_data_type():
    parts = ['gdas','t00Z','sstgrb']
    assert se.get_data_type(parts) == parts[se.DATA_TYPE]

    parts = ['gdas','t00Z']
    assert se.get_data_type(parts) == None

    parts = 26
    assert se.get_data_type(parts) == None

    parts = {}
    assert se.get_data_type(parts) == None


def test_get_cycle_time():
    cycle_tag = 't00Z'
    assert se.get_cycle_time(cycle_tag) == 0

    cycle_tag = 't06Z'
    assert se.get_cycle_time(cycle_tag) == 6*3600

    cycle_tag = 't12Z'
    assert se.get_cycle_time(cycle_tag) == 12*3600

    cycle_tag = 't18Z'
    assert se.get_cycle_time(cycle_tag) == 18*3600

    cycle_tag = 't26Z'
    assert se.get_cycle_time(cycle_tag) == None

    cycle_tag = {}
    assert se.get_cycle_time(cycle_tag) == None

    cycle_tag = 't-06Z'
    assert se.get_cycle_time(cycle_tag) == None


def test_get_data_format():
    fn = 'gdas.t18z.proflr.tm00.bufr_d.nr'
    assert se.get_data_format(fn) == se.OBS_FORMAT_BUFR_D

    fn = 'gdas.t00z.imssnow96.grib2'
    assert se.get_data_format(fn) == se.OBS_FORMAT_GRIB2

    fn = 'gdas.t00z.nsstbufr'
    assert se.get_data_format(fn) == se.OBS_FORMAT_BUFR

    fn = 'gdas.t12z.engicegrb'
    assert se.get_data_format(fn) == se.OBS_FORMAT_GRB

    fn = 'gdas.t00z.snogrb_t1534.3072.1536'
    assert se.get_data_format(fn) == se.OBS_FORMAT_GRIB2

    fn = 'gdas.t00z.snogrb_t574.1152.576'
    assert se.get_data_format(fn) == se.OBS_FORMAT_GRIB2

    fn = 'gdas.t18z.seaice.5min.blend.grb'
    assert se.get_data_format(fn) == se.OBS_FORMAT_GRB

    fn = 'gdas.t12z.seaice.5min.grb'
    assert se.get_data_format(fn) == se.OBS_FORMAT_GRB

    fn = 'foo.bas'
    assert se.get_data_format(fn) == se.OBS_FORMAT_UNKNOWN

    fn = 'gdas.t12z.prepbufr.acft_profiles.nr'
    assert se.get_data_format(fn) == se.OBS_FORMAT_BUFR

    fn = 'gdas.t12z.prepbufr.nr'
    assert se.get_data_format(fn) == se.OBS_FORMAT_BUFR

    fn = {}
    assert se.get_data_format(fn) == se.OBS_FORMAT_UNKNOWN

    fn = 36
    assert se.get_data_format(fn) == se.OBS_FORMAT_UNKNOWN

    fn = []
    assert se.get_data_format(fn) == se.OBS_FORMAT_UNKNOWN


def test_get_combined_suffix():
    parts = str('gdas.t00z.snogrb_t1534.3072.1536').split('.')
    assert se.get_combined_suffix(parts) == '.3072.1536'

    parts = str('gdas.t18z.adpsfc.tm00.bufr_d.nr').split('.')
    assert se.get_combined_suffix(parts) == '.tm00.bufr_d.nr'

    parts = [26, 48, 6, 392]
    assert se.get_combined_suffix(parts) == None

    parts = {}
    assert se.get_combined_suffix(parts) == None

    parts = str('gdas.t18z.adpsfc').split('.')
    assert se.get_combined_suffix(parts) == None
