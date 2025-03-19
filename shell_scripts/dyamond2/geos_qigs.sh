#!/bin/bash
# header goes here
# recommended: 20GB mem, 11h 


set -evx # verbose messages and crash message
module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=NASA/GEOS-3km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/GEOS

LON0=0
LON1=360
LAT0=-30
LAT1=10

HOURS="0,3,6,9,12,15,18,21"

# ~12-20 km
levels="79/115"


# ----- ice -----
# 1/30-1/31
for f in $IN_PATH/$MODEL_PATH/1hr/cli/r1i1p1f1/ml/gn/*_2020013*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-_20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels -selhour,$HOURS $f $out_file  
done

# all of Feb
for f in $IN_PATH/$MODEL_PATH/1hr/cli/r1i1p1f1/ml/gn/*_202002*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-_20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels -selhour,$HOURS $f $out_file
done


# ----- snow -----
# 1/30-1/31
for f in $IN_PATH/$MODEL_PATH/1hr/snowmxrat/r1i1p1f1/ml/gn/*_2020013*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-_20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels -selhour,$HOURS $f $out_file  
done

# all of Feb
for f in $IN_PATH/$MODEL_PATH/1hr/snowmxrat/r1i1p1f1/ml/gn/*_202002*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-_20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels -selhour,$HOURS $f $out_file
done


# ----- graupel -----
# 1/30-1/31
for f in $IN_PATH/$MODEL_PATH/1hr/grplmxrat/r1i1p1f1/ml/gn/*_2020013*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-_20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels $f $out_file  
done

# all of Feb
for f in $IN_PATH/$MODEL_PATH/1hr/grplmxrat/r1i1p1f1/ml/gn/*_202002*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-_20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels $f $out_file
done
