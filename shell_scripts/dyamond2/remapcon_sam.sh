#!/bin/bash
#SBATCH --job-name=s_remapcon
#SBATCH --partition=prepost
#SBATCH --ntasks=1
#SBATCH --time=08:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=s_rmcon.eo%j
#SBATCH --error=s_rmcon_err.eo%j

set -evx # verbose messages and crash message

WORK_PATH=/work/bb1153/b380887/global_tropics/SAM
FILE_PATH=/scratch/b/b380887/global_tropics/SAM
GRIDS=/pf/b/b380887/cold-point-overshoot/slurm_scripts/process_files/grid_files

# OLR: hourly, 1x1
#OLR_IN=$FILE_PATH/SAM_OLR_winter_ITCZ.nc
#OLR_OUT=$FILE_PATH/coarsened/SAM_hourly_1x1_OLR_winter_ITCZ.nc
#cdo -timselmean,4,0 -remapcon,$GRIDS/itcz_1x1_grid.txt $OLR_IN $OLR_OUT

# precip: 30 min, 0.1deg
#PR_IN=$FILE_PATH/SAM_pr_winter_ITCZ.nc
#PR_OUT=$FILE_PATH/coarsened/SAM_pr_30min_0.1deg_winter_ITCZ.nc
#cdo -timselmean,2,0 -remapcon,$GRIDS/itcz_0.1deg_grid.txt $PR_IN $PR_OUT

# 12-20 km temperature: 0.25deg, 3 hourly
T_IN=$WORK_PATH/SAM_temp_12-20km_winter_ITCZ.nc
T_OUT=$FILE_PATH/SAM_0.25deg_temp_12-20km_winter_ITCZ.nc
cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt $T_IN $T_OUT
