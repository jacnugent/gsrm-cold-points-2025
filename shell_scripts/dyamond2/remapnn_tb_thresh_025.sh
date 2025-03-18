#!/bin/bash
#SBATCH --job-name=remapnn_tb
#SBATCH --partition=interactive
#SBATCH --mem=100GB
#SBATCH --ntasks=1
#SBATCH --time=03:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=remapnn_tb.eo%j
#SBATCH --error=remapnn_tb_err.eo%j

set -evx # verbose messages and crash message

module load cdo
export GRIB_DEFINITION_PATH=/sw/rhel6-x64/eccodes/definitions

FILE_PATH=/work/bb1153/b380887/global_tropics
GRID_PATH=$FILE_PATH/itcz_grids
OUT_PATH=/scratch/b/b380887

# do it for SAM too for the sake of consistency
# declare -a ModelArray=(SHIELD GEOS SCREAM ICON SAM)
declare -a ModelArray=(ICON SAM)

for m in "${ModelArray[@]}"; do
    # native var path; SHiELD path has the lowercase i
    if [ "$m" = "SHIELD" ]; then
       native_file=$FILE_PATH/SHiELD/$m"_OLR_winter_ITCZ.nc"
    else
       native_file=$FILE_PATH/$m/$m"_OLR_winter_ITCZ.nc"
    fi
    
    # make grid files if they don't exist
    grid_file=$GRID_PATH/$m"_ITCZ_grid.txt"
    if [ ! -f $grid_file ]; then
       cdo griddes $native_file > $grid_file
    fi

    # interp 0.25 deg file onto native grid
    in_file=$FILE_PATH/Tb_os_thresholds/$m"_cold_point_os_Tb_threshold_ITCZ.nc"
    out_file=$OUT_PATH/$m"_remapped_cold_point_os_Tb_threshold_ITCZ.nc"
    cdo remapnn,$grid_file $in_file $out_file 
done
