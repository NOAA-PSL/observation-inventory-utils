from dataclasses import dataclass, field
from obs_inv_utils.config_base import ConfigInterface


@dataclass
class ObsGroupFileSizePlotConfig(ConfigInterface):
    """
    Function to load config data for file size time series plots
    """
    config_yaml: str
    config_data: dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        super().__init__(self.config_yaml)

    def __repr__(self):
        """
        string representation of config_yaml and config_data
        """
        return f'config_yaml: {self.config_yaml}, ' \
            f'config_data: {self.config_data}'

    def load(self):
        self.config_data = self.yaml_loader.load()
        self.parse()

    def parse(self):
        print(f'type(self.config_data): {type(self.config_data)}')
        #self.plot_groups = self.parse_plot_groups()

    def parse_plot_groups(self):
        pass
