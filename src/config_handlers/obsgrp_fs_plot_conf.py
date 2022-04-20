import os

from dataclasses import dataclass, field
from obs_inv_utils.config_base import ConfigInterface
from obs_inv_utils.yaml_utils import YamlLoader


@dataclass
class ObsFamily:
    yaml_loader: YamlLoader
    data_type_family_name: str
    data_type_family_members: list
    external_obs_intervals: list

    def __post_init__(self):
        print(f'data_type_family_name: {self.data_type_family_name}')
        print(f'data_type_family_members: {self.data_type_family_members}')
        for family_member in self.data_type_family_members:
            print(f'type(family_member): {type(family_member)}')
            if family_member is None:
                continue
            if (family_member.get('data_type') is None or
                    family_member.get('suffix') is None):
                msg = f'data type family member did not contain both ' \
                    f'data_type\' and \'suffix\' keys.'

    def get_members(self):
        return self.data_type_family_members

    def get_family_name(self):
        return self.data_type_family_name

    def get_ext_obs_intrvls(self):
        return self.external_obs_intervals

@dataclass
class ObsGrouping:
    yaml_loader: YamlLoader
    grouping_name: str
    data_type_families: list
    plot_families: list = field(default_factory=list, init=False)

    def __post_init__(self):
        print(f'grouping_name: {self.grouping_name}')

        for data_type_family in self.data_type_families:
            print(f'data_type_family: {data_type_family}')
            try:
                family_name = self.yaml_loader.get_value(
                    key='data_type_family_name',
                    document=data_type_family,
                    return_type=str
                )
            except Exception as e:
                msg = f'problem parsing data_type_family, error: {e}'
                raise ValueError(msg)

            print(
                f'family_name: {family_name}, data_type_family: {data_type_family}')

            try:
                family_members = self.yaml_loader.get_value(
                    key='family_members',
                    document=data_type_family,
                    return_type=list
                )
            except Exception as e:
                print(f'No family members found.')
                family_members = []

            try:
                ext_obs_intrvls = self.yaml_loader.get_value(
                    key='external_obs_intervals',
                    document=data_type_family,
                    return_type=list
                )
            except Exception as e:
                ext_obs_intrvls = []
                print(f'No external intervals found')

            obs_family = ObsFamily(
                self.yaml_loader,
                family_name,
                family_members,
                ext_obs_intrvls
            )

            print(f'{os.linesep}type(obs_family): {type(obs_family)}')

            self.plot_families.append(obs_family)

    def get_plot_families(self):
        return self.plot_families

    def get_grouping_name(self):
        return self.grouping_name



@dataclass
class ObsGroupFileSizePlotConfig(ConfigInterface):
    """
    Function to load config data for file size time series plots
    """
    config_yaml: str
    config_yaml_data: dict = field(default_factory=dict, init=False)
    plot_groupings: list = field(default_factory=list, init=False)

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
        self.set_plot_groupings()

    def set_plot_groupings(self):
        plot_groupings = self.yaml_loader.get_value(
            key='plot_groupings',
            document=self.config_data,
            return_type=list
        )

        for grouping in plot_groupings:
            print(f'plot grouping: {grouping}')
            grouping_name = self.yaml_loader.get_value(
                key='grouping_name',
                document=grouping,
                return_type=str
            )

            data_type_families = self.yaml_loader.get_value(
                key='data_type_families',
                document=grouping,
                return_type=list
            )

            obs_grouping = ObsGrouping(
                self.yaml_loader,
                grouping_name,
                data_type_families
            )

            print(f'{os.linesep}type(obs_grouping): {type(obs_grouping)}')

            self.plot_groupings.append(obs_grouping)
            print(f'{os.linesep}type(plot_groupings): {type(plot_groupings)}')

    def get_plot_groupings(self):
        for grouping in self.plot_groupings:
            print(f'{os.linesep}grouping: {grouping}')
            print(f'{os.linesep}type(grouping): {type(grouping)}')
        return self.plot_groupings
