#!/bin/bash
#SBATCH --job-name=deltatsam
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=25GB
#SBATCH --time=03:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=dtsam.eo%j
#SBATCH --error=dtsam_err.eo%j

set -evx # verbose messages and crash message
module load nco
module load cdo

FILE_PATH=/scratch/b/b380887/SAM

# olr_in=$FILE_PATH/SAM_OLR_acc_winter_ITCZ.nc
# olr_out=$FILE_PATH/SAM_OLR_winter_ITCZ.nc
# olr_in=$FILE_PATH/SAM_OLR_acc_winter_GT.nc
# olr_out=$FILE_PATH/SAM_OLR_winter_GT.nc

pr_in=$FILE_PATH/SAM_pr_acc_winter_ITCZ.nc
pr_out=$FILE_PATH/SAM_pr_winter_ITCZ.nc

# # olr (J/m2 --> W/m2)
# cdo -divc,900 -deltat $olr_in $olr_out
# ncatted -O -a standard_name,rltacc,o,c,"toa_net_downward_longwave_flux" -a long_name,rltacc,o,c,"Net LW at TOA" -a units,rltacc,o,c,"W/m2" $olr_out
# ncrename -O -v rltacc,rlt $olr_out

# pr (mm --> mm/hr)
cdo -mulc,4 -deltat $pr_in $pr_out
ncatted -O -a standard_name,pracc,o,c,"precipitation_flux" -a long_name,pracc,o,c,"Surface Precip." -a units,pracc,o,c,"mm/hr" $pr_out
ncrename -O -v pracc,pr $pr_out
