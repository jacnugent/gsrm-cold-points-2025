#!/bin/bash
#SBATCH --job-name=scream_z
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=20GB
#SBATCH --time=04:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=scream_z.eo%j
#SBATCH --error=scream_z_err.eo%j

set -evx # verbose messages and crash message

module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=LLNL/SCREAM-3km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/SCREAM
GRID_FILE=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER/LLNL/SCREAM-3km/DW-ATM/atmos/fx/gn/grid.nc

LON0=0
LON1=360
LAT0=-30
LAT1=10

temp_path=$IN_PATH/$MODEL_PATH/3hr/ta/r1i1p1f1/ml/gn
qv_path=$IN_PATH/$MODEL_PATH/3hr/hus/r1i1p1f1/ml/gn

tin1=$temp_path/ta_3hr_SCREAM-3km_DW-ATM_r1i1p1f1_ml_gn_20200130000000-20200130210000.nc
tin2=$temp_path/ta_3hr_SCREAM-3km_DW-ATM_r1i1p1f1_ml_gn_20200214000000-20200214210000.nc
tin3=$temp_path/ta_3hr_SCREAM-3km_DW-ATM_r1i1p1f1_ml_gn_20200228000000-20200228210000.nc

qvin1=$qv_path/hus_3hr_SCREAM-3km_DW-ATM_r1i1p1f1_ml_gn_20200130000000-20200130210000.nc
qvin2=$qv_path/hus_3hr_SCREAM-3km_DW-ATM_r1i1p1f1_ml_gn_20200214000000-20200214210000.nc
qvin3=$qv_path/hus_3hr_SCREAM-3km_DW-ATM_r1i1p1f1_ml_gn_20200228000000-20200228210000.nc

cdo -timmean -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgrid,$GRID_FILE $tin1 $OUT_PATH/temp_1-30.nc
cdo -timmean -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgrid,$GRID_FILE $tin2 $OUT_PATH/temp_2-14.nc
cdo -timmean -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgrid,$GRID_FILE $tin3 $OUT_PATH/temp_2-28.nc

cdo -timmean -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgrid,$GRID_FILE $qvin1 $OUT_PATH/qv_1-30.nc
cdo -timmean -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgrid,$GRID_FILE $qvin2 $OUT_PATH/qv_2-14.nc
cdo -timmean -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgrid,$GRID_FILE $qvin3 $OUT_PATH/qv_2-28.nc


