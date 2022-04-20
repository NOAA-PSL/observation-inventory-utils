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
from config_handlers.obsgrp_fs_plot_conf import ObsGroupFileSizePlotConfig
from config_handlers.obsgrp_fs_plot_conf import ObsGrouping, ObsFamily

CALLING_DIR = pathlib.Path(__file__).parent.resolve()

DEFAULT_MIN_DATETIME = datetime.strptime('1989-12-30', '%Y-%m-%d')
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
class ObsGroupFilesizeTimeline(object):
    config: ObsGroupFileSizePlotConfig

    def plot_obsgroups_fs_timeline(self):

        groupings = self.config.get_plot_groupings()
        print(f'{os.linesep}groupings: {groupings}, type(groupings): {type(groupings)}')

        for grouping in groupings:
            print(f'{os.linesep}type(grouping): {type(grouping)}')
            families = grouping.get_plot_families()
            print(f'{os.linesep}families: {families}')

            fmly_cnt = len(families)
            fig, ax = plt.subplots(
                fmly_cnt, 1, sharex=True, figsize=(25, 11), dpi=160)
            figure_title = grouping.get_grouping_name()
            fig.suptitle(figure_title, y=0.95, fontsize=20)

            for idx, family in enumerate(families):
                plt.subplot(fmly_cnt, 1, idx+1)
                print(f'{os.linesep}family: {family}')

                data = oiq.get_family_fs_data(family)
                data['generic_fn'] = data['prefix'] + \
                    '.tag.' + data['data_type'] + data['suffix']
                print(f'data: {data}')
                print(f'type(ax): {type(ax)}')
                members = family.get_members()
                if type(ax) == np.ndarray:
                    ax_sub = ax[idx]
                else:
                    ax_sub = ax
                for member in members:
                    data_type = member.get('data_type')
                    xy = data.loc[
                        data['data_type'] == data_type
                    ].copy()

                    print(f'file_meta: {xy}')
                    xy.set_index('obs_day', inplace=True)
                    max_file_size = xy['file_size'].max()
                    print(f'max_file_size: {max_file_size/1000000}')
                    xy_new = xy.reindex(
                        OBS_INV_DATERANGE_6H_CYCLE,
                        fill_value=-(max_file_size*0.1)
                    )

                    x = xy_new.index
                    y = xy_new['file_size']
                    ax_sub.plot(x, y/1000000, linewidth=0.3, label=data_type)
                    leg = ax_sub.legend(loc='center left', facecolor="white")

                    leg_lines = leg.get_lines()
                    print(f'leg_lines: {leg_lines}')
                    # leg_texts = leg.get_texts()

                    for leg_line in leg_lines:
                        leg_line.set_linewidth(4)
                        # plt.setp(leg_texts, fontsize=10)

                subplot_title = family.get_family_name()
                print(f'ax_sub: {ax_sub}')

                ax_sub.minorticks_on()
                ax_sub.text(0.02, 0.85, subplot_title,
                            transform=ax_sub.transAxes, fontsize=15, backgroundcolor='white')
                ax_sub.grid(which='both', color='grey',
                            linestyle='--', linewidth=0.2)
                plt.ylabel('File Size(Mb)', fontsize=15)

            plt.gcf().autofmt_xdate()

            plt.xlabel('Observation Datetime', fontsize=15)
            y_axis = plt.gca()
            y_axis.ticklabel_format(style='plain', axis='y')

            dest_fn = figure_title.replace(' ', '_').lower()
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

        # due to duplicate inserts of the same file, we need to select only
        # the most recent insert.  Mutliple inserts can occur due to 
        # multiple runs of the inventory search tool.  The most recent
        # insert is considered the current status of that file.  After
        # this operation, we should have a current and unique set of filenames
        # spanning the entire date range of interest.
        uf = data.sort_values(
            'inserted_at'
        ).drop_duplicates(
            ['filename', 'obs_day'],
            keep='last'
        ).dropna(subset=['cycle_time'])

        # create a 'cycle_time_datetime' column from the 'cycle_time' column
        # note the 'cycle_time' column does not contain date information.
        # this new column will now be in the datetime format but will not
        # be set to a specific date.  So adding this new column to the
        # 'obs_day' column will help create a new 'obs_cycle_time' column
        # which defines a combination of the 'obs_day' and 
        # 'cycle_time_datetime'.
        # for example: 'cycle_time_datetime' = 01/01/1970T06:00:00
        # 'obs_day' = 01/01/2014T00:00:00 => 'obs_cycle_time' =
        # 'obs_day' + 'cycle_time_datetime' = 01/01/2014T06:00:00
        uf['generic_fn'] = uf['prefix'] + '.tag.' + uf['un']
        uf['cycle_time'].replace(np.nan, 0)
        uf['cycle_sec_float'] = uf['cycle_time'].astype('float64')
        uf['cycle_time_datetime'] = pd.to_timedelta(
            uf['cycle_sec_float'], unit='s')

        uf['obs_day'] = pd.to_datetime(uf['obs_day'])
        obs_times = uf[['obs_day', 'cycle_time_datetime', 'cycle_time']]

        uf['obs_cycle_time'] = uf['obs_day'] + uf['cycle_time_datetime']

        # This operation creates a unique list of generic filenames
        # following the pattern 'prefix.tag.data_type.suffix' where
        # the tag is 't00z', 't06z', 't12z', and 't18z'.  All records with
        # the same prefix, data_type, and suffix are considered 1 generic
        # filename.  Thus only 1 instance of any given generic filename
        # represents all tags and obs_day records for that generic filename.
        uf_gn = uf.copy()
        unique_gn = uf_gn.drop_duplicates(
            'generic_fn',
            keep='last'
        ).sort_values('instances', ascending=False)

        count = 0

        file_count = len(unique_gn.index)

        last_generic_fn = ''
        plt_cnt = 0
        # iterate through all the generic filenames
        # to produce a time series (including all cycle times) of filename
        # filesizes.  A negative value indicates the file did not exist at
        # that particular obs_day/cycle_time.
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

            plt.figure(figsize=(11, 8.5), dpi=160)
            plt.subplot(111)

            xy = file_meta.copy()

            xy.set_index('obs_cycle_time', inplace=True)
            max_file_size = xy['file_size'].max()
            xy_new = xy.reindex(
                OBS_INV_DATERANGE_6H_CYCLE,
                fill_value=-(max_file_size*0.1)
            )

            x = xy_new.index
            y = xy_new['file_size']
            plt.plot(x, y/1000000, linewidth=0.3)

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

