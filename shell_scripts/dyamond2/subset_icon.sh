#!/bin/bash
#SBATCH --job-name=20icon_gt2d
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=100GB
#SBATCH --time=08:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=20icon_2d.eo%j
#SBATCH --error=20icon_2d_err.eo%j

set -evx # verbose messages and crash message
module load cdo

IN_PATH=/work/dicad/from_Mistral/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/ICON
GRID_FILE=/work/bk1040/DYAMOND/data/winter_data/DYAMOND_WINTER/MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos/fx/gn/grid.nc

# Changed to GT
LON0=0
LON1=360
LAT0=-30
LAT1=30

export GRIB_DEFINITION_PATH=/sw/rhel6-x64/eccodes/definitions

# 15 min vars
declare -a VarArray15min=(pracc) #rltacc) #qsvi qgvi) #clivi pracc rltacc)

# 1/20 to 1/29
for v in "${VarArray15min[@]}"; do
    for f in $IN_PATH/$MODEL_PATH/15min/$v/r1i1p1f1/2d/gn/*_2020012*; do
        fname=$(basename $f)
        out_file=$OUT_PATH/$fname
        cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgrid,$GRID_FILE $f $out_file
    done
done

# # 1/30 to 1/31
# for v in "${VarArray15min[@]}"; do
#     for f in $IN_PATH/$MODEL_PATH/15min/$v/r1i1p1f1/2d/gn/*_2020013*; do
#         fname=$(basename $f)
#         out_file=$OUT_PATH/$fname
#         cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgrid,$GRID_FILE $f $out_file
#     done
# done

# # All of Feb
# for v in "${VarArray15min[@]}"; do
#     for f in $IN_PATH/$MODEL_PATH/15min/$v/r1i1p1f1/2d/gn/*_202002*; do
#         fname=$(basename $f)
#         out_file=$OUT_PATH/$fname
#         cdo -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -setgrid,$GRID_FILE $f $out_file
#     done
# done
