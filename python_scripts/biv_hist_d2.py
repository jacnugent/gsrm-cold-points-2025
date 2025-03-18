"""
biv_hist_d2.py

Script to calculate bivariate histogram (cold point temperature
and brightness temperature) for the DYAMOND2 models. Saves the 
histogram as a dictionary.

------------------
usage: biv_hist.py [-h] -f FILE_PATH -r REGION -m MODEL
                   [-p SAVE_PICKLE_PATH] [-c CHUNK_SIZE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file_path FILE_PATH
                        Input path for files
  -r REGION, --region REGION
                        Region abbreviation
  -m MODEL, --months MODEL
                        Model name
  -p SAVE_PICKLE_PATH, --save_pickle_path SAVE_PICKLE_PATH
                        Output path to save pickle files (default =
                        file_path)
  -c CHUNK_SIZE, --chunk_size CHUNK_SIZE
                        Chunk size (number elements) to compute the
                        histogram
------------------       

Assumes the following file name convention:
* OLR: {m}_OLR_winter_{r}.nc
* temperature: {m}_temp_025_remapped_{r}.nc (for all but SAM)
* temperature (SAM ONLY): {m}_temp_12-20km_winter_{r}.nc

Saves the dictionary as
    {m}_Tb-cpT_hist_dict_{r}.pickle

Default bins are (175, 176, ..., 205) K for cold point
and (175, 180, 185, ..., 330) K for brightness temperature.
"""
import argparse
import sys
sys.path.append("/home/b/b380887/cold-point-overshoot/python_scripts")
import pickle
import xarray as xr
import numpy as np
import get_d2_data as get_d2


# bins for the bivariate histogram
CPT_BINS = np.arange(175, 206, 1)
TB_BINS = np.arange(175, 331, 5)

# start/end date for the files (drop spinup)
START_DATE = "2020-01-30"
END_DATE = "2020-02-28"


def parse_args():
    """ Parse command-line arguments
    """
    parser = argparse.ArgumentParser()
    
    # required
    parser.add_argument("-f", "--file_path", help="Input path for files", required=True)
    parser.add_argument("-r", "--region", help="Region abbreviation", required=True)
    parser.add_argument("-m", "--model", help="Model name", required=True)

    # optional
    parser.add_argument("-p", "--save_pickle_path", help="Output path to save pickle files (default = file_path)")
    parser.add_argument("-c", "--chunk_size", help="Chunk size (number elements) to compute the histogram", default="5e6")

    return parser.parse_args()


def compute_histogram(model, cpT, tb, tb_count, tb_bins=TB_BINS, cpT_bins=CPT_BINS, use_dask=False):
    """ 
    Compute the bivariate (cold point temp & brightness temp) histogram.
    
    Returns the dict with the histogram counts, x & y bins and edges, and 
    length of non-nan brightness temperature elements (need to get from histogram
    counts to frequencies).
    """
    # fix time step issues
    if model == "SHIELD" or model == "ICON":
        tb = tb.sel(time=cpT.time)

    binned_stat, xedges, yedges = np.histogram2d(cpT.values.flatten(), tb.values.flatten(), bins=(cpT_bins, tb_bins))
    
    hist_dict = {
        "hist_computed": binned_stat, 
        "xedges": xedges, 
        "yedges": yedges, 
        "tb_bins": tb_bins, 
        "cpT_bins": cpT_bins,
        "nan_len": int(tb_count),
    }
    return hist_dict


def main():
    """ docstring
    """
    args = parse_args()
    print(args)

    file_path = args.file_path
    region = args.region
    months = args.months
    save_pickle_path = args.save_pickle_path
    chunk_size = float(args.chunk_size)
    
    if file_path[-1] != "/":
        file_path = file_path + "/"
    if save_pickle_path is None:
        save_pickle_path = file_path
    else:
        if save_pickle_path[-1] != "/":
            save_pickle_path = save_pickle_path + "/"
    
    cpT = get_d2.get_cold_point(region, model, file_path)
    tb = get_d2.get_brightness_temp(region, model, file_path)
    tb_count = tb.count().values
    
    # compute & save histogram dictionary
    dict_file_name = "{m}_Tb-cpT_hist_dict_{r}.pickle".format(m=model, r=region)
    hist_dict = compute_histogram(model, cpT, tb, tb_count)
    with open(save_pickle_path + dict_file_name, "wb") as handle:
        pickle.dump(hist_dict, handle)
    print("Dictionary saved to " + save_pickle_path + dict_file_name)
    

if __name__ == "__main__":
    main()      
