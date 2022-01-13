"""
Copyright 2022 NOAA
All rights reserved.

Collection of methods to inventory observation files

"""
import click
import logging
import os
from obs_inv_utils import io_utils

logLevel = os.environ.get("LOG_LEVEL")
if logLevel is None:
    logLevel = logging.DEBUG
logger = logging.getLogger(__name__)
try:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logLevel,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
except Exception:
    logger.exception('bad log level env var')
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

@click.group()
def cli():
    """Cli for observations Inventory."""

@cli.command()
def hello_world():
    click.echo('Hello World!')
