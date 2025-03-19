#!/bin/bash
# header goes here
# recommended: 25GB mem, 3h 


set -evx # verbose messages and crash message
module load nco
module load cdo

FILE_PATH=/scratch/b/b380887/SAM

olr_in=$FILE_PATH/SAM_OLR_acc_winter_ITCZ.nc
olr_out=$FILE_PATH/SAM_OLR_winter_ITCZ.nc

# olr (J/m2 --> W/m2)
cdo -divc,900 -deltat $olr_in $olr_out
ncatted -O -a standard_name,rltacc,o,c,"toa_net_downward_longwave_flux" -a long_name,rltacc,o,c,"Net LW at TOA" -a units,rltacc,o,c,"W/m2" $olr_out
ncrename -O -v rltacc,rlt $olr_out
