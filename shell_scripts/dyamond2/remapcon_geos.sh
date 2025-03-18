#!/bin/bash
#SBATCH --job-name=g_remapcon
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=20GB
#SBATCH --time=04:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=g_rmcon.eo%j
#SBATCH --error=g_rmcon_err.eo%j

set -evx # verbose messages and crash message
module load cdo

FILE_PATH=/scratch/b/b380887/GEOS
WORK_PATH=/work/bb1153/b380887/global_tropics/GEOS
GRIDS=/home/b/b380887/cold-point-overshoot/slurm_scripts/process_files/grid_files

# # geopotential: 0.25deg
# ZG_IN=$WORK_PATH/GEOS_zg_12-20km_winter_ITCZ_days10-40.nc
# ZG_OUT=$FILE_PATH/GEOS_zg_0.25deg_12-20km_winter_ITCZ_days10-40.nc
# cdo -remapcon,$GRIDS/itcz_0.25deg_grid.txt $ZG_IN $ZG_OUT

# temperature: 0.25deg
TEMP_IN=$FILE_PATH/GEOS_temp_12-20km_winter_ITCZ.nc
TEMP_OUT=$FILE_PATH/GEOS_0.25deg_temp_12-20km_winter_ITCZ.nc
cdo -remapcon,$GRIDS/itcz_0.25deg_grid.txt $TEMP_IN $TEMP_OUT

# # OLR: hourly, 1x1
# OLR_IN=$FILE_PATH/GEOS_OLR_winter_ITCZ.nc
# OLR_OUT=$FILE_PATH/GEOS_hourly_1x1_OLR_winter_ITCZ.nc
# cdo -timselmean,4,0 -remapcon,$GRIDS/itcz_1x1_grid.txt $OLR_IN $OLR_OUT

# # precip: 30 min, 0.1deg
# PR_IN=$FILE_PATH/GEOS_pr_winter_ITCZ.nc
# PR_OUT=$FILE_PATH/GEOS_pr_30min_0.1deg_winter_ITCZ.nc
# cdo -timselmean,2,0 -remapcon,$GRIDS/itcz_0.1deg_grid.txt $PR_IN $PR_OUT


