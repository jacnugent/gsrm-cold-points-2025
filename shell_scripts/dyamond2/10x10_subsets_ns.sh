#!/bin/bash
# header goes here
# recommended: 4h time


set -evx # verbose messages and crash message

FILE_PATH=/work/bb1153/b380887/global_tropics
OUT_PATH=/scratch/b/b380887

# declare -a LocArray=(TWP SCA SAV TIM)
# declare -a CoordsArray=("143,153,-5,5" "20,30,-17,-7" "-63,-53,-25,-15", "120,130,-12,-2")
# declare -a LocArray=(SCA2 SAV2 TIM)
# declare -a CoordsArray=("20,30,-17,-7" "-63,-53,-25,-15", "120,130,-12,-2")
declare -a LocArray=(SPC AMZ)
declare -a CoordsArray=("170,180,-15,-5" "-65,-55,-30,-20")
declare -a SVarArray3D=(0.25deg_temp temp qi) 
declare -a SVarArray2D=(pracc) #OLR) 

# SAM
for v in "${SVarArray2D[@]}"; do
   in_file=$FILE_PATH/SAM/SAM_$v"_winter_ITCZ.nc"
   for index in "${!LocArray[@]}"; do
       loc="${LocArray[$index]}"
       coords="${CoordsArray[$index]}"    
       out_file=$OUT_PATH/SAM/SAM_$v"_winter_"$loc".nc"
       cdo sellonlatbox,$coords $in_file $out_file
   done
done

for v in "${SVarArray3D[@]}"; do
   in_file=$FILE_PATH/SAM/SAM_$v"_12-20km_winter_ITCZ.nc"
   for index in "${!LocArray[@]}"; do
       loc="${LocArray[$index]}"
       coords="${CoordsArray[$index]}"    
       out_file=$OUT_PATH/SAM/SAM_$v"_12-20km_winter_"$loc".nc"
       cdo sellonlatbox,$coords $in_file $out_file
   done
done

