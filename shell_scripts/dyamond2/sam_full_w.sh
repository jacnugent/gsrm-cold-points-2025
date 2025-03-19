#!/bin/bash
# header goes here
# recommended: 25GB mem, 8h 

set -evx # verbose messages and crash message

module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=SBU/gSAM-4km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/SAM

LON0=0
LON1=360
LAT0=-30
LAT1=10

# vertical velocity
for f in $IN_PATH/$MODEL_PATH/3hr/wa/r1i1p1f1/ml/gn/*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-20_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,46/61 $f $out_file  
done
