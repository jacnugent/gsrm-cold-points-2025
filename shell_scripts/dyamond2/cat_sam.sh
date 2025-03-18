#!/bin/bash
#SBATCH --job-name=cat_sam
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=25GB
#SBATCH --time=01:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=cat.eo%j
#SBATCH --error=cat_err.eo%j

set -evx # verbose messages and crash message

module load cdo

FILE_PATH=/scratch/b/b380887/SAM

# cdo cat $FILE_PATH/"12-20_wa*.nc" $FILE_PATH/SAM_w_12-20km_winter_ITCZ.nc

# cdo cat $FILE_PATH/*cli*.nc $FILE_PATH/SAM_qi_12-20km_winter_ITCZ.nc
#cdo cat $FILE_PATH/*hus*.nc $FILE_PATH/SAM_qv_12-20km_winter_ITCZ.nc

# cdo cat $FILE_PATH/rltacc*.nc $FILE_PATH/SAM_OLR_acc_winter_ITCZ.nc
# cdo cat $FILE_PATH/rltacc*.nc $FILE_PATH/SAM_OLR_acc_winter_GT.nc
cdo cat $FILE_PATH/pr*.nc $FILE_PATH/SAM_pr_acc_winter_ITCZ.nc

#cdo cat $FILE_PATH/clivi*.nc $FILE_PATH/SAM_IWP_winter_ITCZ.nc
#cdo cat $FILE_PATH/qsvi*.nc $FILE_PATH/SAM_SWP_winter_ITCZ.nc
#cdo cat $FILE_PATH/qgvi*.nc $FILE_PATH/SAM_GWP_winter_ITCZ.nc
#cdo cat $FILE_PATH/"12-20_ta*.nc" $FILE_PATH/SAM_temp_12-20km_winter_ITCZ.nc
