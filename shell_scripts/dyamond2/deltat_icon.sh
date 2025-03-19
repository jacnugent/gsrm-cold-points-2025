#!/bin/bash
# header goes here
# recommended: 25GB mem, 3h 

set -evx # verbose messages and crash message
module load nco
module load cdo

FILE_PATH=/scratch/b/b380887

olr_in=$FILE_PATH/ICON_OLR_acc_winter_ITCZ.nc
olr_out=$FILE_PATH/ICON_OLR_winter_ITCZ.nc

# NOTE: this doesn't get rid of spikes... mask above 350 W/m2 when processing
olr (J/m2 --> W/m2) and flip sign
cdo -divc,-900 -deltat $olr_in $olr_out
ncatted -O -a standard_name,rltacc,o,c,"toa_net_downward_longwave_flux" -a long_name,rltacc,o,c,"Net long wave radiation flux - model top" -a units,rltacc,o,c,"W/m2" $olr_out
ncrename -O -v rltacc,rlt $olr_out
