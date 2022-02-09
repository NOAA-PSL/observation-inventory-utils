import os
from datetime import datetime
from obs_inv_utils import hpss_io_interface as hpss
from obs_inv_utils.config_handler import ObservationsConfig, ObsSearchConfig
from obs_inv_utils import time_utils
from obs_inv_utils.time_utils import DateRange
from obs_inv_utils.hpss_io_interface import HpssTarballContents, HpssFileInfo
from typing import Optional
from dataclasses import dataclass, field


hpss_inspect_tarball = hpss.hpss_cmds[hpss.CMD_INSPECT_TARBALL]

@dataclass
class ObsInventorySearchEngine(object):
    obs_inv_conf: ObservationsConfig
    search_configs: list[ObsSearchConfig] = field(default_factory=list)


    def __post_init__(self):
        print(f'search_configs: {self.search_configs}')
        self.search_configs = self.obs_inv_conf.get_obs_inv_search_configs()
        print(f'search_configs after init: {self.search_configs}')

    def get_obs_file_info(self):

        date_range = self.obs_inv_conf.get_search_date_range()
        master_list = []
        print(f'search config date range: {date_range}')

        all_search_paths_finished = False
        while not all_search_paths_finished:
            all_search_paths_finished = True
            for key, search_config in self.search_configs.items():
                print(f'search_config: {search_config}')
                search_path = search_config.get_current_search_path()
                if search_config.get_date_range().at_end():
                    end = search_config.get_date_range().end
                    print(f'Finished search, path: {search_path}, end: {end}')
                    continue

                args = []
                args.append(search_path)
                hpss_cmd = hpss.HpssCommandHandler(
                    hpss.CMD_INSPECT_TARBALL,
                    args
                )

                if hpss_cmd.send():
                     file_info = hpss_cmd.parse_response()
                     print(f'file_info: {file_info}')
                     files = file_info.files
                     for file in files:
                         master_list.append(file)
                else:
                     print(f'hpss_cmd_failed: {hpss_cmd.get_raw_response()}') 

                search_config.get_date_range().increment_day()
                all_search_paths_finished = False
                print(f'Current search path: {search_path}')

        print(f'All done')
        for file_info in master_list:
            print(f'File info: {file_info}')
