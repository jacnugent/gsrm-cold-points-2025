#!/bin/bash
#SBATCH --job-name=3d_sub_shield
#SBATCH --partition=interactive
#SBATCH --mem=20GB
#SBATCH --ntasks=1
#SBATCH --time=02:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=3d_sub_shield.eo%j
#SBATCH --error=3d_sub_shield_err.eo%j

set -evx # verbose messages and crash message

module load cdo

IN_PATH=/work/ka1081/DYAMOND_WINTER/NOAA/SHiELD-3km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/SHiELD
WORK_PATH=/work/bb1153/b380887/global_tropics/SHiELD
GRID_FILE=/work/ka1081/DYAMOND_WINTER/NOAA/SHiELD-3km/DW-ATM/atmos/fx/grid/r1i1p1f1/2d/gn/grid_fx_SHiELD-3km_DW-CPL_r1i1p1f1_2d_gn_fx.nc

LON0=0
LON1=360
LAT0=-30
LAT1=10

declare -a VarArray=(grplmxrat snowmxrat hus) #zg) #ta) #grplmxrat hus) #wa zg cli) # ta

# Get the last day for snow
f=$IN_PATH/3hr/snowmxrat/r1i1p1f1/ml/gn/snowmxrat_3hr_SHiELD-3km_DW-ATM_r1i1p1f1_ml_gn_20200228030000-20200229000000.nc
fname=$(basename $f)
out_file=$OUT_PATH/"12-20_"$fname
if [ ! -f $out_file ]; then
    cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,12/32 -setgridtype,unstructured -setgrid,$GRID_FILE $f $out_file
fi

# ## Get last few days for zg ##
# # 2/19-2/20 for zg
# f=$IN_PATH/3hr/zg/r1i1p1f1/ml/gn/zg_3hr_SHiELD-3km_DW-ATM_r1i1p1f1_ml_gn_20200219030000-20200220000000.nc
# fname=$(basename $f)
# out_file=$OUT_PATH/"12-20_"$fname
# if [ ! -f $out_file ]; then
#     cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,12/32 -setgridtype,unstructured -setgrid,$GRID_FILE $f $out_file
# fi
    
# # 2/20 --> for zg
# for f in $IN_PATH/3hr/zg/r1i1p1f1/ml/gn/*_2020022*; do
#     fname=$(basename $f)
#     out_file=$OUT_PATH/"12-20_"$fname
#     # only get it if it doesn't exist 
#     if [ ! -f $out_file ]; then
#         cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,12/32 -setgridtype,unstructured -setgrid,$GRID_FILE $f $out_file
#     fi
# done
    
    
# ## skipping first 10 days ###

# for v in "${VarArray[@]}"; do
#     # Jan 30-31
#     for f in $IN_PATH/3hr/$v/r1i1p1f1/ml/gn/*_2020013*; do
#         fname=$(basename $f)
#         out_file=$OUT_PATH/"12-20_"$fname
#         # only get it if it doesn't exist 
#         if [ ! -f $out_file ]; then
#             cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,12/32 -setgridtype,unstructured -setgrid,$GRID_FILE $f $out_file
#         fi
#     done
    
#     # Feb
#     for f in $IN_PATH/3hr/$v/r1i1p1f1/ml/gn/*202002*; do
#         fname=$(basename $f)
#         out_file=$OUT_PATH/"12-20_"$fname
#         # only get it if it doesn't exist 
#         if [ ! -f $out_file ]; then
#             cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,12/32 -setgridtype,unstructured -setgrid,$GRID_FILE $f $out_file
#         fi
#     done
# done


# # cat right away
# cdo cat $OUT_PATH/*zg* $OUT_PATH/SHIELD_zg_12-20km_winter_ITCZ_days10-40.nc

# # coarsen to 0.25deg right away
# GRIDS=/home/b/b380887/cold-point-overshoot/slurm_scripts/process_files/grid_files
# TEMP_IN=$OUT_PATH/SHIELD_zg_12-20km_winter_ITCZ_days10-40.nc
# TEMP_OUT=$OUT_PATH/SHIELD_zg_0.25deg_12-20km_winter_ITCZ_days10-40.nc
# cdo remapcon,$GRIDS/itcz_0.25deg_grid.txt -setgrid,$GRID_FILE $TEMP_IN $TEMP_OUT

# # 10x10 subset
# declare -a LocArray=(TWP SCA SAV TIM)
# declare -a CoordsArray=("143,153,-5,5" "20,30,-17,-7" "-63,-53,-25,-15" "120,130,-12,-2")
# # in_file=$WORK_PATH/SHIELD_zg_12-20km_winter_ITCZ_days10-40.nc
# in_file=$TEMP_OUT
# for index in "${!LocArray[@]}"; do
#    loc="${LocArray[$index]}"
#    coords="${CoordsArray[$index]}" 
#    out_file=$OUT_PATH/SHIELD_zg_0.25deg_12-20km_winter_$loc".nc"
#    cdo sellonlatbox,$coords $in_file $out_file
# done



# # TWP, full 3d
# IN_PATH=/work/ka1081/DYAMOND_WINTER/NOAA/SHiELD-3km/DW-ATM/atmos/3hr/zg/r1i1p1f1/ml/gn
# OUT_PATH=/scratch/b/b380887/qi_full_3d

# LON0=143
# LON1=153
# LAT0=-5
# LAT1=5

# in_219=$IN_PATH/zg_3hr_SHiELD-3km_DW-ATM_r1i1p1f1_ml_gn_20200219030000-20200220000000.nc
# in_220=$IN_PATH/zg_3hr_SHiELD-3km_DW-ATM_r1i1p1f1_ml_gn_20200220030000-20200221000000.nc
# in_221=$IN_PATH/zg_3hr_SHiELD-3km_DW-ATM_r1i1p1f1_ml_gn_20200221030000-20200222000000.nc

# out_219=$OUT_PATH/SHIELD_TWP_zg_0219-0220.nc
# out_220=$OUT_PATH/SHIELD_TWP_zg_0220-0221.nc
# out_221=$OUT_PATH/SHIELD_TWP_zg_0221-0222.nc

# cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgridtype,unstructured -setgrid,$GRID_FILE $in_219 $out_219
# cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgridtype,unstructured -setgrid,$GRID_FILE $in_220 $out_220
# cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgridtype,unstructured -setgrid,$GRID_FILE $in_221 $out_221
