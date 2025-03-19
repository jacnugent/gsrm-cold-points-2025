#!/bin/bash
# header goes here
# recommended: 50GB mem, 9h 

set -evx # verbose messages and crash message

module load python3
source activate /home/b/b380887/.conda/envs/era5env


SCRIPT_PATH="/home/b/b380887/cold-point-overshoot/python_scripts"
OUT_PATH="/scratch/b/b380887/ERA5_ml"
WORK_PATH="/work/bb1153/b380887/global_tropics"


declare -a YearArr=(2020) #2008 2009 2010)
month="Feb"
region="ITCZ"

# process renalysis data for all years
for year in "${YearArr[@]}"; do
    echo $month $year
    
    temp_gt=$OUT_PATH/ERA5_T_0.25deg_ml_12-20km_$month$year"_ITCZ.nc"
    tq_gt=$OUT_PATH/tq_$month$year"_ITCZ.grib"
    zlnsp_gt=$OUT_PATH/zlnsp_$month$year"_ITCZ.grib"

    echo "Computing geopotential..."
    zout=$OUT_PATH/z_out_$month$year"_"$region".grib"
    if [ ! -f $zout ] ; then
        python3 $SCRIPT_PATH/compute_geopotential_on_ml.py -o $zout $tq_gt $zlnsp_gt
    fi
        
    echo "Converting to netcdf..."
    zout_nc=$OUT_PATH/ERA5_zg_0.25deg_ml_$month$year"_"$region".nc"
    if [ ! -f $zout_nc ] ; then
        grib_to_netcdf -o $zout_nc $zout
    fi

    echo "Converting tq file to netcdf..."
    tq_out_nc=$OUT_PATH/ERA5_tq_0.25deg_ml_$month$year"_"$region".nc"
    if [ ! -f $tq_out_nc ] ; then
        grib_to_netcdf -o $tq_out_nc $tq_out
    fi
    
    # delete the .grib files if it worked
    if [ -f $zout_nc ] ; then
        rm $zout
    fi
    
    echo "..."$region" done"
    
done
