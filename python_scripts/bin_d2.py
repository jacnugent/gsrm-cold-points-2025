"""
bin_d2.py

Script to save all binned dictionaries for each model/region.

------
usage: bin_d2.py [-h] -f FILE_PATH -r REGION -m MODEL -p
                 SAVE_PICKLE_PATH [-c CONV_THRESH]

options:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file_path FILE_PATH
                        Input path for files
  -r REGION, --region REGION
                        Region abbreviation
  -m MODEL, --model MODEL
                        Model name
  -p SAVE_PICKLE_PATH, --save_pickle_path SAVE_PICKLE_PATH
                        Output path to save pickle files
-----

"""
import argparse
import pickle
import dask
import sys
sys.path.append("/home/b/b380887/cold-point-overshoot/python_scripts/")

import xarray as xr
import numpy as np
import bin_overshoot as bin_os
import get_d2_data as get_d2

from dask.diagnostics import ProgressBar


IND_OFFSETS_DICT = {
    "SCREAM": [-4, -2, 0, 2, 4],
    "GEOS": [-4, -2, 0, 2, 4],
    "SHIELD": [-2, -1, 0, 1, 2],
    "SAM": [-2, -1, 0, 1, 2],
    "ICON": [-2, -1, 0, 1, 2],
}
DIFF_BINS = np.arange(-20, 101, 2)
CONV_THRESH = 5e-5 # kg/kg
RACP_THRESH = 2e-6 # kg/kg


def parse_args():
    """ Parse command-line arguments
    """
    parser = argparse.ArgumentParser()
    
    # required
    parser.add_argument("-f", "--file_path", help="Input path for files", required=True)
    parser.add_argument("-r", "--region", help="Region abbreviation", required=True)
    parser.add_argument("-m", "--model", help="Model name", required=True)
    parser.add_argument("-p", "--save_pickle_path", help="Output path to save pickle files", required=True)

    # optional
    parser.add_argument("-c", "--conv_thresh", help="Threshold for convective ice (in kg/kg)", default="5e-5")
    parser.add_argument("-d", "--diff_bins", help="Bins for the Tb-Tcp differences (K)")
    
    return parser.parse_args()


def main():
    """ 
    Get the data, do the binning, and save the dictionary 
    to a pickle file for one model/region.'
    """
    args = parse_args()
    print(args)
    
    region = args.region
    model = args.model
    file_path = args.file_path
    conv_thresh = args.conv_thresh
    pickle_dir = args.save_pickle_path
    
    diff_bins = DIFF_BINS
    if conv_thresh is None:
        conv_thresh = CONV_THRESH
    else:
        conv_thresh = float(conv_thresh)
    racp_thresh = RACP_THRESH
    
    # get the data
    tb = get_d2.get_brightness_temp(region, model, file_path)
    cpT, cp_inds = get_d2.get_cold_point(region, model, file_path, return_inds=True)
    
    # for RACP cirrus: get ice only, except for SCREAM
    if model == "SCREAM":
        qi = get_d2.get_qtot(region, model, file_path)
    else:
        qi = get_d2.get_qi(region, model, file_path)
        
    # can only get ice for SAM or ICON
    if model == "SAM" or model == "ICON":
        qtot = get_d2.get_qi(region, model, file_path)
    else:
        qtot = get_d2.get_qtot(region, model, file_path)
    if model == "SHIELD" or model == "GEOS":
        qsg = get_d2.get_qsg(region, model, file_path)
    
    diffs = tb - cpT
    
    ind_offsets = IND_OFFSETS_DICT[model]


    # total frozen - all, just above the convective threshold, and just above the RACP cirrus threshold
    if model == "SAM" or model == "ICON":
        varname = "qi"
    else:
        varname = "qtot"
    varname_conv = varname + "_conv"
    # qtot_means_dict, qtot_counts_dict, _ = bin_os.bin_var_by_diffs(qtot, diffs, diff_bins,
    #                                                            cp_inds, ind_offsets=ind_offsets,
    #                                                            save_dicts=True, save_dir=pickle_dir, model=model,
    #                                                            region=region, variable=varname)
    qtot_conv_means_dict, qtot_conv_counts_dict, _ = bin_os.bin_var_by_diffs(qtot.where(qtot > conv_thresh), diffs, 
                                                                             diff_bins, cp_inds, 
                                                                             ind_offsets=ind_offsets,
                                                                             save_dicts=True, save_dir=pickle_dir, 
                                                                             model=model, region=region, 
                                                                             variable=varname_conv)
    
    
#     # for RACP (cloud ice for all except SCREAM)
#     if model == "SCREAM":
#         varname = "qtot"
#     else:
#         varname = "qi"
#     varname_racp = varname + "_racp"    
#     qtot_racp_means_dict, qtot_racp_counts_dict, _ = bin_os.bin_var_by_diffs(qi.where(qi > racp_thresh), diffs, 
#                                                                              diff_bins, cp_inds, 
#                                                                              ind_offsets=ind_offsets,
#                                                                              save_dicts=True, save_dir=pickle_dir, 
#                                                                              model=model, region=region, 
#                                                                              variable=varname_racp)
    
    # # snow and graupel only - all and just above the convective threshold
    # if model == "SHIELD" or model == "GEOS":
    #     qsg_means_dict, qsg_counts_dict, _ = bin_os.bin_var_by_diffs(qsg, diffs, diff_bins,
    #                                                                    cp_inds, ind_offsets=ind_offsets,
    #                                                                    save_dicts=True, save_dir=pickle_dir, model=model,
    #                                                                    region=region, variable="qsg")
    #     qsg_conv_means_dict, qsg_conv_counts_dict, _ = bin_os.bin_var_by_diffs(qsg.where(qsg > conv_thresh), diffs, 
    #                                                                            diff_bins, cp_inds, 
    #                                                                             ind_offsets=ind_offsets,
    #                                                                             save_dicts=True, save_dir=pickle_dir, 
    #                                                                             model=model, region=region, 
    #                                                                             variable="qsg_conv")


if __name__ == "__main__":
    main()     
    