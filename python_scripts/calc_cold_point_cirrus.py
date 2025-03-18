"""
calc_cold_point_cirrus.py

Calculate the number of time steps that each grid point has an ice mixing ratio
above the radiatively-active threshold for a 1 km layer near the cold point.

---------------

usage: calc_cold_point_cirrus.py [-h] -m MODEL -f FILE_PATH -o OUT_PATH -i INDEX_PATH -c XCHUNKS

-------------

"""
import argparse 
import xarray as xr
import numpy as np


START_DATE = "2020-01-30"
END_DATE = "2020-02-28"

# radiatively active threshold
QI_CRIT = 2e-6 # kg/kg

# map model to dimension names (to manually chunk over)
XDIM_DICT = {
    "SHIELD": "Xdim",
    "ICON": "cell",
    "SCREAM": "ncol",
    "GEOS": "Xdim",
    "SAM": "lon"
}


def parse_args():
    """ Parse command-line arguments
    """
    parser = argparse.ArgumentParser()
    
    # required
    parser.add_argument("-m", "--model", help="Model name", required=True)
    parser.add_argument("-f", "--file_path", help="Input path for qi files", required=True)
    parser.add_argument("-o", "--out_path", help="Output path for files", required=True)
    parser.add_argument("-i", "--index_path", help="Path for (remapped) cold point index files", required=True)
    parser.add_argument("-c", "--xchunks", type=int, help="Size of grid points to use for each manual chunking (integer)", required=True)
    
    # optional
    parser.add_argument("-n", "--no_conv", action='store_true', help="Exclude convection from the identification of cirrus (i.e., impose an upper limit on cloud ice)", required=False)


    return parser.parse_args()


def get_qi(model, file_path, start_date=START_DATE, 
           end_date=END_DATE):
    """ Read in the ITCZ ice file and change so it's ordered bottom-up
    """
    if model == "SHIELD":
        qi_td = xr.open_dataset(file_path + "SHiELD/SHIELD_qi_12-20km_winter_ITCZ.nc")["cli"]
        qi = qi_td.reindex(pfull_ref=qi_td.pfull_ref[::-1])
    else:
        qi_td = xr.open_dataset(file_path + "{m}/{m}_qi_12-20km_winter_ITCZ.nc".format(m=model))["cli"]
        if model == "SAM":
            print("got here")
            qi = qi_td
            print("did the dividing")
        elif model == "GEOS" or model == "SCREAM":
            qi = qi_td.reindex(lev=qi_td.lev[::-1])
        elif model == "ICON":
            qi = qi_td.reindex(height=qi_td.height[::-1])
    
    return qi.sel(time=slice(start_date, end_date))
        
    
def get_1km_layer_counts(model, qi, cp_inds, xchunks, qi_crit=QI_CRIT, xdim_dict=XDIM_DICT):
    """ 
    Count the number of times a grid point has a 1km-average
    ice layer near the cold point that exceeds the radiatively
    active threshold.
    
    Use this one for SAM, ICON, or SHIELD (i.e., dz~500m models).
    """
    xdim = xdim_dict[model]
    
    nx = int(np.ceil(len(qi[xdim])/xchunks))
    qi_below_list = [[]]*nx # -1000m to 0 m
    qi_at_list = [[]]*nx # -500m to +500 m
    qi_above_list = [[]]*nx # 0 m to +500 m 

    for i in range(nx):
        start_ind = int(i*xchunks)
        end_ind = int((i+1)*xchunks)
        if end_ind > len(qi[xdim]):
            end_ind = None

        # do the chunking
        # and get ice at levels relative to the cold point for that chunk
        if model == "SHIELD":
            inds_mini = cp_inds.isel(Xdim=slice(start_ind, end_ind)).astype(int)
            qi_mini = qi.isel(Xdim=slice(start_ind, end_ind))
            qi_cp = qi_mini.isel(pfull_ref=inds_mini).values
            qi_a500 = qi_mini.isel(pfull_ref=inds_mini+1).values
            qi_a1000 = qi_mini.isel(pfull_ref=inds_mini+2).values
            qi_b500 = qi_mini.isel(pfull_ref=inds_mini-1).values
            qi_b1000 = qi_mini.isel(pfull_ref=inds_mini-2).values
        elif model == "ICON":
            inds_mini = cp_inds.isel(cell=slice(start_ind, end_ind)).astype(int)
            qi_mini = qi.isel(cell=slice(start_ind, end_ind))
            qi_cp = qi_mini.isel(height=inds_mini).values
            qi_a500 = qi_mini.isel(height=inds_mini+1).values
            qi_a1000 = qi_mini.isel(height=inds_mini+2).values
            qi_b500 = qi_mini.isel(height=inds_mini-1).values
            qi_b1000 = qi_mini.isel(height=inds_mini-2).values
        elif model == "SAM": 
            inds_mini = cp_inds.isel(lon=slice(start_ind, end_ind)).astype(int)
            qi_mini = qi.isel(lon=slice(start_ind, end_ind))
            inds_mini = inds_mini.assign_coords(lat=qi_mini.lat)
            # for SAM - some decimal lat values got truncated in the reindexing;
            # set them equal again
            qi_cp = qi_mini.isel(z=inds_mini).values
            qi_a500 = qi_mini.isel(z=inds_mini+1).values
            qi_a1000 = qi_mini.isel(z=inds_mini+2).values
            qi_b500 = qi_mini.isel(z=inds_mini-1).values
            qi_b1000 = qi_mini.isel(z=inds_mini-2).values

        # find the mean qi mixing ratio in the 1000m layer (average of top/middle/bottom values)
        qi_below = np.mean(np.array([qi_b1000, qi_b500, qi_cp]), axis=0)
        qi_at = np.mean(np.array([qi_b500, qi_cp, qi_a500]), axis=0)
        qi_above = np.mean(np.array([qi_cp, qi_a500, qi_a1000]), axis=0)

        # count the number of times the mean of the 1000m layer exceeds the threshold
        if model == "SAM":
            qi_below_ra = np.sum(np.where(qi_below/1000. > qi_crit, 1, 0), axis=0)
            qi_at_ra = np.sum(np.where(qi_at/1000. > qi_crit, 1, 0), axis=0)
            qi_above_ra = np.sum(np.where(qi_above/1000. > qi_crit, 1, 0), axis=0)
        else:
            qi_below_ra = np.sum(np.where(qi_below > qi_crit, 1, 0), axis=0)
            qi_at_ra = np.sum(np.where(qi_at > qi_crit, 1, 0), axis=0)
            qi_above_ra = np.sum(np.where(qi_above > qi_crit, 1, 0), axis=0)

        # add to a list - will later concatenate these and give it the xdimension
        qi_below_list[i] = qi_below_ra
        qi_at_list[i] = qi_at_ra
        qi_above_list[i] = qi_above_ra

        print(i+1, "done out of", nx)
    
    return [qi_below_list, qi_at_list, qi_above_list]


def get_1km_layer_counts_fine_z(model, qi, cp_inds, xchunks, qi_crit=QI_CRIT, xdim_dict=XDIM_DICT):
    """ 
    Count the number of times a grid point has a 1km-average
    ice layer near the cold point that exceeds the radiatively
    active threshold.
    
    Use this one for GEOS or SCREAM (i.e., dz~250m models).
    """
    xdim = xdim_dict[model]
    
    nx = int(np.ceil(len(qi[xdim])/xchunks))
    qi_below_list = [[]]*nx # -1000m to 0 m
    qi_at_list = [[]]*nx # -500m to +500 m
    qi_above_list = [[]]*nx # 0 m to +500 m 

    for i in range(nx):
        start_ind = int(i*xchunks)
        end_ind = int((i+1)*xchunks)
        if end_ind > len(qi[xdim]):
            end_ind = None

        # do the chunking
        # and get ice at levels relative to the cold point for that chunk
        if model == "GEOS":
            inds_mini = cp_inds.isel(Xdim=slice(start_ind, end_ind)).astype(int)
            qi_mini = qi.isel(Xdim=slice(start_ind, end_ind))
        elif model == "SCREAM":
            inds_mini = cp_inds.isel(ncol=slice(start_ind, end_ind)).astype(int)
            qi_mini = qi.isel(ncol=slice(start_ind, end_ind))
        qi_cp = qi_mini.isel(lev=inds_mini).values
        qi_a500 = qi_mini.isel(lev=inds_mini+2).values
        qi_a1000 = qi_mini.isel(lev=inds_mini+4).values
        qi_b500 = qi_mini.isel(lev=inds_mini-2).values
        qi_b1000 = qi_mini.isel(lev=inds_mini-4).values
        qi_b250 = qi_mini.isel(lev=inds_mini-1).values
        qi_b750 = qi_mini.isel(lev=inds_mini-3).values
        qi_a250 = qi_mini.isel(lev=inds_mini+1).values
        qi_a750 = qi_mini.isel(lev=inds_mini+3).values

        # find the mean qi mixing ratio in the 1000m layer (average of the layer values)
        qi_below = np.mean(np.array([qi_b1000, qi_b750, qi_b500, qi_b250, qi_cp]), axis=0)
        qi_at = np.mean(np.array([qi_b500, qi_b250, qi_cp, qi_a250, qi_a500]), axis=0)
        qi_above = np.mean(np.array([qi_cp, qi_a250, qi_a500, qi_a750, qi_a1000]), axis=0)

        # count the number of times the mean of the 1000m layer exceeds the threshold
        qi_below_ra = np.sum(np.where(qi_below > qi_crit, 1, 0), axis=0)
        qi_at_ra = np.sum(np.where(qi_at > qi_crit, 1, 0), axis=0)
        qi_above_ra = np.sum(np.where(qi_above > qi_crit, 1, 0), axis=0)

        # add to a list - will later concatenate these and give it the xdimension
        qi_below_list[i] = qi_below_ra
        qi_at_list[i] = qi_at_ra
        qi_above_list[i] = qi_above_ra

        print(i+1, "done out of", nx)
    
    return [qi_below_list, qi_at_list, qi_above_list]


def cat_array_into_da(array_list, model, qi, xdim_dict=XDIM_DICT):
    """ Concatenate a list of numpy arrays into a data array
    """
    xdim = xdim_dict[model]
    if len(array_list[0].shape) > 1:
        cat_arr = np.concatenate(array_list, axis=1)
    else:
        cat_arr = np.concatenate(array_list)
        
    if model == "SAM":
        da = xr.DataArray(cat_arr, dims=["lat", "lon"], 
                          coords={"lat": qi["lat"], "lon": qi["lon"]})
    else:
        da = xr.DataArray(cat_arr, dims=[xdim], coords={xdim: qi[xdim]})
    
    return da


def main():
    """
    Get the cold point-relative cirrus counts for three layers (above, below, and
    "at" cold point) and save as netcdfs.
    """
    args = parse_args()
    print(args)
    
    model = args.model
    file_path = args.file_path
    out_path = args.out_path
    index_path = args.index_path
    xchunks = args.xchunks
    
    # get ice + indices and match times
    qi = get_qi(model, file_path)
    print("got qi")
    cp_inds = xr.open_dataset(index_path + "{m}_cold_point_inds_remapped.nc".format(m=model))["cp_inds_cut"].sel(time=qi.time)
    if model == "SCREAM":
        cp_inds = cp_inds.rename({"grid_size": "ncol"}) # match dimension names
    print("got the cold point inds")
    
    if model == "SCREAM" or model == "GEOS":
        qi_below_list, qi_at_list, qi_above_list = get_1km_layer_counts_fine_z(model, qi, cp_inds, xchunks)
    else:
        qi_below_list, qi_at_list, qi_above_list = get_1km_layer_counts(model, qi, cp_inds, xchunks)
    print("got the count lists")
        
    # make into data arrays
    da_below = cat_array_into_da(qi_below_list, model, qi)
    da_at = cat_array_into_da(qi_at_list, model, qi)
    da_above = cat_array_into_da(qi_above_list, model, qi)
    print("got the count data arrays")
    
    # add metadata
    da_below = da_below.rename("ci_count")
    da_below.attrs = {"layer": "-1000m to zcp",
                      "threshold": QI_CRIT,
                      "threshold_units": "kg/kg"}
    da_at = da_at.rename("ci_count")
    da_at.attrs = {"layer": "-500m to +500m",
                   "threshold": QI_CRIT,
                   "threshold_units": "kg/kg"}
    da_above = da_above.rename("ci_count")
    da_above.attrs = {"layer": "zcp to +1000m",
                      "threshold": QI_CRIT,
                      "threshold_units": "kg/kg"}
    
    # save files
    da_below.to_netcdf(out_path + "{m}_cp_cirrus_counts_b1000_to_0.nc".format(m=model))
    print("saved below file")
    da_at.to_netcdf(out_path + "{m}_cp_cirrus_counts_b500_to_a500.nc".format(m=model))
    print("saved at file")
    da_above.to_netcdf(out_path + "{m}_cp_cirrus_counts_0_to_a1000.nc".format(m=model))
    print("saved above file")
    
    
if __name__ == "__main__":
    main()
    