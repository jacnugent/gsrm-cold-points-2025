#!/bin/bash
# header goes here
# recommended: 50GB mem, 6h for the models, 25 GB mem, 2h for obs

set -evx # verbose messages and crash message

module load python3
source activate /home/b/b380887/.conda/envs/d2env

MODEL="ICON"
CHUNKS=500000
# chunk sizes:
# SHIELD: 500,000
# SAM: 256 (just lon)
# SCREAM: 250,000
# GEOS: 250,000
# ICON: 500,000

FILE_PATH="/work/bb1153/b380887/global_tropics/"
# FILE_PATH="/scratch/b/b380887/"
OUT_PATH="/scratch/b/b380887/"
INDEX_PATH=$FILE_PATH"cold_point_indices/"
SCRIPT_PATH="/home/b/b380887/cold-point-overshoot/python_scripts"

# --- MODELS ---
# u flag so it doesn't buffer the print statements
# python -u $SCRIPT_PATH/calc_cold_point_cirrus.py -m $MODEL -f $FILE_PATH -o $OUT_PATH -i $INDEX_PATH -c $CHUNKS
python -u $SCRIPT_PATH/calc_cold_point_cirrus_at_cp_only.py -m $MODEL -f $FILE_PATH -o $OUT_PATH -i $INDEX_PATH -c $CHUNKS


# # --- OBSERVATIONS ---
YEARS="2007 2008 2009 2010"
REGION="ITCZ"
MONTHS="Feb"
OBS_PATH="/work/bb1153/b380887/global_tropics/obs/DARDAR/"
# # python $SCRIPT_PATH/calc_cold_point_cirrus_obs.py -y $YEARS -m $MONTHS -r $REGION -f $FILE_PATH -o $OUT_PATH 
# # python $SCRIPT_PATH/calc_cold_point_cirrus_obs.py -y $YEARS -m $MONTHS -r $REGION -f $FILE_PATH -o $OUT_PATH --no_conv
python -u $SCRIPT_PATH/calc_cold_point_cirrus_obs_at_cp_only.py -y $YEARS -m $MONTHS -r $REGION -f $OBS_PATH -o $OUT_PATH 
