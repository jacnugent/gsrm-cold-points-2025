#!/bin/bash
# header goes here
# recommended: 50GB mem, 6h 


set -evx # verbose messages and crash message

module load cdo

FILE_PATH=/work/bb1153/b380887/global_tropics
# FILE_PATH=/scratch/b/b380887
OUT_PATH=/scratch/b/b380887

declare -a LocArray=(SCA TIM AMZ SPC)  
declare -a CoordsArray=("20,30,-17,-7" "120,130,-12,-2"  "-65,-55,-30,-20" "170,180,-15,-5")
declare -a ModelArray=(SCREAM GEOS ICON)
declare -a VarArray3D=(zg) #qs) #temp temp_0.25deg)
declare -a VarArray2D=(pr) # OLR)

# 3D variables 
for m in "${ModelArray[@]}"; do
   for v in "${VarArray3D[@]}"; do
       in_file=$FILE_PATH/$m/$m"_"$v"_12-20km_winter_ITCZ.nc"
       for index in "${!LocArray[@]}"; do
           loc="${LocArray[$index]}"
           coords="${CoordsArray[$index]}"    
           out_file=$OUT_PATH/$m"_"$v"_12-20km_winter_"$loc".nc"
           cdo sellonlatbox,$coords $in_file $out_file
       done
    done
done

# 2D variables 
for m in "${ModelArray[@]}"; do
   for v in "${VarArray2D[@]}"; do
       if [ $m == "ICON" ] ; then
           v="pracc"
       fi
       in_file=$FILE_PATH/$m/$m"_"$v"_winter_ITCZ.nc"
       for index in "${!LocArray[@]}"; do
           loc="${LocArray[$index]}"
           coords="${CoordsArray[$index]}"    
           out_file=$OUT_PATH/$m"_"$v"_winter_"$loc".nc"
           cdo sellonlatbox,$coords $in_file $out_file
       done
    done
done

