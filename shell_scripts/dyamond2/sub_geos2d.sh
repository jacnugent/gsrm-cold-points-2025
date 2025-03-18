#!/bin/bash
#SBATCH --job-name=sub_geos_2d
#SBATCH --partition=interactive
#SBATCH --mem=20GB
#SBATCH --ntasks=1
#SBATCH --time=06:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=sub_g.eo%j
#SBATCH --error=sub_g_err.eo%j

set -evx # verbose messages and crash message
module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=NASA/GEOS-3km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/GEOS

LON0=0
LON1=360
LAT0=-30
LAT1=10

# 15 min vars
declare -a VarArray15min=(pr) #clivi qgvi qsvi)

# 1/30-1/31
for v in "${VarArray15min[@]}"; do
    for f in $IN_PATH/$MODEL_PATH/15min/$v/r1i1p1f1/2d/gn/*_2020013*; do
        fname=$(basename $f)
        out_file=$OUT_PATH/$fname
        cdo sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 $f $out_file 
    done
done

# All of February
for v in "${VarArray15min[@]}"; do
    for f in $IN_PATH/$MODEL_PATH/15min/$v/r1i1p1f1/2d/gn/*_202002*; do
        fname=$(basename $f)
        out_file=$OUT_PATH/$fname
        cdo sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 $f $out_file 
    done
done



# # 1/20-1/29 (skip the 1st 5 days)
# for f in $IN_PATH/$MODEL_PATH/15min/rlut/r1i1p1f1/2d/gn/*_2020012*; do
#     fname=$(basename $f)
#     out_file=$OUT_PATH/"12-_20km_"$fname
#     cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 $f $out_file  
# done

# # 1/30-1/31
# for f in $IN_PATH/$MODEL_PATH/15min/rlut/r1i1p1f1/2d/gn/*_2020013*; do
#     fname=$(basename $f)
#     out_file=$OUT_PATH/"12-_20km_"$fname
#     cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 $f $out_file  
# done

# # all of Feb
# for f in $IN_PATH/$MODEL_PATH/15min/rlut/r1i1p1f1/2d/gn/*_202002*; do
#     fname=$(basename $f)
#     out_file=$OUT_PATH/"12-_20km_"$fname
#     cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 $f $out_file
# done

