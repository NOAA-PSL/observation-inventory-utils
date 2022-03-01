#!/usr/bin/env python
"""
Copyright 2022 NOAA
All rights reserved.

Collection of methods to inventory observation files

"""
import click
import logging
import os
from obs_inv_utils import io_utils
import sys
from obs_inv_utils import config_handler as cf
# from obs_inv_utils import harvester_engine
from obs_inv_utils import plot_generator as pg

@click.group()
def cli():
    """Cli for observations Inventory."""

@cli.command()
def hello_world():
    click.echo('Hello World!')


@cli.command()
@click.option('-c', '--config-inv-yaml', 'config_yaml', required=True, type=str)
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


if __name__ == '__main__':
    print(f'in cli - input arguments: {sys.argv[1:]}')
    cli()
