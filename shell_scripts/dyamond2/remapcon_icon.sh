#!/bin/bash
# header goes here
# recommended: 100GB mem, 5h 

set -evx # verbose messages and crash message

module load cdo
export GRIB_DEFINITION_PATH=/sw/rhel6-x64/eccodes/definitions

FILE_PATH=/work/bb1153/b380887/global_tropics/ICON
GRIDS=/home/b/b380887/cold-point-overshoot/slurm_scripts/process_files/grid_files
GRID_FILE=/work/bk1040/DYAMOND/data/winter_data/DYAMOND_WINTER/MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos/fx/gn/grid.nc

# Temperature: 0.25deg
TEMP_IN=$FILE_PATH/ICON_temp_12-20km_winter_ITCZ.nc
TEMP_OUT=$FILE_PATH/ICON_temp_0.25deg_12-20km_winter_ITCZ.nc
cdo -remapcon,$GRIDS/itcz_0.25deg_grid.txt -setgrid,$GRID_FILE $TEMP_IN $TEMP_OUT

