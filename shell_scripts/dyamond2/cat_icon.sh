#!/bin/bash
# header goes here
# recommended: 100GB mem, 1h 


set -evx # verbose messages and crash message

module load cdo

FILE_PATH=/scratch/b/b380887/ICON

cdo cat $FILE_PATH/*wa*.nc $FILE_PATH/ICON_w_12-20km_winter_ITCZ_days10-40.nc
cdo cat $FILE_PATH/clivi*.nc $FILE_PATH/ICON_IWP_winter_ITCZ.nc
cdo cat $FILE_PATH/qsvi*.nc $FILE_PATH/ICON_SWP_winter_ITCZ.nc
cdo cat $FILE_PATH/qgvi*.nc $FILE_PATH/ICON_GWP_winter_ITCZ.nc

cdo cat $FILE_PATH/*pa*.nc $FILE_PATH/ICON_pa_12-20km_winter_ITCZ_days10-40.nc
cdo cat $FILE_PATH/*hus*.nc $FILE_PATH/ICON_qv_12-20km_winter_ITCZ.nc
cdo cat $FILE_PATH/*cli*.nc $FILE_PATH/ICON_qi_12-20km_winter_ITCZ.nc

cdo cat $FILE_PATH/*ta*.nc $FILE_PATH/ICON_temp_12-20km_winter_ITCZ.nc
cdo cat $FILE_PATH/rl*.nc $FILE_PATH/ICON_OLR_acc_winter_ITCZ.nc
# cdo cat $FILE_PATH/rl*.nc $FILE_PATH/ICON_OLR_acc_winter_GT.nc
cdo cat $FILE_PATH/pr*.nc $FILE_PATH/ICON_pr_acc_winter_ITCZ.nc
cdo cat $FILE_PATH/14*.nc $FILE_PATH/ICON_w_14_17_20km_winter_ITCZ.nc
