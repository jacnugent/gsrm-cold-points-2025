#!/bin/bash
#SBATCH --job-name=icon_w
#SBATCH --partition=prepost
#SBATCH --ntasks=1
#SBATCH --mem=100GB
#SBATCH --time=08:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=icon_w.eo%j
#SBATCH --error=icon_w_err.eo%j

set -evx # verbose messages and crash message

IN_PATH=/work/dicad/cmip6-dev/data4freva/model/global/dyamond/DYAMOND_WINTER
MODEL_PATH=MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos
OUT_PATH=/scratch/b/b380887/global_tropics/SAM
GRID_FILE=/work/bk1040/DYAMOND/data/winter_data/DYAMOND_WINTER/MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos/fx/gn/grid.nc

LON0=0
LON1=360
LAT0=-30
LAT1=10

export GRIB_DEFINITION_PATH=/sw/rhel6-x64/eccodes/definitions

# get levels from vlevs.nc (DYAMOND1 file)
levels="45,38,34"

for f in $IN_PATH/$MODEL_PATH/3hr/wa/r1i1p1f1/ml/gn/*202002*; do
    fname=$(basename $f)
    out_file=$OUT_PATH/"14_17_20_"$fname
    cdo -f nc -sellonlatbox,$LON0,$LON1,$LAT0,$LAT1 -sellevel,$levels -setgrid,$GRID_FILE $f $out_file  
done

