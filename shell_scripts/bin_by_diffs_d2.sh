#!/bin/bash
# header goes here
# recommended: 50GB mem, 4 hours

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
