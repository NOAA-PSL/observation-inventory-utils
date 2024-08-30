#!/usr/local/bin/csh

# Load obs_inv_util reworked for NASA module paths
# ------------------------------
# The purpose of this script is to 1) load python anaconda env
# and 2) provide a wrapper for the python click cli interface
# for the observation inventory tool
#
# sample usage:
# obs_inv_utils.sh [command] [args]
#

setenv InvToday `date "+%Y-%m-%d"`
setenv indir  $NOBACKUP/NNJA
setenv wrkdir $NOBACKUP/NNJA/function-output/ 
setenv NNJA $NOBACKUP/NNJA
#setenv wrkdir $NOBACKUP/NINJA/DiscoverObsInventory/function-output/$InvToday

#setenv InvToday 'mkdir -v `date "+%Y-%m-%d"`' 
#setenv InvToday '`date "+%Y-%m-%d"`'
# echo `date "+%Y-%m-%d"`
echo $InvToday

mkdir -p $wrkdir
cd $indir

# Environment variables for build dir
setenv OBS_INV_HOME_DIR /discover/nobackup/sicohen/workenv/observation-inventory-utils
setenv OBS_INV_SRC /discover/nobackup/sicohen/workenv/observation-inventory-utils/src
setenv OBS_INV_UTILS /discover/nobackup/sicohen/workenv/observation-inventory-utils/src/obs_inv_utils
#setenv OBS_INV_YAML /discover/nobackup/sicohen/workenv/observation-inventory-utils/discover-yaml
setenv OBS_INV_FIGURES /discover/nobackup/sicohen/workenv/observation-inventory-utils/src/obs_inv_utils/figures
#setenv SQL_UTILS /discover/nobackup/sicohen/workenv/observation-inventory-utils/src/sql_utils
setenv clean_bucket_pack /discover/nobackup/sicohen/workenv/clean_bucket_pack

# -------------------------------------------------
# Loading NOAA Tool ~ observation-inventory-utils
# -------------------------------------------------


# From README installation instructions on github
# ------------------------------
# module purge
# module use -a /contrib/home/builder/UFS-RNR-stack/modules
# module load anaconda3
# module load intel/18.0.5.274
# module load impi/2018.4.274
# ------------------------------

# NASA DISCOVER
module purge
module load comp/intel/18.0.5.274
module load mpi/impi/18.0.5.274
module load aws/2
module load python/GEOSpyD/Min23.5.2-0_py3.11

setenv PATH discover/nobackup/sicohen/workenv/NCEPLIBS-bufr/NCEPLIBS-bufr-bufr_v12.0.0/utils:$PATH
setenv OBS_INV_HOME_DIR /discover/nobackup/sicohen/workenv/observation-inventory-utils
setenv OBS_INV_SRC $OBS_INV_HOME_DIR/src
setenv PYTHONPATH $NOBACKUP/sicohen/workenv/observation-inventory-utils/env/lib/python3.7/site-packages:$PYTHONPATH
setenv PYTHONPATH $OBS_INV_HOME_DIR/src:$PYTHONPATH

echo source $NOBACKUP/venvs/ObsInvEnv/bin/activate.csh

source $NOBACKUP/venvs/ObsInvEnv/bin/activate.csh

#echo PYTHONPATH=$PYTHONPATH
#echo Python Version: $(python --version)

echo cd $indir
cd $indir

# Alias for the ls discover command in discover_interface.py
# For discover_interface.py ~ discover_cmd(['ls','-ld', --time-type=full-iso']
alias my_ls_time 'ls -ldr'

