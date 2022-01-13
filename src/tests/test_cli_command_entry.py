"""
Copyright 2022 NOAA
All rights reserved.

Unit tests for io_utils

"""
from obs_inv_utils import io_utils
from obs_inv_utils import credentials as creds


def test_aws_default_region():
    """
    Test the import of .env constant aws_default_region
    """

    assert io_utils.show_aws_region() == creds.AWS_DEFAULT_REGION
