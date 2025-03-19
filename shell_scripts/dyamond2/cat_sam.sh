#!/bin/bash
# header goes here
# recommended: 25GB mem, 1h 


set -evx # verbose messages and crash message

module load cdo

FILE_PATH=/scratch/b/b380887/SAM

cdo cat $FILE_PATH/"12-20_wa*.nc" $FILE_PATH/SAM_w_12-20km_winter_ITCZ.nc

cdo cat $FILE_PATH/*cli*.nc $FILE_PATH/SAM_qi_12-20km_winter_ITCZ.nc
cdo cat $FILE_PATH/*hus*.nc $FILE_PATH/SAM_qv_12-20km_winter_ITCZ.nc

cdo cat $FILE_PATH/rltacc*.nc $FILE_PATH/SAM_OLR_acc_winter_ITCZ.nc
# cdo cat $FILE_PATH/rltacc*.nc $FILE_PATH/SAM_OLR_acc_winter_GT.nc
cdo cat $FILE_PATH/pr*.nc $FILE_PATH/SAM_pr_acc_winter_ITCZ.nc

cdo cat $FILE_PATH/clivi*.nc $FILE_PATH/SAM_IWP_winter_ITCZ.nc
cdo cat $FILE_PATH/qsvi*.nc $FILE_PATH/SAM_SWP_winter_ITCZ.nc
cdo cat $FILE_PATH/qgvi*.nc $FILE_PATH/SAM_GWP_winter_ITCZ.nc
cdo cat $FILE_PATH/"12-20_ta*.nc" $FILE_PATH/SAM_temp_12-20km_winter_ITCZ.nc
