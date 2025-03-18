#!/bin/bash
#SBATCH --job-name=tb_3h
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=50GB
#SBATCH --time=03:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=tb_3h.eo%j
#SBATCH --error=tb_3h_err.eo%j

set -evx # verbose messages and crash message


in_file="/work/bb1153/b380887/global_tropics/obs/MERGIR/MERGIR_Feb2020_4km_ITCZ.nc4"
out_file="/scratch/b/b380887/MERGIR_tb_3hrly_ITCZ.nc"

HOURS="0,3,6,9,12,15,18,21"

# cdo selhour,$HOURS $in_file $out_file

# this is how to actually do it (otherwise you get all minutes at each 
# selected hour)
cdo -seltimestep,1/-1/2 -selhour,$HOURS $in_file $out_file
