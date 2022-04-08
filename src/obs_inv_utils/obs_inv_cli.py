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
from config_handlers.obsgrp_fs_plot_conf import ObsGroupFileSizePlotConfig
from config_handlers.obs_search_conf import ObservationsConfig
from obs_inv_utils import plot_generator as pg


@click.group()
def cli():
    """Cli for observations Inventory."""


@cli.command()
@click.option('-c', '--config-yaml', 'config_yaml', required=True, type=str)
def get_obs_inventory(config_yaml):

    print(f'Inventory config to use: {config_yaml}')
    cf = ObservationsConfig(config_yaml)
    cf.load()
    # harvester = harvester_engine.HarvesterEngine(cf)
    # harvester.get_obs_file_sizes()


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
    print(repr(config))


if __name__ == '__main__':
    print(f'in cli - input arguments: {sys.argv[1:]}')
    cli()
