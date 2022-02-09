"""
Copyright 2022 NOAA
All rights reserved.

Unit tests for io_utils

"""
import os
import pathlib
import pytest
from obs_inv_utils import config_handler as conf
from datetime import datetime, timedelta
from collections import namedtuple, OrderedDict
from obs_inv_utils import time_utils
from obs_inv_utils import search_engine


PYTEST_CALLING_DIR = pathlib.Path(__file__).parent.resolve()
OBS_INV_YAML_CONFIG__VALID = 'obs_inv_config__valid.yaml'

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
    se = search_engine.ObsInventorySearchEngine(obs_conf)

    se.get_obs_file_info()
