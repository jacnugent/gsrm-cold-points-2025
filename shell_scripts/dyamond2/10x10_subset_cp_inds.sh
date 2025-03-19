#!/bin/bash
# header goes here
# recommended: 50GB mem, 6h 


set -evx # verbose messages and crash message

module load cdo

OUT_PATH=/work/bb1153/b380887/10x10/cp_inds
FILE_PATH=/work/bb1153/b380887/global_tropics/cold_point_indices

declare -a LocArray=(SPC AMZ)
declare -a CoordsArray=("170,180,-15,-5" "-65,-55,-30,-20")
declare -a ModelArray=(SCREAM GEOS SHIELD SAM ICON)

for m in "${ModelArray[@]}"; do
   in_file=$FILE_PATH/$m"_cold_point_inds_remapped.nc"
   for index in "${!LocArray[@]}"; do
       loc="${LocArray[$index]}"
       coords="${CoordsArray[$index]}"    
       out_file=$OUT_PATH/$m"_cp_inds_"$loc".nc"
       cdo sellonlatbox,$coords $in_file $out_file
   done
done

