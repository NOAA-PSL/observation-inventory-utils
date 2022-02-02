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

if __name__ == '__main__':
    print(f'in cli - input arguments: {sys.argv[1:]}')
    cli()
