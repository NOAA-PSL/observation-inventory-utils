'''
File for collecting constants and utility functions used for the automated inventory system
'''
from collections import namedtuple

#constants
NCEPLIBS_SINV = 'sinv'
NCEPLIBS_CMPBQM = 'cmpbqm'

HV_IODA_META = 'ioda_meta_netcdf'

CLEAN_PLATFORM = 'aws_s3_clean'
REANALYSIS_BUCKET = 'noaa-reanlyses-pds'

PRIVATE_EUMETSAT_PLATFORM = 'aws_s3_private'
PRIVATE_EUMETSAT_BUCKET = 'nnja-private-eumetsat'

DATESTR_FORMAT = '%Y%m%dT%H%M%SZ'
ESCAPED_DATESTR_FORMAT = '%%Y%%m%%dT%%H%%M%%SZ'

CYCLING_6H = '21600'
CYCLING_DAILY = '86400'
CYCLING_HOURLY = '3600'

InventoryInfo = namedtuple(
    'InventoryInfo',
    [
        'obs_name',
        'key',
        'start',
        'platform',
        'cycling_interval',
        's3_bucket',
        's3_prefix',
        'files',
        'inv_cmd'
    ]
)
