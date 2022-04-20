from abc import ABCMeta, abstractmethod

from obs_inv_utils import yaml_utils
from obs_inv_utils import obs_storage_platforms
from obs_inv_utils import file_utils


def is_valid_storage_platform(value):
    if not obs_storage_platforms.is_valid(value):
        msg = f'Invalid platform: {value}, must be one of ' \
              f'[{obs_storage_platforms.PLATFORMS}].'
        raise ValueError(msg)

    return True


class ConfigInterface(metaclass=ABCMeta):

    def __init__(self, config_yaml):
        file_utils.is_valid_readable_file(config_yaml)
        self.config_yaml = config_yaml
        self.yaml_loader = yaml_utils.YamlLoader(self.config_yaml)

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def parse(self):
        pass
