#!/bin/bash
# header goes here
# recommended: 20GB mem, 8h 

set -evx # verbose messages and crash message

module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=NASA/GEOS-3km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/GEOS

declare -a LocArray=(TWP SCA SAV TIM)
declare -a CoordsArray=("143,153,-5,5" "20,30,-17,-7" "-63,-53,-25,-15" "120,130,-12,-2")

# ~12-20 km
levels="79/115"

# January 30-31
for f in $IN_PATH/$MODEL_PATH/1hr/hus/r1i1p1f1/ml/gn/*_2020013*; do
   fname=$(basename $f)
   for index in "${!LocArray[@]}"; do
       loc="${LocArray[$index]}"
       coords="${CoordsArray[$index]}"    
       out_file=$OUT_PATH/$loc"_12-20km_"$fname
       cdo -f nc -sellonlatbox,$coords -sellevidx,$levels $f $out_file
   done
done

# February
for f in $IN_PATH/$MODEL_PATH/1hr/hus/r1i1p1f1/ml/gn/*_202002*; do
   fname=$(basename $f)
   for index in "${!LocArray[@]}"; do
       loc="${LocArray[$index]}"
       coords="${CoordsArray[$index]}"    
       out_file=$OUT_PATH/$loc"_12-20km_"$fname
       cdo -f nc -sellonlatbox,$coords -sellevidx,$levels $f $out_file
   done
done
