#!/bin/bash
# header goes here
# recommended: 50GB mem, 2h 

# set -evx # verbose messages and crash message

module load python3
source activate /home/b/b380887/.conda/envs/d2env

SEASON="DJF"

SCRIPT_PATH="/home/b/b380887/cold-point-overshoot/python_scripts"
FILE_PATH="/work/bb1153/b380887/10x10/"
PICKLE_PATH="/home/b/b380887/cold-point-overshoot/pickle_files/d2_tb-cpt_hists/obs/"
OUT_PATH="/scratch/b/b380887/"

declare -a YearArr=(2007 2008 2009 2010)
declare -a RegionArr=(SPC) # AMZ SCA TIM)


for year in "${YearArr[@]}"; do
    echo $year
    for region in "${RegionArr[@]}"; do
        echo "Getting regridded cold point temperature file..."
        python $SCRIPT_PATH/cold_point_reindex.py -y $year -r $region -m "DJF" -f $FILE_PATH/$region -o $FILE_PATH/$region
        echo "Get the histogram dictionary..."
        python $SCRIPT_PATH/biv_hist.py -y $year -r $region -m "DJF" -f $FILE_PATH/$region -p $PICKLE_PATH --no_spc_split
        echo "...done with "$region
    done
done
    