from dataclasses import dataclass
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import mpld3
import os
import pandas as pd
from pandas import DataFrame
import pathlib
import numpy as np

from obs_inv_utils import obs_inv_queries as oiq

CALLING_DIR = pathlib.Path(__file__).parent.resolve()

DEFAULT_MIN_DATETIME = datetime.strptime('1999-12-30', '%Y-%m-%d')
DEFAULT_MAX_DATETIME = datetime.strptime('2021-01-01', '%Y-%m-%d')

OBS_INV_DATERANGE = pd.date_range(
    DEFAULT_MIN_DATETIME,
    DEFAULT_MAX_DATETIME,
    freq='D'
)

OBS_INV_DATERANGE_6H_CYCLE = pd.date_range(
    DEFAULT_MIN_DATETIME,
    DEFAULT_MAX_DATETIME,
    freq='6H'
)

print(f'OBS_INV_DATERANGE: {OBS_INV_DATERANGE}')

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

        unique_rows = data.sort_values(
            'inserted_at'
        ).drop_duplicates(
            subset=[
                'filename',
                'obs_day'
            ],
            keep='last'
        )
        data_index = unique_rows.index

        uf = data.sort_values(
            'inserted_at'
        ).drop_duplicates(
            ['filename', 'obs_day'],
            keep='last'
        ).dropna(subset=['cycle_time'])

        # bad = uf.loc[uf['cycle_time'] == np.nan]
        # print(f'bad: {bad}')

        uf['generic_fn'] = uf['prefix'] + '.tag.' + uf['un']
        uf['cycle_time'].replace(np.nan, 0)
        uf['cycle_sec_float'] = uf['cycle_time'].astype('float64')
        uf['cycle_time_datetime'] = pd.to_timedelta(
            uf['cycle_sec_float'], unit='s')

        uf['obs_day'] = pd.to_datetime(uf['obs_day'])
        obs_times = uf[['obs_day', 'cycle_time_datetime', 'cycle_time']]

        # for obs_time in obs_times.itertuples():

        #     print(f'obs_times: {obs_time}')
        # print(f'obs_time.info {obs_time.info()}')
        uf['obs_cycle_time'] = uf['obs_day'] + uf['cycle_time_datetime']

        print(f'uf: {len(uf.index)}, {uf}')

        uf_gn = uf.copy()
        unique_gn = uf_gn.drop_duplicates(
            'generic_fn',
            keep='last'
        ).sort_values('instances', ascending=False)

        count = 0

        file_count = len(unique_gn.index)

        last_generic_fn = ''
        plt_cnt = 0
        for unique_fn in unique_gn.itertuples():

            generic_fn = unique_fn.generic_fn
            if last_generic_fn != generic_fn:
                last_generic_fn = generic_fn
                plt_cnt += 1
            else:
                continue
            count += 1
            file_meta = uf.loc[
                uf['generic_fn'] == unique_fn.generic_fn
            ]

            # print(
            #     f'file_meta: records: {len(file_meta.index)}, file_meta data: {file_meta}')

            # unique_tags = file_meta.drop_duplicates('cycle_tag', keep='last')
            # print(f'unique_tags: {unique_tags}')

            plt.figure(figsize=(11, 8.5), dpi=160)
            plt.subplot(111)

            # print(f'file_meta.info(): {file_meta.info()}')

            xy = file_meta.copy()
            # .loc[
            #     ['obs_day', 'obs_cycle_time', 'file_size']
            # ].copy()
            # .drop_duplicates('obs_cycle_time', keep='last').copy()

            xy.set_index('obs_cycle_time', inplace=True)
            max_file_size = xy['file_size'].max()
            xy_new = xy.reindex(
                OBS_INV_DATERANGE_6H_CYCLE,
                fill_value=-(max_file_size*0.1)
            )

            x = xy_new.index
            y = xy_new['file_size']
            plt.plot(x, y/1000000, linewidth=0.3)

            # for tag in unique_tags.itertuples():

            #     xy = file_meta.loc[
            #         file_meta['cycle_tag'] == tag.cycle_tag,
            #         ['obs_day', 'file_size']
            #     ].drop_duplicates('obs_day', keep='last').copy()

            #     xy.set_index('obs_day', inplace=True)
            #     max_file_size = xy['file_size'].max()
            #     xy_new = xy.reindex(OBS_INV_DATERANGE,
            #                         fill_value=-(max_file_size*0.1))

            #     missing_data = xy_new.loc[xy_new['file_size'] <= 0]

            #     x = xy_new.index
            #     y = xy_new['file_size']

            #     plt.scatter(x, y/1000000, label=tag.cycle_tag, s=0.5)

            # plt.legend()
            plt.gcf().autofmt_xdate()

            figure_title = 'file: ' + generic_fn + \
                f', {plt_cnt} of {file_count}'
            plt.title(figure_title)
            plt.xlabel('Observation Day')
            plt.ylabel('File Size (Mb)')
            y_axis = plt.gca()
            y_axis.ticklabel_format(style='plain', axis='y')

            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            dest_fn = generic_fn
            dest_path_png = os.path.join(
                CALLING_DIR, 'figures', dest_fn + '.png'
            )
            parent_dir = pathlib.Path(dest_path_png).parent
            pathlib.Path(parent_dir).mkdir(parents=True, exist_ok=True)
            dest_path_html = os.path.join(
                CALLING_DIR, 'figures', dest_fn + '.html'
            )
            print(f'saving figure to {dest_path_png}')
            plt.savefig(dest_path_png)

            # fig = plt.gcf()
            # html_str = mpld3.fig_to_html(fig)
            # Html_file = open(dest_path_html, "w")
            # Html_file.write(html_str)
            # Html_file.close()
            # plt.show()

            # if count == 10:
            #     exit(1)
