#!/bin/bash
# header goes here
# recommended: 20GB mem, 4h 

set -evx # verbose messages and crash message

module load cdo

FILE_PATH=/work/bb1153/b380887/global_tropics/SCREAM
OUT_PATH=/scratch/b/b380887/SCREAM
GRIDS=/home/b/b380887/cold-point-overshoot/slurm_scripts/process_files/grid_files

# temperature: 0.25deg
TEMP_IN=$OUT_PATH/SCREAM_temp_12-20km_winter_ITCZ_day_10-40.nc
TEMP_OUT=$OUT_PATH/SCREAM_temp_0.25deg_12-20km_winter_ITCZ_days10-40.nc
cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt $TEMP_IN $TEMP_OUT
