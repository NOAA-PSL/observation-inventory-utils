#!/bin/bash
# The purpose of this script is to 1) load python anaconda env
# and 2) provide a wrapper for the python click cli interface
# for the observation inventory tool
#
# sample usage:
# obs_inv_utils.sh [command] [args]
#

set -eu
set +x

module purge
module use -a /scratch2/BMC/gsienkf/UFS-RNR/UFS-RNR-stack/modules
module load anaconda3

OBS_INV_HOME_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PYTHONPATH=$OBS_INV_HOME_DIR/src
echo PYTHONPATH=$PYTHONPATH
echo Python Version: $(python --version)

set -a
source $OBS_INV_HOME_DIR/.env_rc
set +a

echo args: $@
python $OBS_INV_HOME_DIR/src/obs_inv_utils/obs_inv_cli.py $@
