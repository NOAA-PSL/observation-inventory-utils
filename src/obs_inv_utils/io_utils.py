"""
Copyright 2022 NOAA
All rights reserved.

Collection of methods to facilitate file/object retrieval

"""
from obs_inv_utils import credentials as creds


def show_aws_region():
    """
    This function will show and return the configured aws default region
    """
    print(f'aws default region: {creds.AWS_DEFAULT_REGION}')
    return creds.AWS_DEFAULT_REGION
