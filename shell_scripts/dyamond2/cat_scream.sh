#!/bin/bash
# header goes here
# recommended: 20GB mem, 1h 


set -evx # verbose messages and crash message

module load cdo

FILE_PATH=/scratch/b/b380887/SCREAM
                                                                                            
cdo cat $FILE_PATH/*ps*.nc $FILE_PATH/SCREAM_ps_winter_ITCZ.nc

cdo cat $FILE_PATH/*wap*.nc $FILE_PATH/SCREAM_wap_12-20km_winter_ITCZ_days10-40.nc
cdo cat $FILE_PATH/*cli*.nc $FILE_PATH/SCREAM_qi_12-20km_winter_ITCZ.nc
cdo cat $FILE_PATH/*hus*.nc $FILE_PATH/SCREAM_qv_12-20km_winter_ITCZ.nc
cdo cat $FILE_PATH/*ta*.nc $FILE_PATH/SCREAM_temp_12-20km_winter_ITCZ.nc

cdo cat $FILE_PATH/rlt*.nc $FILE_PATH/SCREAM_OLR_winter_ITCZ.nc
# cdo cat $FILE_PATH/rlt*.nc $FILE_PATH/SCREAM_OLR_winter_GT.nc
cdo cat $FILE_PATH/pr*.nc $FILE_PATH/SCREAM_precip_winter_ITCZ.nc
cdo cat $FILE_PATH/clivi*.nc $FILE_PATH/SCREAM_FWP_winter_ITCZ.nc
