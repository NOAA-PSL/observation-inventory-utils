from dataclasses import dataclass
from datetime import datetime

from obs_inv_utils import obs_inv_queries as oiq

DEFAULT_MIN_DATETIME = datetime.strptime('2000-01-01', '%Y-%m-%d')
DEFAULT_MAX_DATETIME = datetime.strptime('2021-01-01', '%Y-%m-%d')

@dataclass
class ObsInvFilesizeTimeline(object):
    min_instances: int

    def __post_init__(self):
        if self.min_instances < 0:
            msg = f'Invalid minimum instances: {self.min_instances}, must ' \
                  f'be greater than or equal to 0.'
            raise ValueError(msg)


    def plot_timeline(self):
        data = oiq.get_filesize_timeline_data(self.min_instances)
        print(f'Observation inventory file filesize data: {data}')
