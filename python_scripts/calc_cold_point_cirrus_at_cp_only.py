"""
calc_cold_point_cirrus_at_cp_only.py

Calculate the number of time steps that each grid point has an ice mixing ratio
above the radiatively-active threshold at the cold point level.

---------------

usage: calc_cold_point_cirrus_at_cp_only.py [-h] -m MODEL -f FILE_PATH -o OUT_PATH -i INDEX_PATH -c XCHUNKS

-------------

"""
import argparse 
import xarray as xr
import numpy as np


START_DATE = "2020-01-30"
END_DATE = "2020-02-28"

# radiatively active threshold
# QI_CRIT = 2e-6 # kg/kg
QI_CRIT = 4e-6 # kg/kg

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
            qi = qi_td
        elif model == "GEOS" or model == "SCREAM":
            qi = qi_td.reindex(lev=qi_td.lev[::-1])
        elif model == "ICON":
            qi = qi_td.reindex(height=qi_td.height[::-1])
    
    return qi.sel(time=slice(start_date, end_date))
        
    
def get_1km_layer_counts(model, qi, cp_inds, xchunks, qi_crit=QI_CRIT, xdim_dict=XDIM_DICT):
    """ 
    Count the number of times a grid point has a ice at the cold point that 
    exceeds the radiatively active threshold.
    
    Use this one for all models.
    
    ***this function title does not reflect what it actually does***
    """
    xdim = xdim_dict[model]
    
    nx = int(np.ceil(len(qi[xdim])/xchunks))
    qi_cp_list = [[]]*nx 

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
        elif model == "ICON":
            inds_mini = cp_inds.isel(cell=slice(start_ind, end_ind)).astype(int)
            qi_mini = qi.isel(cell=slice(start_ind, end_ind))
            qi_cp = qi_mini.isel(height=inds_mini).values
        elif model == "SAM": 
            inds_mini = cp_inds.isel(lon=slice(start_ind, end_ind)).astype(int)
            qi_mini = qi.isel(lon=slice(start_ind, end_ind))
            inds_mini = inds_mini.assign_coords(lat=qi_mini.lat)
            # for SAM - some decimal lat values got truncated in the reindexing;
            # set them equal again
            qi_cp = qi_mini.isel(z=inds_mini).values
        elif model == "GEOS":
            inds_mini = cp_inds.isel(Xdim=slice(start_ind, end_ind)).astype(int)
            qi_mini = qi.isel(Xdim=slice(start_ind, end_ind))
            qi_cp = qi_mini.isel(lev=inds_mini).values
        elif model == "SCREAM":
            inds_mini = cp_inds.isel(ncol=slice(start_ind, end_ind)).astype(int)
            qi_mini = qi.isel(ncol=slice(start_ind, end_ind))
            qi_cp = qi_mini.isel(lev=inds_mini).values
            
        # count the number of times the mean of the 1000m layer exceeds the threshold
        if model == "SAM":
            qi_cp_ra = np.sum(np.where(qi_cp/1000. > qi_crit, 1, 0), axis=0)
        else:
            qi_cp_ra = np.sum(np.where(qi_cp > qi_crit, 1, 0), axis=0)

        # add to a list - will later concatenate these and give it the xdimension
        qi_cp_list[i] = qi_cp_ra

        print(i+1, "done out of", nx)
    
    return qi_cp_list


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
    Get the cold point-relative cirrus counts for the cold point layer
    and save as netcdfs.
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
    
    qi_cp_list = get_1km_layer_counts(model, qi, cp_inds, xchunks)
    print("got the count list")
        
    # make into data arrays
    da_cp = cat_array_into_da(qi_cp_list, model, qi)
    print("got the count data array")
    
    # add metadata
    da_cp = da_cp.rename("ci_count")
    da_cp.attrs = {"level": "zcp",
                      "threshold": QI_CRIT,
                      "threshold_units": "kg/kg"}
    
    # save files
    da_cp.to_netcdf(out_path + "{m}_cp_cirrus_counts_at_zcp.nc".format(m=model))
    print("saved zcp file")
    
    
if __name__ == "__main__":
    main()
    