#!/usr/local/bin/csh

# Load obs_inv_util reworked for NASA module paths
# ------------------------------
# The purpose of this script is to 1) load python anaconda env

# -------------------------------------------------
# Loading NOAA Tool ~ observation-inventory-utils
# -------------------------------------------------


# NASA DISCOVER
module purge
module load comp/intel/18.0.5.274
module load mpi/impi/18.0.5.274
module load aws/2
module load python/GEOSpyD/Min23.5.2-0_py3.11

# Environment Variables ~ required (?) by obs_inv_utils
setenv OBS_INV_HOME_DIR $PWD
setenv OBS_INV_SRC $OBS_INV_HOME_DIR/src
setenv PYTHONPATH $OBS_INV_HOME_DIR/src:$PYTHONPATH
setenv PATH $NOBACKUP/workenv/NCEPLIBS-bufr/NCEPLIBS-bufr-bufr_v12.0.0/utils:$PATH


# Virtual environment 
source $NOBACKUP/venvs/ObsInvEnv/bin/activate.csh

echo PYTHONPATH=$PYTHONPATH
