#!/bin/bash
# header goes here
# recommended: 20GB mem, 8h 

set -evx # verbose messages and crash message

module load cdo

IN_PATH=/work/ka1081/DYAMOND_WINTER/NOAA/SHiELD-3km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/SHiELD
GRID_FILE=/work/ka1081/DYAMOND_WINTER/NOAA/SHiELD-3km/DW-ATM/atmos/fx/grid/r1i1p1f1/2d/gn/grid_fx_SHiELD-3km_DW-CPL_r1i1p1f1_2d_gn_fx.nc

LON0=0
LON1=360
LAT0=-30
LAT1=10 

declare -a VarArray15min=(pr) #rlut)

# 1/30-1/31
for v in "${VarArray15min[@]}"; do
    for f in $IN_PATH/15min/$v/r1i1p1f1/pl/gn/*_2020013*; do
        fname=$(basename $f)
        out_file=$OUT_PATH/$fname
        cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgridtype,unstructured -setgrid,$GRID_FILE $f $out_file
    done
done

# All of February
for v in "${VarArray15min[@]}"; do
    for f in $IN_PATH/15min/$v/r1i1p1f1/pl/gn/*_202002*; do
        fname=$(basename $f)
        out_file=$OUT_PATH/$fname
        cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgridtype,unstructured -setgrid,$GRID_FILE $f $out_file
    done
done


# Get the geopotential heights for one file so you can get a rough estimate of the 3D indices needed for 12-20 km
in_file_zg=/work/ka1081/DYAMOND_WINTER/NOAA/SHiELD-3km/DW-ATM/atmos/3hr/zg/r1i1p1f1/ml/gn/zg_3hr_SHiELD-3km_DW-ATM_r1i1p1f1_ml_gn_20200214030000-20200215000000.nc
out_file_zg=$OUT_PATH/test_zg_ITCZ.nc
cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgridtype,unstructured -setgrid,$GRID_FILE $in_file_zg $out_file_zg
