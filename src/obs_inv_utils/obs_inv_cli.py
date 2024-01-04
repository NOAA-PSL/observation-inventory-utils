#!/usr/bin/env python
"""
Copyright 2022 NOAA
All rights reserved.

Collection of methods to inventory observation files

"""

import logging
import os
import sys

import click

# import obs_inv_utils.config_handlers as cf_hdlr
import obs_inv_utils
import config_handlers
from config_handlers.obsgrp_fs_plot_conf import ObsGroupFileSizePlotConfig
from config_handlers.obsgrp_fs_plot_conf import ObsGrouping, ObsFamily
from config_handlers.obs_search_conf import ObservationsConfig
from config_handlers.obs_meta_sinv import ObsMetaSinvConfig
from config_handlers.obs_meta_cmpbqm import ObsMetaCMPBQMConfig
from config_handlers import obs_meta_sinv, obs_meta_cmpbqm
from obs_inv_utils.nceplibs_bufr_cmd_handler import ObsBufrFileMetaHandler, ObsPrepBufrFileMetaHandler

from obs_inv_utils import plot_generator as pg
from obs_inv_utils import search_engine as se

@click.group()
def cli():
    """Cli for observations Inventory."""


def get_obs_inventory_base(config_yaml):
    print(f'Inventory config to use: {config_yaml}')
    cf = ObservationsConfig(config_yaml)
    cf.load()
    inv_search = se.ObsInventorySearchEngine(cf)
    inv_search.get_obs_file_info()

@cli.command()
@click.option('-c', '--config-yaml', 'config_yaml', required=True, type=str)
def get_obs_inventory(config_yaml):
    return get_obs_inventory_base(config_yaml)

@cli.command()
@click.option('-m', '--min-instances', 'min_instances', required=True, type=int)
def plot_files_filesize_vs_time(min_instances):
    size_timeline = pg.ObsInvFilesizeTimeline(min_instances)
    size_timeline.plot_timeline()


@cli.command()
@click.option('-c', '--config-yaml', 'config_yaml', required=True, type=str)
def plot_groups_filesize_timeseries(config_yaml):
    config = ObsGroupFileSizePlotConfig(config_yaml)
    config.load()
    # print(repr(config))
    obgr = pg.ObsGroupFilesizeTimeline(config)
    obgr.plot_obsgroups_fs_timeline()

def get_obs_count_meta_sinv_base(config_yaml):
    config = ObsMetaSinvConfig(config_yaml)
    config.load()
    print(repr(config))
    mh = ObsBufrFileMetaHandler(config)
    mh.get_bufr_file_meta(obs_meta_sinv.NCEPLIBS_BUFR_SINV)

@cli.command()
@click.option('-c', '--config-yaml', 'config_yaml', required=True, type=str)
def get_obs_count_meta_sinv(config_yaml):
    return get_obs_count_meta_sinv_base(config_yaml)

def get_obs_count_meta_cmpbqm_base(config_yaml):
    config = ObsMetaCMPBQMConfig(config_yaml)
    config.load()
    print(repr(config))
    mh = ObsPrepBufrFileMetaHandler(config)
    mh.get_prepbufr_file_meta(obs_meta_cmpbqm.NCEPLIBS_PREPBUFR_CMPBQM)

@cli.command()
@click.option('-c', '--config-yaml', 'config_yaml', required=True, type=str)
def get_obs_count_meta_cmpbqm(config_yaml):
    return get_obs_count_meta_cmpbqm_base(config_yaml)
    

if __name__ == '__main__':
    print(f'in cli - input arguments: {sys.argv[1:]}')
    cli()
