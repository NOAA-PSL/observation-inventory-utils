#!/bin/bash
#
# script for configuring set up to run on obs inventory cluster on parallel works


module load gnu
module load intel/2023.2.0
module load impi/2023.2.0
export PATH=/contrib/inv-stack/ncep/NCEPLIBS-bufr-12.1.0/utils:$PATH 

OBS_INV_HOME_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PYTHONPATH=$OBS_INV_HOME_DIR/src
echo PYTHONPATH=$PYTHONPATH
echo Python Version: $(python --version)

