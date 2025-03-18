#!/bin/bash
#SBATCH --job-name=sub10_ns
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --time=04:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=sub10_ns.eo%j
#SBATCH --error=sub10_ns_err.eo%j

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
# declare -a NVarArray=(pr FWP)

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

# for v in "${SVarArray3D[@]}"; do
#    in_file=$FILE_PATH/SAM/SAM_$v"_12-20km_winter_ITCZ.nc"
#    for index in "${!LocArray[@]}"; do
#        loc="${LocArray[$index]}"
#        coords="${CoordsArray[$index]}"    
#        out_file=$OUT_PATH/SAM/SAM_$v"_12-20km_winter_"$loc".nc"
#        cdo sellonlatbox,$coords $in_file $out_file
#    done
# done

# # NICAM
# for v in "${NVarArray[@]}"; do
#    in_file=$FILE_PATH/NICAM/native/NICAM_$v"_winter_ITCZ.nc"
#    for index in "${!LocArray[@]}"; do
#        loc="${LocArray[$index]}"
#        coords="${CoordsArray[$index]}"
#        out_file=$OUT_PATH/NICAM_$v"_winter_"$loc".nc"
#        cdo sellonlatbox,$coords $in_file $out_file
#    done
# done

# Get TWP w for Rachel
# cdo sellonlatbox,143,153,-5,5 $FILE_PATH/SAM/SAM_w_14_17_20km_winter_ITCZ.nc $OUT_PATH/SAM_w_14_17_20km_winter_TWP.nc
# cdo sellonlatbox,143,153,-5,5 $FILE_PATH/NICAM/native/NICAM_w_14_17_20km_winter_ITCZ.nc $OUT_PATH/NICAM_w_14_17_20km_winter_TWP.nc

