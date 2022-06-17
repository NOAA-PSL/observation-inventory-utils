# builtin imports
from copy import deepcopy
from typing import Optional
from dataclasses import dataclass, field

# third party import
import attr

# local imports
import obs_inv_utils
from obs_inv_utils import config_base
from obs_inv_utils.config_base import ConfigInterface
from obs_inv_utils.yaml_utils import YamlLoader
from obs_inv_utils import time_utils
from obs_inv_utils.time_utils import DateRange


SEARCH_PATH_KEY = 'key'


@dataclass
class ObsSearchConfig(object):
    """
    Class responsible for creating an observation search config.
    """

    storage_platform: str
    search_config: dict
    date_range: DateRange
    cycle_intervals: list = field(default_factory=list, init=False)

    def __post_init__(self):
        config_base.is_valid_storage_platform(self.storage_platform)
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


@dataclass
class ObservationsConfig(ConfigInterface):
    """
    Class responsible for loading in the observations inventory search
    configuration.
    """

    config_yaml: str
    config_data: dict = field(default_factory=dict, init=False)
    obs_search_configs: dict = field(default_factory=dict, init=False)
    search_date_range: DateRange = field(
        default_factory=DateRange, init=False)

    def __post_init__(self):
        super().__init__(self.config_yaml)

    def load(self):
        self.config_data = self.yaml_loader.load()
        self.parse()
        print(f'config_data: {self.config_data}')

    def parse(self):
        

        obs_search_configs = self.yaml_loader.get_value(
            key='search_info',
            document=self.config_data,
            return_type=list
        )

        config_date_range = self.yaml_loader.get_value(
            key='date_range',
            document=self.config_data,
            return_type=dict
        )

        self.search_date_range = time_utils.get_date_range_from_dict(
            config_date_range)

        print(f'search_date_range: {self.search_date_range}')

        try:
            for obs_search_config in obs_search_configs:
                print(f'obs_search_config: {obs_search_config}')

                storage_platform = self.yaml_loader.get_value(
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
