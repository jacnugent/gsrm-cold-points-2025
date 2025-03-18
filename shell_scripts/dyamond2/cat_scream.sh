#!/bin/bash
#SBATCH --job-name=cat_scream
#SBATCH --partition=interactive
#SBATCH --mem=20GB
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=cat_scream.eo%j
#SBATCH --error=cat_scream_err.eo%j

set -evx # verbose messages and crash message

module load cdo

FILE_PATH=/scratch/b/b380887/SCREAM
                                                                                            
# cdo cat $FILE_PATH/*ps*.nc $FILE_PATH/SCREAM_ps_winter_ITCZ.nc

# cdo cat $FILE_PATH/*wap*.nc $FILE_PATH/SCREAM_wap_12-20km_winter_ITCZ_days10-40.nc
# cdo cat $FILE_PATH/*cli*.nc $FILE_PATH/SCREAM_qi_12-20km_winter_ITCZ.nc
# cdo cat $FILE_PATH/*hus*.nc $FILE_PATH/SCREAM_qv_12-20km_winter_ITCZ.nc
# cdo cat $FILE_PATH/*ta*.nc $FILE_PATH/SCREAM_temp_12-20km_winter_ITCZ.nc

# cdo cat $FILE_PATH/rlt*.nc $FILE_PATH/SCREAM_OLR_winter_ITCZ.nc
# cdo cat $FILE_PATH/rlt*.nc $FILE_PATH/SCREAM_OLR_winter_GT.nc
cdo cat $FILE_PATH/pr*.nc $FILE_PATH/SCREAM_precip_winter_ITCZ.nc
#cdo cat $FILE_PATH/clivi*.nc $FILE_PATH/SCREAM_FWP_winter_ITCZ.nc
