#!/bin/bash
#SBATCH --job-name=i_remapcon
#SBATCH --partition=interactive
#SBATCH --mem=100GB
#SBATCH --ntasks=1
#SBATCH --time=05:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=i_rmcon.eo%j
#SBATCH --error=i_rmcon_err.eo%j

set -evx # verbose messages and crash message

module load cdo
export GRIB_DEFINITION_PATH=/sw/rhel6-x64/eccodes/definitions

FILE_PATH=/work/bb1153/b380887/global_tropics/ICON
GRIDS=/home/b/b380887/cold-point-overshoot/slurm_scripts/process_files/grid_files
GRID_FILE=/work/bk1040/DYAMOND/data/winter_data/DYAMOND_WINTER/MPIM-DWD-DKRZ/ICON-NWP-2km/DW-ATM/atmos/fx/gn/grid.nc

# OLR: hourly, 1x1
#OLR_IN=$FILE_PATH/ICON_OLR_winter_ITCZ.nc
#OLR_OUT=$FILE_PATH/ICON_hourly_1x1_OLR_winter_ITCZ.nc
#cdo -timselmean,4,0 -remapcon,$GRIDS/itcz_1x1_grid.txt -setgrid,$GRID_FILE $OLR_IN $OLR_OUT

# precip: 30 min, 0.1deg
PR_IN=$FILE_PATH/ICON_pr_winter_ITCZ.nc
PR_OUT=$FILE_PATH/ICON_pr_30min_0.1deg_winter_ITCZ.nc
cdo -timselmean,2,0 -remapcon,$GRIDS/itcz_0.1deg_grid.txt -setgrid,$GRID_FILE $PR_IN $PR_OUT

# Temperature: 0.25deg
TEMP_IN=$FILE_PATH/ICON_temp_12-20km_winter_ITCZ.nc
TEMP_OUT=$FILE_PATH/ICON_temp_0.25deg_12-20km_winter_ITCZ.nc
cdo -remapcon,$GRIDS/itcz_0.25deg_grid.txt -setgrid,$GRID_FILE $TEMP_IN $TEMP_OUT

