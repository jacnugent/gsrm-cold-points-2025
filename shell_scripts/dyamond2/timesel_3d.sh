#!/bin/bash
#SBATCH --job-name=i_timesel_3d
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=20GB
#SBATCH --time=02:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=i_timesel_3d.eo%j
#SBATCH --error=i_timesel_ed_err.eo%j

set -evx # verbose messages and crash message
module load cdo

# FILE_PATH=/scratch/b/b380887
FILE_PATH=/work/bb1153/b380887/global_tropics

# drop first 10 days so files are smaller
DATE0="2020-01-30T00:00:00"
DATE1="2020-03-01T00:00:00"

in_file_qi=$FILE_PATH/ICON/ICON_qi_12-20km_winter_ITCZ.nc
in_file_qv=$FILE_PATH/ICON/ICON_qv_12-20km_winter_ITCZ.nc
in_file_temp=$FILE_PATH/ICON/ICON_temp_12-20km_winter_ITCZ.nc

out_file_qi=$FILE_PATH/ICON/ICON_qi_12-20km_winter_ITCZ_day_10-40.nc
out_file_qv=$FILE_PATH/ICON/ICON_qv_12-20km_winter_ITCZ_day_10-40.nc
out_file_temp=$FILE_PATH/ICON/ICON_temp_12-20km_winter_ITCZ_day_10-40.nc

cdo select,startdate=$DATE0,enddate=$DATE1 $in_file_qi $out_file_qi
cdo select,startdate=$DATE0,enddate=$DATE1 $in_file_qv $out_file_qv
cdo select,startdate=$DATE0,enddate=$DATE1 $in_file_temp $out_file_temp

# in_file_qi=$FILE_PATH/SCREAM/SCREAM_qi_12-20km_winter_ITCZ.nc
# in_file_qv=$FILE_PATH/SCREAM/SCREAM_qv_12-20km_winter_ITCZ.nc
# in_file_temp=$FILE_PATH/SCREAM/SCREAM_temp_12-20km_winter_ITCZ.nc

# out_file_qi=$FILE_PATH/SCREAM/SCREAM_qi_12-20km_winter_ITCZ_day_10-40.nc
# out_file_qv=$FILE_PATH/SCREAM/SCREAM_qv_12-20km_winter_ITCZ_day_10-40.nc
# out_file_temp=$FILE_PATH/SCREAM/SCREAM_temp_12-20km_winter_ITCZ_day_10-40.nc

# cdo select,startdate=$DATE0,enddate=$DATE1 $in_file_qi $out_file_qi
# cdo select,startdate=$DATE0,enddate=$DATE1 $in_file_qv $out_file_qv
# cdo select,startdate=$DATE0,enddate=$DATE1 $in_file_temp $out_file_temp

