#!/bin/bash
# header goes here
# recommended:  8h 

set -evx # verbose messages and crash message

IN_PATH=/work/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=SBU/SAM2-4km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/global_tropics/SAM

LON0=0
LON1=360
LAT0=-30
LAT1=10

for f in $IN_PATH/$MODEL_PATH/3hr/ta/r1i1p1f1/ml/gn/*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-20_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,46/61 $f $out_file  
done
