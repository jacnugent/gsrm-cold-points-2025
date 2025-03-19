#!/bin/bash
# header goes here
# recommended: 8h 

set -evx # verbose messages and crash message

WORK_PATH=/work/bb1153/b380887/global_tropics/SAM
FILE_PATH=/scratch/b/b380887/global_tropics/SAM
GRIDS=/pf/b/b380887/cold-point-overshoot/slurm_scripts/process_files/grid_files

# 12-20 km temperature: 0.25deg, 3 hourly
T_IN=$WORK_PATH/SAM_temp_12-20km_winter_ITCZ.nc
T_OUT=$FILE_PATH/SAM_0.25deg_temp_12-20km_winter_ITCZ.nc
cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt $T_IN $T_OUT
