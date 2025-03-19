#!/bin/bash
# header goes here
# recommended: 20GB mem, 4h (longer?)


module load cdo

set -evx # verbose messages and crash message

FILE_PATH=/work/bb1153/b380887/global_tropics/SHiELD
OUT_PATH=/scratch/b/b380887

declare -a LocArray=(SPC AMZ SCA TIM)
declare -a CoordsArray=("170,180,-15,-5" "-65,-55,-30,-20" "20,30,-17,-7" "120,130,-12,-2")
declare -a VarArray3D=(qs temp_0.25deg zg)
declare -a VarArray2D=(pr OLR)


# loop through regions, then 3d & 2d variables

for index in "${!LocArray[@]}"; do
   loc="${LocArray[$index]}"
   coords="${CoordsArray[$index]}" 
   
   for v in "${VarArray3D[@]}"; do
       in_file_3d=$OUT_PATH/SHiELD/SHIELD_$v"_12-20km_winter_ITCZ.nc"
       # in_file_3d=$FILE_PATH/SHIELD_$v"_12-20km_winter_ITCZ.nc"
       out_file_3d=$OUT_PATH/SHIELD_$v"_12-20km_winter_"$loc".nc"
       cdo sellonlatbox,$coords $in_file_3d $out_file_3d
    done
    
   for x in "${VarArray2D[@]}"; do
       in_file_2d=$FILE_PATH/SHIELD_$x"_winter_ITCZ.nc"
       out_file_2d=$OUT_PATH/SHIELD_$x"_winter_"$loc".nc"
       cdo sellonlatbox,$coords $in_file_2d $out_file_2d
    done

done

