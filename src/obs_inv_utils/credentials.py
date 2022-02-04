"""
Copyright 2022 NOAA
All rights reserved.

Collection of methods to facilitate file/object retrieval

"""
import os
#from dotenv import load_dotenv

# load private credentials from environment variables that were sourced from
# the file .env_rc .  It would be a lot easier to use the dotenv module

#load_dotenv()

# load private credentials
AWS_ACCESS_KEY_ID = os.getenv("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = os.getenv("aws_secret_access_key")
AWS_DEFAULT_REGION = os.getenv("aws_default_region")
