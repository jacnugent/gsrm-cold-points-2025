#!/bin/bash
#SBATCH --job-name=sam_T
#SBATCH --partition=prepost
#SBATCH --ntasks=1
#SBATCH --time=08:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=sam_T.eo%j
#SBATCH --error=sam_T_err.eo%j

set -evx # verbose messages and crash message

IN_PATH=/work/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=SBU/SAM2-4km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/global_tropics/SAM

LON0=0
LON1=360
LAT0=-30
LAT1=10

for f in $IN_PATH/$MODEL_PATH/3hr/ta/r1i1p1f1/ml/gn/*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"12-20_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevidx,46/61 $f $out_file  
done
