#!/bin/bash
# header goes here
# recommended: 100GB mem, 9h 

set -evx # verbose messages and crash message
module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER/SBU/gSAM-4km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/SAM

LON0=0
LON1=360
LAT0=-30
LAT1=10

declare -a VarArray15min=(pracc) #clivi qsvi qgvi) # rltacc pracc)

# 15 min vars
for v in "${VarArray15min[@]}"; do
    for f in $IN_PATH/15min/$v/r1i1p1f1/2d/gn/*; do
        fname=$(basename $f)
        out_file=$OUT_PATH/$fname
        cdo sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 $f $out_file  
    done
done
