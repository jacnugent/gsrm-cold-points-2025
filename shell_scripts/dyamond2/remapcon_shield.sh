#!/bin/bash
# header goes here
# recommended: 20GB mem, 4h 

set -evx # verbose messages and crash message

module load cdo

FILE_PATH=/scratch/b/b380887/SHiELD
GRIDS=/home/b/b380887/cold-point-overshoot/slurm_scripts/process_files/grid_files
GRID_FILE=/work/ka1081/DYAMOND_WINTER/NOAA/SHiELD-3km/DW-ATM/atmos/fx/grid/r1i1p1f1/2d/gn/grid_fx_SHiELD-3km_DW-CPL_r1i1p1f1_2d_gn_fx.nc



# --- geopotential height: 0.25deg (each region) ----
REG_PATH=/work/bb1153/b380887/10x10

ZG_IN1=$REG_PATH/TWP/SHIELD_zg_12-20km_winter_TWP.nc
ZG_OUT1=$REG_PATH/TWP/SHIELD_zg_0.25deg_12-20km_winter_TWP.nc

ZG_IN2=$REG_PATH/TIM/SHIELD_zg_12-20km_winter_TIM.nc
ZG_OUT2=$REG_PATH/TIM/SHIELD_zg_0.25deg_12-20km_winter_TIM.nc

ZG_IN3=$REG_PATH/SCA/SHIELD_zg_12-20km_winter_SCA.nc
ZG_OUT3=$REG_PATH/SCA/SHIELD_zg_0.25deg_12-20km_winter_SCA.nc

ZG_IN4=$REG_PATH/SAV/SHIELD_zg_12-20km_winter_SAV.nc
ZG_OUT4=$REG_PATH/SAV/SHIELD_zg_0.25deg_12-20km_winter_SAV.nc

cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt -setgrid,$GRID_FILE $ZG_IN1 $ZG_OUT1
cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt -setgrid,$GRID_FILE $ZG_IN2 $ZG_OUT2
cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt -setgrid,$GRID_FILE $ZG_IN3 $ZG_OUT3
cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt -setgrid,$GRID_FILE $ZG_IN4 $ZG_OUT4


# temperature: 0.25deg
TEMP_IN=$FILE_PATH/SHIELD_temp_12-20km_winter_ITCZ_days10-40.nc
TEMP_OUT=$FILE_PATH/SHIELD_temp_0.25deg_12-20km_winter_ITCZ_days10-40.nc
cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt -setgrid,$GRID_FILE $TEMP_IN $TEMP_OUT

# geopotential height: 0.25deg
ZG_IN=$FILE_PATH/SHIELD_zg_12-20km_winter_ITCZ_days10-40.nc
ZG_OUT=$FILE_PATH/SHIELD_zg_0.25deg_12-20km_winter_ITCZ_days10-40.nc
cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt -setgrid,$GRID_FILE $ZG_IN $ZG_OUT
