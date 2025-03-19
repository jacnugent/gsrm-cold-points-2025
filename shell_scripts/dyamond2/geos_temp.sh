#!/bin/bash
# header goes here
# recommended: 20GB mem, 8h 

set -evx # verbose messages and crash message
module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=NASA/GEOS-3km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/GEOS

LON0=0
LON1=360
LAT0=-30
LAT1=10

# ~12-20 km
levels="79/115"

# 1/30
for f in $IN_PATH/$MODEL_PATH/1hr/ta/r1i1p1f1/ml/gn/*_2020013*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-_20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels $f $out_file  
done

# All of Feb
for f in $IN_PATH/$MODEL_PATH/1hr/ta/r1i1p1f1/ml/gn/*_202002*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-_20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels $f $out_file
done

