"""
calc_cold_point_cirrus_obs.py

Calculate the number of time steps that each grid point has an ice mixing ratio
above the radiatively-active threshold for a 1 km layer near the cold point.
This script is for the observations (DARDAR, at ERA5 cold point-relative levels)

---------------

usage: calc_cold_point_cirrus_obs.py [-h] -y YEARS -m MONTHS -r REGION -f FILE_PATH -o OUT_PATH 

-------------

"""
import sys
sys.path.append("/home/b/b380887/cold-point-overshoot/python_scripts")
import argparse 
import xarray as xr
import numpy as np
import get_d2_data as get_d2

# radiatively active threshold
QI_CRIT = 2e-6 # kg/kg

# threshold to be considered deep convection (and not cirrus)
CONV_THRESH = 5e-5 # kg/kg


def parse_args():
    """ Parse command-line arguments
    """
    parser = argparse.ArgumentParser()
    
    # required
    parser.add_argument("-y", "--years", nargs='+', help="Year(s) to process", required=True)
    parser.add_argument("-r", "--region",  help="Region to process", required=True)
    parser.add_argument("-m", "--months", help="String of month abbreviation(s) to process", required=True)
    parser.add_argument("-f", "--file_path", help="Input path for IWC files", required=True)
    parser.add_argument("-o", "--out_path", help="Output path for files", required=True)
    
    # optional
    parser.add_argument("-lt", "--lats", nargs=2, help="Latitude range (default= -30 to 10", required=False)
    parser.add_argument("-ln", "--lons", nargs=2, help="Longitude range (default= -180 to 180", required=False)
    parser.add_argument("-n", "--no_conv", action='store_true', help="Exclude convection from the identification of cirrus (i.e., impose an upper limit on cloud ice)", required=False)


    return parser.parse_args()


def get_qi(region, months, file_path, year_list):
    """ 
    Read in the IWC files and convert to qi; returns cold point-relative
    dataset for all levels as well as one with all retrievals (including zeros)
    for getting the total number of retrievals (i.e., including zeros) in
    each time/5x5 box later on.
    """
    qi = get_d2.get_cp_relative_dardar(region, months, file_path, year_list,
                                       unique_times=True)
    qi_no_min = get_d2.get_cp_relative_dardar(region, months, file_path, year_list,
                                               unique_times=True, qi_min=None)["qi_b1000"]
    
    return qi, qi_no_min


def get_1km_layers(qi):
    """ Get data arrays of the layer mean iwc (at, above, below cold point)
    """
    qi_below = xr.DataArray(np.nanmean([qi["qi_b1000"].values, qi["qi_b500"].values, 
                                        qi["qi_cp"].values],axis=0), 
                            dims=qi.dims, coords=qi.coords)
    qi_above = xr.DataArray(np.nanmean([qi["qi_cp"].values, qi["qi_a500"].values, 
                                        qi["qi_a1000"].values], axis=0), 
                            dims=qi.dims, coords=qi.coords)
    qi_at = xr.DataArray(np.nanmean([qi["qi_b500"].values, qi["qi_cp"].values, 
                                    qi["qi_a500"].values], axis=0), 
                         dims=qi.dims, coords=qi.coords)
    
    return qi_below, qi_at, qi_above


def make_empty_count_das(lat_range, lon_range, dx_deg=5, dy_deg=5, return_coord_lists=True):
    """ 
    Make empty (all values 0) data arrays to hold cirrus counts for
    each layer and the total number of retrievals in the XxY boxes. 
    dx_deg and dy_deg are the number of lat/lon degrees in the target boxes (default=5)
    """
    lat_list = np.arange(lat_range[0], lat_range[1] + 0.1, dy_deg)
    lon_list = np.arange(lon_range[0], lon_range[1] + 0.1, dx_deg)
    mean_lats = 0.5*(lat_list[1:] + lat_list[:-1])
    mean_lons = 0.5*(lon_list[1:] + lon_list[:-1])
    
    # total rad active counts in the  boxes
    ci_at_counts = xr.DataArray(
        np.zeros((len(mean_lons), len(mean_lats))),
        dims=["lon", "lat"],
        coords={"lon": mean_lons, "lat": mean_lats}
    )
    ci_above_counts = xr.DataArray(
        np.zeros((len(mean_lons), len(mean_lats))),
        dims=["lon", "lat"],
        coords={"lon": mean_lons, "lat": mean_lats}
    )
    ci_below_counts = xr.DataArray(
        np.zeros((len(mean_lons), len(mean_lats))),
        dims=["lon", "lat"],
        coords={"lon": mean_lons, "lat": mean_lats}
    )

    # total number of retrievals (so xy*time) in the  boxes
    n_retrievals = xr.DataArray(
        np.zeros((len(mean_lons), len(mean_lats))),
        dims=["lon", "lat"],
        coords={"lon": mean_lons, "lat": mean_lats}
    )
    
    if return_coord_lists:
        return_list = [ci_below_counts, ci_at_counts, ci_above_counts, n_retrievals, lat_list, lon_list]
    else:
        return_list = [ci_below_counts, ci_at_counts, ci_above_counts, n_retrievals]

    return return_list


def get_da_in_box(da, latmin, latmax, lonmin, lonmax):
    """ 
    For one data array and one latxlon box, returns a data array of only
    the values within that box
    """
    da_in_box = da.where(da.lon >= lonmin) \
                   .where(da.lon < lonmax) \
                    .where(da.lat >= latmin) \
                    .where(da.lat < latmax).dropna(dim="time")
    return da_in_box


def get_1km_coarse_layer_counts(qi_below, qi_at, qi_above, qi_no_min, lat_range, lon_range, 
                                dx_deg=5, dy_deg=5, qi_crit=QI_CRIT, conv_thresh=CONV_THRESH, no_conv=False):
    """
    Count the number of radiatively active cirrus times for that layer and the number of total retrievals
    (over time and space, including zeros) for each latxlon box.
    """
    output_list = make_empty_count_das(lat_range, lon_range, dx_deg, dy_deg, return_coord_lists=True)
    ci_below_counts, ci_at_counts, ci_above_counts = output_list[0:3]
    n_retrievals = output_list[3]
    lat_list, lon_list = output_list[4:6]
        
    for i in range(len(lat_list)-1):
        for j in range(len(lon_list)-1):
            ci_above_in_box = get_da_in_box(qi_above, lat_list[i], lat_list[i+1], lon_list[j], lon_list[j+1])
            ci_at_in_box = get_da_in_box(qi_at, lat_list[i], lat_list[i+1], lon_list[j], lon_list[j+1])
            ci_below_in_box = get_da_in_box(qi_below, lat_list[i], lat_list[i+1], lon_list[j], lon_list[j+1])

            if no_conv:
                ci_at_counts.values[j, i] = ci_at_in_box.where(ci_at_in_box > qi_crit).where(ci_at_in_box < conv_thresh).count(dim="time").values
                ci_above_counts.values[j, i] = ci_above_in_box.where(ci_above_in_box > qi_crit).where(ci_above_in_box < conv_thresh).count(dim="time").values
                ci_below_counts.values[j, i] = ci_below_in_box.where(ci_below_in_box > qi_crit).where(ci_below_in_box < conv_thresh).count(dim="time").values
            else:
                ci_at_counts.values[j, i] = ci_at_in_box.where(ci_at_in_box > qi_crit).count(dim="time").values
                ci_above_counts.values[j, i] = ci_above_in_box.where(ci_above_in_box > qi_crit).count(dim="time").values
                ci_below_counts.values[j, i] = ci_below_in_box.where(ci_below_in_box > qi_crit).count(dim="time").values

            n_retrievals.values[j, i] = qi_no_min.where(qi_no_min.lon >= lon_list[j], drop=True) \
                                             .where(qi_no_min.lon < lon_list[j+1], drop=True) \
                                             .where(qi_no_min.lat >= lat_list[i], drop=True) \
                                             .where(qi_no_min.lat < lat_list[i+1], drop=True).count(dim="time").values
        
    return ci_below_counts, ci_at_counts, ci_above_counts, n_retrievals


def save_files(da_below, da_at, da_above, out_path, no_conv=False, qi_crit=QI_CRIT, 
               conv_thresh=CONV_THRESH):
    """ Add metadata to the data arrays and save as netcdfs
    """
    # add metadata
    da_below = da_below.rename("ci_count")
    da_at = da_at.rename("ci_count")
    da_above = da_above.rename("ci_count")
    
    if no_conv:
        da_below.attrs = {"layer": "-1000m to zcp",
                          "threshold": qi_crit,
                          "conv_thresh": conv_thresh,
                          "threshold_units": "kg/kg"}
        da_at.attrs = {"layer": "-500m to +500m",
                       "threshold": qi_crit,
                        "conv_thresh": conv_thresh,
                       "threshold_units": "kg/kg"}
        da_above.attrs = {"layer": "zcp to +1000m",
                          "threshold": qi_crit,
                          "conv_thresh": conv_thresh,
                          "threshold_units": "kg/kg"}
    else:
        da_below.attrs = {"layer": "-1000m to zcp",
                          "threshold": qi_crit,
                          "threshold_units": "kg/kg"}
        da_at.attrs = {"layer": "-500m to +500m",
                       "threshold": qi_crit,
                       "threshold_units": "kg/kg"}
        da_above.attrs = {"layer": "zcp to +1000m",
                          "threshold": qi_crit,
                          "threshold_units": "kg/kg"}
    
    # save files
    if no_conv: 
        below_name = out_path + "OBS_cp_cirrus_counts_no_conv_b1000_to_0.nc"
        at_name = out_path + "OBS_cp_cirrus_counts_no_conv_b500_to_a500.nc"
        above_name = out_path + "OBS_cp_cirrus_counts_no_conv_0_to_a1000.nc"
    else:
        below_name = out_path + "OBS_cp_cirrus_counts_b1000_to_0.nc"
        at_name = out_path + "OBS_cp_cirrus_counts_b500_to_a500.nc"
        above_name = out_path + "OBS_cp_cirrus_counts_0_to_a1000.nc"
        
    da_below.to_netcdf(below_name)
    print("saved below file")
    da_at.to_netcdf(at_name)
    print("saved at file")
    da_above.to_netcdf(above_name)
    print("saved above file")
    
    
def main():
    """
    Get the cold point-relative cirrus counts for three layers (above, below, and
    "at" cold point) and save as netcdfs.
    """
    args = parse_args()
    print(args)
    
    year_list = args.years
    file_path = args.file_path
    out_path = args.out_path
    months = args.months
    region = args.region
    lats = args.lats
    lons = args.lons
    no_conv = args.no_conv
    
    if lats is None:
        lats = [-30, 10]
    if lons is None:
        lons = [-180, 180]

    qi, qi_no_min = get_qi(region, months, file_path, year_list)
    qi_below, qi_at, qi_above = get_1km_layers(qi)
    da_below, da_at, da_above, n_retrievals = get_1km_coarse_layer_counts(
        qi_below, qi_at, qi_above, qi_no_min, lats, lons
    )
    
    # save files
    save_files(da_below, da_at, da_above, out_path, no_conv=no_conv)
    
    # save counts
    n_retrievals.to_netcdf(out_path + "OBS_xy_5x5_counts.nc")
    print("saved counts file")

    
if __name__ == "__main__":
    main()
    