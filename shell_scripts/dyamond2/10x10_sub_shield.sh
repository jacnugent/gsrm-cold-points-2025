#!/bin/bash
#SBATCH --job-name=sh3_sub10
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=20GB
#SBATCH --time=04:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=sh_sub10_all.eo%j
#SBATCH --error=sh_sub10_all_err.eo%j

module load cdo

set -evx # verbose messages and crash message

FILE_PATH=/work/bb1153/b380887/global_tropics/SHiELD
OUT_PATH=/scratch/b/b380887

# declare -a LocArray=(TWP SCA SAV TIM)
# declare -a CoordsArray=("143,153,-5,5" "20,30,-17,-7" "-63,-53,-25,-15" "120,130,-12,-2")
# declare -a LocArray=(SCA SAV TIM)
# declare -a CoordsArray=("20,30,-17,-7" "-63,-53,-25,-15" "120,130,-12,-2")
# declare -a LocArray=(SPC AMZ SCA TIM)
# declare -a CoordsArray=("170,180,-15,-5" "-65,-55,-30,-20" "20,30,-17,-7" "120,130,-12,-2")
declare -a LocArray=(SPC AMZ)
declare -a CoordsArray=("170,180,-15,-5" "-65,-55,-30,-20")
declare -a VarArray3D=(qs) # temp_0.25deg zg)
declare -a VarArray2D=(pr) #OLR)


# loop through regions, then 3d & 2d variables

for index in "${!LocArray[@]}"; do
   loc="${LocArray[$index]}"
   coords="${CoordsArray[$index]}" 
   
   # for v in "${VarArray3D[@]}"; do
   #     in_file_3d=$OUT_PATH/SHiELD/SHIELD_$v"_12-20km_winter_ITCZ.nc"
   #     # in_file_3d=$FILE_PATH/SHIELD_$v"_12-20km_winter_ITCZ.nc"
   #     out_file_3d=$OUT_PATH/SHIELD_$v"_12-20km_winter_"$loc".nc"
   #     cdo sellonlatbox,$coords $in_file_3d $out_file_3d
   #  done
    
   for x in "${VarArray2D[@]}"; do
       in_file_2d=$FILE_PATH/SHIELD_$x"_winter_ITCZ.nc"
       out_file_2d=$OUT_PATH/SHIELD_$x"_winter_"$loc".nc"
       cdo sellonlatbox,$coords $in_file_2d $out_file_2d
    done

done

