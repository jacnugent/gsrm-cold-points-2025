#!/bin/bash
# header goes here
# recommended: 100GB mem, 8h 

set -evx # verbose messages and crash message

module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/ICON
GRID_FILE=/work/bk1040/DYAMOND/data/winter_data/DYAMOND_WINTER/MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos/fx/gn/grid.nc

LON0=0
LON1=360
LAT0=-30
LAT1=10

export GRIB_DEFINITION_PATH=/sw/rhel6-x64/eccodes/definitions

# get levels from vlevs.nc (DYAMOND1 file)
#for f in $IN_PATH/$MODEL_PATH/3hr/ta/r1i1p1f1/ml/gn/*; do
# 2/20 onward
for f in $IN_PATH/$MODEL_PATH/3hr/ta/r1i1p1f1/ml/gn/*_2020022*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-20_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevel,34/50 -setgrid,$GRID_FILE $f $out_file  
done

