#!/bin/bash
# header goes here
# recommended: 50GB mem, 6h 

set -evx # verbose messages and crash message

module load cdo
export GRIB_DEFINITION_PATH=/sw/rhel6-x64/eccodes/definitions

# FILE_PATH=/work/bb1153/b380887/10x10
FILE_PATH=/work/bb1153/b380887/global_tropics
OUT_PATH=/scratch/b/b380887

# mem should be 100 GB if using ICON

# interp 0.25 deg cold point file onto the native grid for all models
declare -a ModelArray=(UM ARPNH) #GEOS) #ICON SAM) # SHIELD GEOS SCREAM 
for model in "${ModelArray[@]}"; do
    grid_file=$FILE_PATH/itcz_grids/$model"_ITCZ_grid.txt"
    in_file=$FILE_PATH/local_cold_points/$model"_cpT_0.25deg_ITCZ.nc"
    out_file=$OUT_PATH/$model"_cpT_remapped_ITCZ.nc"
    cdo remapnn,$grid_file $in_file $out_file
done


declare -a LocArray=(TIM SCA) #AMZ SPC) #TWP SCA SAV TIM)

# --- GEOS ---
for r in "${LocArray[@]}"; do

    # make grid files if they don't exist
    grid_file=$FILE_PATH/10x10_grids/GEOS_$r"_grid.txt"
    if [ ! -f $grid_file ]; then
        cdo griddes $FILE_PATH/$r/GEOS_temp_12-20km_winter_$r".nc" > $grid_file
    fi

    # interp 0.25 deg file onto native grid
    in_file=$FILE_PATH/$r/GEOS_temp_0.25deg_12-20km_winter_$r".nc"
    out_file=$OUT_PATH/GEOS_temp_025_remapped_$r".nc"
    cdo remapnn,$grid_file $in_file $out_file 

done


# --- ICON ---
for r in "${LocArray[@]}"; do

    # make grid files if they don't exist
    grid_file=$FILE_PATH/10x10_grids/ICON_$r"_grid.txt"
    if [ ! -f $grid_file ]; then
        cdo griddes $FILE_PATH/$r/ICON_temp_12-20km_winter_$r".nc" > $grid_file
    fi

    # interp 0.25 deg file onto native grid
    in_file=$FILE_PATH/$r/ICON_temp_0.25deg_12-20km_winter_$r".nc"
    out_file=$OUT_PATH/ICON_temp_025_remapped_$r".nc"
    cdo remapnn,$grid_file $in_file $out_file 

done


--- SCREAM ---
for r in "${LocArray[@]}"; do

    # make grid files if they don't exist
    grid_file=$FILE_PATH/10x10_grids/SCREAM_$r"_grid.txt"
    if [ ! -f $grid_file ]; then
        cdo griddes $FILE_PATH/$r/SCREAM_temp_12-20km_winter_$r".nc" > $grid_file
    fi

    # interp 0.25 deg file onto native grid
    in_file=$FILE_PATH/$r/SCREAM_temp_0.25deg_12-20km_winter_$r.nc
    out_file=$OUT_PATH/SCREAM_temp_025_remapped_$r.nc
    cdo remapnn,$grid_file $in_file $out_file 

done


# --- SHiELD ---
for r in "${LocArray[@]}"; do

    # make grid files if they don't exist
    grid_file=$FILE_PATH/10x10_grids/SHIELD_$r"_grid.txt"
    if [ ! -f $grid_file ]; then
        echo "Grid not found; making it"
        cdo griddes $FILE_PATH/$r/SHIELD_temp_12-20km_winter_$r.nc > $grid_file
    fi

    # interp 0.25 deg file onto native grid
    # in_file=$FILE_PATH/$r/SHIELD_temp_0.25deg_12-20km_winter_$r.nc
    in_file=$OUT_PATH/SHIELD_temp_0.25deg_12-20km_winter_$r.nc
    out_file=$OUT_PATH/SHIELD_temp_025_remapped_$r.nc
    cdo remapnn,$grid_file $in_file $out_file 

done
