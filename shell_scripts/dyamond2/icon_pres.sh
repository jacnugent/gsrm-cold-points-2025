#!/bin/bash
#SBATCH --job-name=icon_p
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=100GB
#SBATCH --time=09:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=icon_p.eo%j
#SBATCH --error=icon_p_err.eo%j

set -evx # verbose messages and crash message

module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/ICON
GRID_FILE=/work/bk1040/DYAMOND/data/winter_data/DYAMOND_WINTER/MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos/fx/gn/grid.nc

LON0=0
LON1=360
LAT0=-30
LAT1=10

export GRIB_DEFINITION_PATH=/sw/rhel6-x64/eccodes/definitions

# get levels from vlevs.nc (DYAMOND1 file)

### do this in chunks to skip the first 10 days (save time)
# # Jan 30-31
# for f in $IN_PATH/$MODEL_PATH/3hr/pa/r1i1p1f1/ml/gn/*2020013*; do
#     fname=$(basename $f)
#     out_file=$OUT_PATH/"12-20_"$fname
#     cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevel,34/50 -setgrid,$GRID_FILE $f $out_file  
# done

# # all February
# for f in $IN_PATH/$MODEL_PATH/3hr/pa/r1i1p1f1/ml/gn/*202002*; do
#     fname=$(basename $f)
#     out_file=$OUT_PATH/"12-20_"$fname
#     cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevel,34/50 -setgrid,$GRID_FILE $f $out_file  
# done

# # March 1
# for f in $IN_PATH/$MODEL_PATH/3hr/pa/r1i1p1f1/ml/gn/*20200301*; do
#     fname=$(basename $f)
#     out_file=$OUT_PATH/"12-20_"$fname
#     cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevel,34/50 -setgrid,$GRID_FILE $f $out_file  
# done

### concatenate the files
cdo cat $OUT_PATH/*12-20_*pa* $OUT_PATH/ICON_pa_12-20km_winter_ITCZ_days10-40.nc

### subset by 10x10 region
declare -a LocArray=(TWP SCA SAV TIM)
declare -a CoordsArray=("143,153,-5,5" "20,30,-17,-7" "-63,-53,-25,-15" "120,130,-12,-2")

in_file=$OUT_PATH/ICON_pa_12-20km_winter_ITCZ_days10-40.nc
for index in "${!LocArray[@]}"; do
   loc="${LocArray[$index]}"
   coords="${CoordsArray[$index]}"
   out_file=$OUT_PATH/ICON_pa_12-20km_winter_$loc"_days10-40.nc"
   cdo -sellonlatbox,$coords -setgrid,$GRID_FILE $in_file $out_file
done

