#!/bin/bash
#SBATCH --job-name=cat_geos
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --time=06:00:00
#SBATCH --mem=20GB
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=cat.eo%j
#SBATCH --error=cat_err.eo%j

set -evx # verbose messages and crash message
module load cdo 

FILE_PATH=/scratch/b/b380887/GEOS
HOURS="0,3,6,9,12,15,18,21"

# for 3d variables - select every 3 hours (match other DYAMOND files)
# cdo -selhour,$HOURS -cat $FILE_PATH/*grplmxrat*.nc $FILE_PATH/GEOS_qg_winter_ITCZ.nc 
# cdo -selhour,$HOURS -cat $FILE_PATH/*ta*.nc $FILE_PATH/GEOS_temp_winter_ITCZ.nc 

# already selected every 3 hours on these
# cdo -cat $FILE_PATH/*snowmx*.nc $FILE_PATH/GEOS_qs_12-20km_winter_ITCZ.nc 
# cdo -cat $FILE_PATH/*cli*.nc $FILE_PATH/GEOS_qi_12-20km_winter_ITCZ.nc 
# cdo -cat $FILE_PATH/*zg*.nc $FILE_PATH/GEOS_zg_12-20km_winter_ITCZ.nc 

# # --- temp - sub 10x10 for height in the same script ---
# declare -a LocArray=(SCA TIM AMZ SPC)  
# declare -a CoordsArray=("20,30,-17,-7" "120,130,-12,-2"  "-65,-55,-30,-20" "170,180,-15,-5")
# in_file=$FILE_PATH/GEOS_zg_12-20km_winter_ITCZ.nc 
# for index in "${!LocArray[@]}"; do
#    loc="${LocArray[$index]}"
#    coords="${CoordsArray[$index]}"    
#    out_file=$FILE_PATH/$m"_"$v"_12-20km_winter_"$loc".nc"
#    cdo sellonlatbox,$coords $in_file $out_file
# done

# 2d
# cdo cat $FILE_PATH/qsvi*.nc $FILE_PATH/GEOS_SWP_winter_ITCZ.nc
# cdo cat $FILE_PATH/qgvi*.nc $FILE_PATH/GEOS_GWP_winter_ITCZ.nc
# cdo cat $FILE_PATH/rlut_*.nc $FILE_PATH/GEOS_OLR_winter_ITCZ.nc
cdo cat $FILE_PATH/pr*.nc $FILE_PATH/GEOS_pr_winter_ITCZ.nc

# for 3d variables - make it 3 hourly right away
# cdo -timselmean,3,0 -cat $FILE_PATH/*zg*.nc $FILE_PATH/GEOS_zg_winter_ITCZ.nc
# cdo -timselmean,3,0 -cat $FILE_PATH/*ta*.nc $FILE_PATH/GEOS_temp_12-20km_winter_ITCZ_days10-40.nc
# cdo -timselmean,3,0 -cat $FILE_PATH/*wa*.nc $FILE_PATH/GEOS_w_12-20km_winter_ITCZ_days10-40.nc
# cdo -timselmean,3,0 -cat $FILE_PATH/*cli*.nc $FILE_PATH/GEOS_qi_12-20km_winter_ITCZ_days10-40.nc
# cdo -timselmean,3,0 -cat $FILE_PATH/*grplmxrat*.nc $FILE_PATH/GEOS_qg_12-20km_winter_ITCZ_days10-40.nc



