#!/bin/bash
#SBATCH --job-name=deltaticon
#SBATCH --partition=interactive
#SBATCH --mem=25GB
#SBATCH --ntasks=1
#SBATCH --time=03:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=dticon.eo%j
#SBATCH --error=dticon_err.eo%j

set -evx # verbose messages and crash message
module load nco
module load cdo

FILE_PATH=/scratch/b/b380887

# olr_in=$FILE_PATH/ICON_OLR_acc_winter_ITCZ.nc
# olr_out=$FILE_PATH/ICON_OLR_winter_ITCZ.nc
# olr_in=$FILE_PATH/ICON_OLR_acc_winter_GT.nc
# olr_out=$FILE_PATH/ICON_OLR_winter_GT.nc



# NOTE: this doesn't get rid of spikes... mask above 350 W/m2 when processing
# olr (J/m2 --> W/m2) and flip sign
# cdo -divc,-900 -deltat $olr_in $olr_out
# ncatted -O -a standard_name,rltacc,o,c,"toa_net_downward_longwave_flux" -a long_name,rltacc,o,c,"Net long wave radiation flux - model top" -a units,rltacc,o,c,"W/m2" $olr_out
# ncrename -O -v rltacc,rlt $olr_out

declare -a RegionArr=(AMZ SPC)

for r in "${RegionArr[@]}"; do

    # pr (mm --> mm/hr)
    pr_in=$FILE_PATH/ICON_pracc_winter_$r".nc"
    pr_out=$FILE_PATH/ICON_pr_winter_$r".nc"
    cdo -mulc,4 -deltat $pr_in $pr_out
    ncatted -O -a standard_name,pracc,o,c,"precipitation_flux" -a long_name,pracc,o,c,"Total Precipitation" -a units,pracc,o,c,"mm/hr" $pr_out
    ncrename -O -v pracc,pr $pr_out

    # temp - do SAM in the same script (easier)
    pr_in_sam=$FILE_PATH/SAM_pracc_winter_$r".nc"
    pr_out_sam=$FILE_PATH/SAM_pr_winter_$r".nc"
    cdo -mulc,4 -deltat $pr_in_sam $pr_out_sam
    ncatted -O -a standard_name,pracc,o,c,"precipitation_flux" -a long_name,pracc,o,c,"Surface Precip." -a units,pracc,o,c,"mm/hr" $pr_out_sam
    ncrename -O -v pracc,pr $pr_out_sam
    
done