#!/bin/bash
#SBATCH --job-name=remapnn_cpT
#SBATCH --partition=interactive
#SBATCH --mem=50GB
#SBATCH --ntasks=1
#SBATCH --time=04:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=remapnn_cpT.eo%j
#SBATCH --error=remapnn_cpT_err.eo%j

set -evx # verbose messages and crash message

# mem should be 100 GB for ICON

module load cdo
export GRIB_DEFINITION_PATH=/sw/rhel6-x64/eccodes/definitions

FILE_PATH=/work/bb1153/b380887/global_tropics
GRID_PATH=$FILE_PATH/itcz_grids
OUT_PATH=/scratch/b/b380887

# remap ERA5 onto MERGIR grid
# grid_file=$GRID_PATH/"MERGIR_ITCZ_grid.txt"
# in_file=$FILE_PATH/local_cold_points/ERA5_cpT_0.25deg_ITCZ.nc
# out_file=$OUT_PATH/ERA5_remapped_cpT_ITCZ.nc
# cdo remapnn,$grid_file $in_file $out_file

# do it for SAM too for the sake of consistency
declare -a ModelArray=(UM ARPNH) #GEOS) #SHIELD GEOS SCREAM ICON SAM)

for m in "${ModelArray[@]}"; do
    # native var path; SHiELD path has the lowercase i
    if [ "$m" = "SHIELD" ]; then
       native_file=$FILE_PATH/SHiELD/$m"_OLR_winter_ITCZ.nc" 
    else
       # native_file=$FILE_PATH/$m/$m"_OLR_winter_ITCZ.nc"
      native_file=$OUT_PATH/$m/$m"_OLR_winter_ITCZ.nc"
    fi
    
    # make grid files if they don't exist
    grid_file=$GRID_PATH/$m"_ITCZ_grid.txt"
    if [ ! -f $grid_file ]; then
       cdo griddes $native_file > $grid_file
    fi

    # interp 0.25 deg file onto native grid
    # in_file=$OUT_PATH/$m"_cpT_0.25deg_ITCZ.nc"
    in_file=$FILE_PATH/local_cold_points/$m"_cpT_0.25deg_ITCZ.nc"
    out_file=$OUT_PATH/$m"_remapped_cpT_ITCZ.nc"
    cdo remapnn,$grid_file $in_file $out_file 
    
    # # interp cold point indices (0.25deg) onto native grid
    # in_file=$FILE_PATH/cold_point_indices/$m"_0.25deg_cold_point_inds.nc"
    # out_file=$OUT_PATH/$m"_cold_point_inds_remapped.nc"
    # cdo remapnn,$grid_file $in_file $out_file 
    
done
