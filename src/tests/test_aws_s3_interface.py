"""
Copyright 2022 NOAA
All rights reserved.

Unit tests for io_utils

"""
import os
import pathlib
import pytest
from obs_inv_utils import aws_s3_interface as s3
from unittest.mock import patch
from obs_inv_utils import config_handler as conf
from datetime import datetime, timedelta
from collections import namedtuple, OrderedDict
from obs_inv_utils import time_utils
from obs_inv_utils import search_engine as se
from tests.cmd_outputs import hpss_cmd_helpers as hpss_helpers
from unittest.mock import patch
import subprocess
VALID_CONFIG_PATH = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'configs'
)

BDP_BUCKET = 'noaa-reanalyses-pds'

VALID_FILE_PATH_FILE_NOT_FOUND = '/foo/bar/abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRTSUVWXYZ-012356.789'
VALID_PREFIX_1 = 'observations/atmos/gefsv13_reanalysis-md5/20190819000000/bufr/'
VALID_FILE_PATH_2 = '/3year/NCEPDEV/GEFSRR/GDAS_OBS/grib/OP_BUFR/2020/gdas.20200120_grib.tar'
VALID_FILE_PATH_3 = '/3year/NCEPDEV/GEFSRR/GDAS_OBS/satbufr/OP_BUFR/2020/gdas.20200120_satbufr.tar'


#def test_send_command__get_s3_obj_list_valid_key():
#    client = s3.get_bdp_s3_client()
#    s3.get_s3_objects_list(client, BDP_BUCKET, VALID_PREFIX_1)
    # s3_command = s3.AwsS3CommandHandler(s3.CMD_GET_S3_OBJ_LIST, args)
    # success = s3_command.send()
    # assert success == True

    #obj_metadata = s3_command.parse_response()
    #assert len(tarball_contents.files) == tarball_contents.expected_count
    #assert tarball_contents.parent_dir == VALID_FILE_PATH_1




PYTEST_CALLING_DIR = pathlib.Path(__file__).parent.resolve()
OBS_INV_YAML_CONFIG__VALID = 'obs_inv_config__valid_s3.yaml'

DATA_DIR = 'data'
CONFIGS_DIR = 'configs'

def test_search_engine__init():

    conf_filepath = os.path.join(
        PYTEST_CALLING_DIR,
        CONFIGS_DIR,
        OBS_INV_YAML_CONFIG__VALID
    )

    obs_conf = conf.ObservationsConfig(conf_filepath)
    obs_conf.load()
    print(f'obs_conf: {obs_conf}')
    client = s3.get_bdp_s3_client()
    inv_search = se.ObsInventorySearchEngine(obs_conf)

    inv_search.get_obs_file_info()
