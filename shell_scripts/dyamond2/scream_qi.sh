#!/bin/bash
#SBATCH --job-name=scream_qi
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=20GB
#SBATCH --time=04:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=scream_qi.eo%j
#SBATCH --error=scream_qi_err.eo%j

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

# 12-20 km
levels="23/55"

# Jan 30-31
# for f in $IN_PATH/$MODEL_PATH/3hr/cli/r1i1p1f1/ml/gn/*; do
for f in $IN_PATH/$MODEL_PATH/3hr/cli/r1i1p1f1/ml/gn/*_2020013*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels -setgrid,$GRID_FILE $f $out_file
done

# All of Feb
for f in $IN_PATH/$MODEL_PATH/3hr/cli/r1i1p1f1/ml/gn/*_202002*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-20km_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,$levels -setgrid,$GRID_FILE $f $out_file
done
