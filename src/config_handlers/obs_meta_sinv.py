import os

from dataclasses import dataclass, field
from obs_inv_utils.config_base import ConfigInterface
from obs_inv_utils.yaml_utils import YamlLoader
from obs_inv_utils import time_utils
from obs_inv_utils.time_utils import DateRange

NCEPLIBS_BUFR_SINV = 'nceplibs_bufr_sinv'

@dataclass
class ObsMetaSinvConfig(ConfigInterface):
    """
    Function to load config data for observation counts in bufr
    files as processed by Jack Woolen's NCEPLIBS-bufr utility
    """
    config_yaml: str
    config_data: dict = field(default_factory=str, init=False)
    s3_bucket: str = field(default_factory=str, init=False)
    s3_prefix: str = field(default_factory=str, init=False)
    bufr_files: list = field(default_factory=list, init=False)
    work_dir: str = field(default_factory=str, init=False)
    scrub_files: bool = field(default_factory=bool, init=False)
    platform: str = field(default_factory=str, init=False) 
    date_range: DateRange = field(
        default_factory=DateRange, init=False)

    def __post_init__(self):

        super().__init__(self.config_yaml)

    def __repr__(self):
        """
        string representation of config_yaml and config_data
        """
        return f'config_yaml: {self.config_yaml}, ' \
            f'config_data: {self.config_data}, ' \
            f's3_bucket: {self.s3_bucket}, ' \
            f's3_bucket: {self.date_range}, ' \
            f's3_bucket: {self.bufr_files}, '


    def load(self):
        self.config_data = self.yaml_loader.load()
        self.parse()

    def parse(self):
        print(f'type(self.config_data): {type(self.config_data)}')

        self.platform = self.yaml_loader.get_value(
            key='platform',
            document=self.config_data,
            return_type=str
        )        

        self.s3_bucket = self.yaml_loader.get_value(
            key='s3_bucket',
            document=self.config_data,
            return_type=str
        )

        self.s3_prefix = self.yaml_loader.get_value(
            key='s3_prefix',
            document=self.config_data,
            return_type=str
        )

        date_range = self.yaml_loader.get_value(
            key='date_range',
            document=self.config_data,
            return_type=dict
        )

        
        self.date_range = time_utils.get_date_range_from_dict(
            date_range)

        self.bufr_files = self.yaml_loader.get_value(
            key='bufr_files',
            document=self.config_data,
            return_type=list
        )

        self.work_dir = self.yaml_loader.get_value(
            key='work_dir',
            document=self.config_data,
            return_type=str
        )

        self.scrub_files = self.yaml_loader.get_value(
            key='scrub_files',
            document=self.config_data,
            return_type=bool
        )

    def get_date_range(self):
        return self.date_range

    def get_bufr_file_list(self):
        return self.bufr_files
