#!/bin/bash
# header goes here
# recommended: 25GB mem, 4h 

set -evx # verbose messages and crash message

module load cdo

FILE_PATH=/scratch/b/b380887/SHiELD

cdo cat $FILE_PATH/*ta*.nc $FILE_PATH/SHIELD_temp_winter_ITCZ.nc
cdo cat $FILE_PATH/*zg*.nc $FILE_PATH/SHIELD_zg_12-20km_winter_ITCZ.nc
cdo cat $FILE_PATH/*grpl*.nc $FILE_PATH/SHIELD_qg_12-20km_winter_ITCZ.nc
cdo cat $FILE_PATH/snow/*snowmxrat*.nc $FILE_PATH/SHIELD_qs_12-20km_winter_ITCZ.nc


# NOTE - have to do it without the weird time step (2/25-2/26)
cdo cat $FILE_PATH/*cli*.nc $FILE_PATH/SHIELD_qi_12-20km_winter_ITCZ.nc

cdo cat $FILE_PATH/*grpl*.nc $FILE_PATH/SHIELD_qg_12-20km_winter_ITCZ.nc
cdo cat $FILE_PATH/*hus*.nc $FILE_PATH/SHIELD_qv_12-20km_winter_ITCZ.nc

cdo cat $FILE_PATH/*wa*.nc $FILE_PATH/SHIELD_w_12-20km_winter_ITCZ.nc
cdo cat $FILE_PATH/*zg*.nc $FILE_PATH/SHIELD_zg_12-20km_winter_ITCZ.nc

cdo cat $FILE_PATH/*rlut*.nc $FILE_PATH/SHIELD_OLR_winter_ITCZ.nc
# cdo cat $FILE_PATH/*rlut*.nc $FILE_PATH/SHIELD_OLR_winter_GT.nc
cdo cat $FILE_PATH/*pr*.nc $FILE_PATH/SHIELD_pr_winter_ITCZ.nc

# cdo cat $FILE_PATH/"regridded*pr*.nc" $FILE_PATH/SHiELD_0.1deg_pr_winter_ITCZ.nc
