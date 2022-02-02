import attr
import os
from datetime import datetime, timedelta
from pathlib import Path
import re
from obs_inv_utils import yaml_utils
from obs_inv_utils import obs_storage_platforms

DEFAULT_START_TIME = datetime(year=1990, month=1, day=1)
DEFAULT_END_TIME = datetime.utcnow()
DEFAULT_DATE_STR = '%Y%m%dT%H%M%SZ'
DEFAULT_OBS_CYCLE_INTERVALS = [0, 21600, 43200, 64800]

DEFAULT_DATE_RANGE_CONFIG = {
    'datestr': DEFAULT_DATE_STR,
    'end': DEFAULT_END_TIME,
    'start': DEFAULT_START_TIME
}


def get_datetime_str(value, format_str):
    try:
        formatted_datetime =  datetime.strptime(value, format_str)
    except Exception as e:
        msg = f'Invalid time: {value} or format_str: {format_str}' \
              f', error: {e}'
        raise ValueError(msg) 

    return formatted_datetime


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
    
    return True


def set_datetime(time_str, format_str):
    try:
        time = datetime.strptime(time_str, format_str)
    except Exception as e:
        print(f'Invalid time str: {time_str} or format string: {format_str}. {e}')
        return None

    return time


# def is_valid_cycle_intervals(instance, attribute, values):
#    if not isinstance(value, list):
#        print(f'Attribute must be a list of ints. valid example: '\
#              f'{DEFAULT_OBS_CYCLE_INTERVALS}, using default.')
#        return False
#
#    for item in values:
#         if value < 0 or value > MAX_CYCLE_INTERVAL:


def is_valid_date_range(instance, attribute, value):
    if not isinstance(value, dict):
        print(f'Attribute must be a dict, valid example: '\
              f'{DEFAULT_DATE_RANGE_CONFIG}, using defaults.')
        return False

    datestr = value.get('datestr', None)
    if datestr is None:
        msg = f'Invalid date format string: {value}, valid example: ' \
              f'{DEFAULT_DATE_STR}'
        raise ValueError(msg)

    start = set_datetime(value.get('start', None), datestr)
    end = set_datetime(value.get('end', None), datestr)

    if start is None or end is None:
        msg = f'Invalid date range: {value}, valid example: ' \
              f'{DEFAULT_DATE_RANGE_CONFIG}'
        raise ValueError(msg)

    print(f'start: {start}, end: {end}')

    if start > end:
        msg = f'Invalid date range: {value}, "start" must older than ' \
              f'"end", valid example: {DEFAULT_DATE_RANGE_CONFIG}'
        raise ValueError(msg)
    
    return True
    

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
    date_range = attr.ib(
        validator=is_valid_date_range,
        default=DEFAULT_DATE_RANGE_CONFIG
    )
    cycle_intervals = attr.ib(init=False)
    start = attr.ib(init=False)
    end = attr.ib(init=False)


    def __attrs_post_init__(self):
        self.cycle_intervals = DEFAULT_OBS_CYCLE_INTERVALS
        self.start = set_datetime(
            self.date_range['start'],
            self.date_range['datestr']
        )
        self.end = set_datetime(
            self.date_range['end'],
            self.date_range['datestr']
        )


    def get_storage_platform(self):
        return storage_platform


    def get_start(self):
        return self.start


    def get_end(self):
        return self.end


    def get_cycle_intervals(self):
        return self.cycle_intervals


@attr.s(slots=True)
class ObservationsConfig(object):
    """
    Class responsible for loading in the observations inventory search
    configuration.
    """

    config_yaml = attr.ib(validator=is_valid_readable_file)
    obs_search_configs = attr.ib(default=attr.Factory(dict))

    def load(self):
        
        config_data = yaml_utils.YamlLoader(self.config_yaml)
        self.get_obs_inv_search_configs(config_data)
        print(f'config_data: {config_data}')


    def get_obs_inv_search_configs(self, config_data):
        obs_search_yaml_data = config_data.load()

        obs_search_configs = config_data.get_value(
            key='search_info',
            document=obs_search_yaml_data,
            return_type=list
        )

        search_date_range = config_data.get_value(
            key='date_range',
            document=obs_search_yaml_data,
            return_type=dict
        )

        print(f'search_date_range: {search_date_range}')

        try:
            for obs_search_config in obs_search_configs:
                print(f'obs_search_config: {obs_search_config}')

                storage_platform = config_data.get_value(
                    key='platform',
                    document=obs_search_config,
                    return_type=str
                )

                obs_search_config_obj = ObsSearchConfig(
                    storage_platform,
                    obs_search_config,
                    search_date_range
                )
                search_key = obs_search_config['key']
                hash_key = f'{storage_platform}-{search_key}'
                print(f'hash_key: {hash_key}')
                self.obs_search_configs[hash_key] = obs_search_config_obj

        except Exception as e:
            msg = f'Problem loading config data: {e}'
            raise ValueError(msg)

        return self.obs_search_configs


    def get_all_obs_inv_search_configs(self):
        return self.obs_search_configs
