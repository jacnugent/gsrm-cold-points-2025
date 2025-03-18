#!/bin/bash
#SBATCH --job-name=conv_bin_d2
#SBATCH --partition=interactive
#SBATCH --ntasks=1
#SBATCH --mem=50GB
#SBATCH --time=04:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=jnug@uw.edu
#SBATCH --account=bb1153
#SBATCH --output=conv_bin_d2.eo%j
#SBATCH --error=conv_bin_d2_err.eo%j

set -evx # verbose messages and crash message

module load python3
source activate /home/b/b380887/.conda/envs/d2env

declare -a ModelArr=(SHIELD SCREAM GEOS) # SAM ICON 
declare -a RegionArr=(AMZ SPC) # SCA TIM)

SCRIPT_PATH="/home/b/b380887/cold-point-overshoot/python_scripts"
FILE_PATH="/work/bb1153/b380887/10x10/"
PICKLE_PATH="/home/b/b380887/cold-point-overshoot/pickle_files/tb_corrected_binned/new_thresh/"
# PICKLE_PATH="/home/b/b380887/cold-point-overshoot/pickle_files/racp_cirrus_binned/"

for model in "${ModelArr[@]}"; do
    echo $model
    
    for region in "${RegionArr[@]}"; do
        python $SCRIPT_PATH/bin_d2.py -r $region -m $model -p $PICKLE_PATH -f $FILE_PATH -c "2.5e-4"
        echo "...done with"$region"."
    done
    
    echo "...done with "$model"."
done
