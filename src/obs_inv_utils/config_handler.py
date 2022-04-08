import attr
from copy import deepcopy
import os
from datetime import datetime, timedelta
from pathlib import Path
import re
from obs_inv_utils import yaml_utils
from obs_inv_utils import obs_storage_platforms
from obs_inv_utils import time_utils
from obs_inv_utils.time_utils import DateRange

SEARCH_PATH_KEY = 'key'

def is_valid_readable_file(instance, attribute, value):
    """
    Method to ensure that the filename/path is valid, exists, contains data,
    and the user has sufficient permissions to read it.
    """
    # look for invalid characters in filename/path
    try:
        m = re.search(r'[^A-Za-z0-9\._\-\/]', value)
        if m is not None and m.group(0) is not None:
            print('Only a-z A-Z 0-9 and - . / _ characters allowed in filepath')
            raise ValueError(f'Invalid characters found in file path: {value}')
    except Exception as e:
        raise ValueError(f'Invalid file path: {e}')
    try:
        path = Path(value)
        if not path.is_file():
            raise ValueError(f'Path: {value} does not exist')
    except Exception as e:
        raise ValueError(f'Invalid file path: {e}')

    # check permissions on file
    status = os.stat(value, follow_symlinks=True)
    print(f'status.st_size: {status.st_size}')
    if status.st_size == 0:
        print(f'if block caught 0 byte file {status}')
        raise ValueError(f'Invalid file. File {value} is empty.')

    permissions = oct(status.st_mode)[-3:]
    readAccess = os.access(value, os.R_OK)
    if readAccess is False:
        raise ValueError(
            f'Insufficient permissions on file "{value}" - {permissions}.'
        )


def is_valid_storage_platform(instance, attribute, value):
    if not obs_storage_platforms.is_valid(value):
        msg = f'Invalid platform: {value}, must be one of ' \
              f'[{obs_storage_platforms.PLATFORMS}].'
        raise ValueError(msg)

    return True


@attr.s(slots=True)
class ObsSearchConfig(object):
    """
    Class responsible for creating an observation search config.
    """

    storage_platform = attr.ib(validator=is_valid_storage_platform)
    search_config = attr.ib()
    date_range = attr.ib(default=None)
    cycle_intervals = attr.ib(init=False)


    def __attrs_post_init__(self):
        self.cycle_intervals = time_utils.DEFAULT_OBS_CYCLE_INTERVALS
        if not isinstance(self.date_range, DateRange):
            self.date_range = DateRange()

    def get_storage_platform(self):
        return self.storage_platform


    def get_date_range(self):
        return self.date_range


    def get_cycle_intervals(self):
        return self.cycle_intervals


    def get_current_search_path(self):
        current = self.date_range.current
        path = time_utils.get_datetime_str(
            current, self.search_config.get(SEARCH_PATH_KEY)
        )
        print(f'path: {path}')
        return path

@attr.s(slots=True)
class ObservationsConfig(object):
    """
    Class responsible for loading in the observations inventory search
    configuration.
    """

    config_yaml = attr.ib(validator=is_valid_readable_file)
    obs_search_configs = attr.ib(default=attr.Factory(dict))
    search_date_range = attr.ib(default=None)


    def load(self):
        
        config_data = yaml_utils.YamlLoader(self.config_yaml)
        self.parse_obs_inv_search_configs(config_data)
        print(f'config_data: {config_data}')


    def parse_obs_inv_search_configs(self, config_data):
        obs_search_yaml_data = config_data.load()

        obs_search_configs = config_data.get_value(
            key='search_info',
            document=obs_search_yaml_data,
            return_type=list
        )

        config_date_range = config_data.get_value(
            key='date_range',
            document=obs_search_yaml_data,
            return_type=dict
        )

        self.search_date_range = time_utils.get_date_range_from_dict(
            config_date_range)

        print(f'search_date_range: {self.search_date_range}')

        try:
            for obs_search_config in obs_search_configs:
                print(f'obs_search_config: {obs_search_config}')

                storage_platform = config_data.get_value(
                    key='platform',
                    document=obs_search_config,
                    return_type=str
                )
                
                date_range = DateRange(
                    self.search_date_range.start,
                    self.search_date_range.end
                )

                obs_search_config_obj = ObsSearchConfig(
                    storage_platform,
                    obs_search_config,
                    date_range
                )
                search_key = obs_search_config['key']
                hash_key = f'{storage_platform}-{search_key}'
                print(f'hash_key: {hash_key}')
                self.obs_search_configs[hash_key] = obs_search_config_obj

        except Exception as e:
            msg = f'Problem loading config data: {e}'
            raise ValueError(msg)

        return self.obs_search_configs


    def get_obs_inv_search_configs(self):
        return self.obs_search_configs


    def get_search_date_range(self):
        return self.search_date_range
