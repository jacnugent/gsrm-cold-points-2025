#!/bin/bash
# header goes here
# recommended: 20GB mem, 4h 

set -evx # verbose messages and crash message
module load cdo

FILE_PATH=/scratch/b/b380887/GEOS
WORK_PATH=/work/bb1153/b380887/global_tropics/GEOS
GRIDS=/home/b/b380887/cold-point-overshoot/slurm_scripts/process_files/grid_files

# geopotential: 0.25deg
ZG_IN=$WORK_PATH/GEOS_zg_12-20km_winter_ITCZ_days10-40.nc
ZG_OUT=$FILE_PATH/GEOS_zg_0.25deg_12-20km_winter_ITCZ_days10-40.nc
cdo -remapcon,$GRIDS/itcz_0.25deg_grid.txt $ZG_IN $ZG_OUT

# temperature: 0.25deg
TEMP_IN=$FILE_PATH/GEOS_temp_12-20km_winter_ITCZ.nc
TEMP_OUT=$FILE_PATH/GEOS_0.25deg_temp_12-20km_winter_ITCZ.nc
cdo -remapcon,$GRIDS/itcz_0.25deg_grid.txt $TEMP_IN $TEMP_OUT
