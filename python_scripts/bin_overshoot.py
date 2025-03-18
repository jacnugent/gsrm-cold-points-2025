"""
bin_overshoot.py

Module to make plots of variables binned
by OLR and IWP/FWP to identify a metric/proxy
for overshooting convection.
"""
import pickle
import dask
import sys
sys.path.append("/home/b/b380887/cold-point-overshoot/python_scripts/")

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import model_grid as mg

from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter
from scipy.stats import binned_statistic
from dask.diagnostics import ProgressBar


FILE_PATH = "/work/bb1153/b380887/10x10/"
GLOBAL_PATH = "/work/bb1153/b380887/global_tropics/"
SAVE_PATH = "/home/b/b380887/cold-point-overshoot/plots/osc_metric/"
PICKLE_DIR = "/home/b/b380887/cold-point-overshoot/pickle_files/osc/"

START_DATE = "2020-01-30"
END_DATE = "2020-03-01"

QI_MIN = 1e-8
QG_MIN = 0

ZNAME_DICT = {"NICAM": "lev",
              "SAM": "z",
              "SCREAM": "lev",
              "ICON": "height",
              "SHIELD": "pfull_ref",
              "GEOS": "lev"
             }
DIFF_BINS = np.arange(-20, 101, 2)


# ------ Data/binning functions ------ #

def bin_var_by_diffs(var_to_bin, diffs, bins, cp_inds, zname=None,
                     ind_offsets=[-2, -1, 0, 1, 2], save_dicts=False, 
                     save_dir=PICKLE_DIR, model=None, region=None, 
                     variable=None):
    """ 
    **** this is the one to use****
    
    Bin `var_to_bin` by `diffs` (Tb - Tcp) at `bins` at levels offset 
    from cold point index (`cp_inds`, `ind_offsets`).
    `zname` is the name of the zcoordinate ("lev", "height", etc.) 
    Returns [bin mean dict, bin count dict, bins] where the dicts have 
    key of dz relative to cold point (e.g., -500 = 500m below) and 
    list of binned statistics as items.. 
    """
    offset_dict = dict(zip([-1000, -500, 0, 500, 1000], ind_offsets))
    var_bin_means = {}
    var_bin_counts = {}
    
    if zname is None:
        zname = ZNAME_DICT[model]
        
    # fix time steps
    if model == "SHIELD":
        diffs = diffs.sel(time=var_to_bin.time)
        cp_inds = cp_inds.sel(time=var_to_bin.time)
    
    for i, dz in enumerate(list(offset_dict.keys())):
        offset = offset_dict[dz]
        if zname.lower() == "z":
            var_lev, values_nonan = da_to_nonans(var_to_bin.isel(z=cp_inds+offset), diffs)
        elif zname.lower() == "pfull_ref":
            var_lev, values_nonan = da_to_nonans(var_to_bin.isel(pfull_ref=cp_inds+offset), diffs)
        elif zname.lower() == "height":
            var_lev, values_nonan = da_to_nonans(var_to_bin.isel(height=cp_inds+offset), diffs)
        elif zname.lower() == "lev":
            var_lev, values_nonan = da_to_nonans(var_to_bin.isel(lev=cp_inds+offset), diffs)

        
        means, _, _ = binned_statistic(values_nonan, var_lev, statistic="mean", bins=bins)
        counts, _, _ = binned_statistic(values_nonan, var_lev, statistic="count", bins=bins)
        var_bin_means[dz] = np.where(counts > 0, means, np.nan)
        var_bin_counts[dz] = np.where(counts > 0, counts, np.nan)
        
    if save_dicts:
        if save_dir is None or variable is None or model is None or region is None:
            raise Exception("Must input save_dir, variable, model, AND region if you want to save the dictionaries")        
        mean_name = save_dir + "{m}_{v}_bin_means_{r}.pickle".format(m=model, v=variable, r=region)
        count_name = save_dir + "{m}_{v}_bin_counts_{r}.pickle".format(m=model, v=variable, r=region)
        with open(mean_name, 'wb') as handle:
            pickle.dump(var_bin_means, handle)
        with open(count_name, 'wb') as handle:
            pickle.dump(var_bin_counts, handle)
    
    return [var_bin_means, var_bin_counts, bins]
        
        
                
def bin_variable(var_to_bin, values, bins, zname, cp_inds,
                 ind_offsets=[-2, -1, 0, 1, 2], statistic="mean", drop_ts=False, save=False, save_dir=PICKLE_DIR, model=None, region=None,
                variable=None):
    """ 
    Bin `var_to_bin` by `values` with `bins` at levels offset from cold point index (`cp_inds`, 
    `ind_offsets`). Returns the binned statistic (defualt = mean). 
    `zname` is the name of the zcoordinate ("lev", "height", etc.) 'drop_ts` is true for NICAM so you drop the last time step.
    """
    bin_means = np.zeros((len(ind_offsets), len(bins)-1))
    
    for i, offset in enumerate(ind_offsets):
        if zname.lower() == "z":
            var_lev, values_nonan = da_to_nonans(var_to_bin.isel(z=cp_inds+offset), values)
        elif zname.lower() == "pfull_ref":
            var_lev, values_nonan = da_to_nonans(var_to_bin.isel(pfull_ref=cp_inds+offset), values)
        elif zname.lower() == "height":
            var_lev, values_nonan = da_to_nonans(var_to_bin.isel(height=cp_inds+offset), values)
        elif zname.lower() == "lev":
            if drop_ts:
                var_lev, values_nonan = da_to_nonans(var_to_bin.isel(lev=cp_inds+offset).isel(time=slice(None, -1)), values)
            else:
                var_lev, values_nonan = da_to_nonans(var_to_bin.isel(lev=cp_inds+offset), values)

            
        mean_var, bin_edges, inds = binned_statistic(values_nonan, var_lev, 
                                                     statistic=statistic, bins=bins)
        bin_means[i, :] = mean_var
        
    if save:
        bin_mean_dict = dict(zip(ind_offsets, bin_means))
        if type(statistic) is not str:
            stat = "custom"
        else:
            stat = statistic
        out_path = save_dir + "{m}_{v}_bin_{s}_{r}.pickle".format(m=model, v=variable, s=stat, r=region)
        
        with open(out_path, 'wb') as handle:
            pickle.dump(bin_mean_dict, handle)

    return bin_means


def save_hist(values, bins, model, varname, region, bin_range=None,
              out_path=PICKLE_DIR):
    """
    Save pickle file with the histogram
    """
    if bin_range is None:
        bin_range = [bins[0], bins[-1]]
                     
    counts, edges = np.histogram(values, bins=bins, range=bin_range)
    freqs = counts / counts.sum()
    hist_dict = {"counts": counts, "freqs": freqs, "bin_edges": edges}
    
    out_file = out_path + "{m}_{v}_histogram_dict_{r}.pickle".format(m=model, v=varname, r=region)
    with open(out_file, 'wb') as handle:
        pickle.dump(hist_dict, handle)
        
    return hist_dict
    

def bin_single_level(var_to_bin, values, bins, statistic="mean"):
    """
    Bin a variable by another at a single level (e.g., if you
    already have the data sorted into the [-1, -.5, 0, +.5, +1] levels
    for cold point-relative coordinates)
    
    Don't save this one here (easier to do separately once you calc for all)
    """
    var_lev, values_nonan = da_to_nonans(var_to_bin, values)

    mean_var, bin_edges, inds = binned_statistic(values_nonan, var_lev,
                                                 statistic=statistic, bins=bins)

    return mean_var
    
    
    
# ------ Helper functions ------ #

def da_to_nonans(da1, da2=None):
    """ 
    Convert a data array to a flattened numpy array with
    nans removed. If a second array is given (da2), removes
    indices where da1 = nan
    """
    da_flat = da1.values.flatten()
    no_nans1 = da_flat[~np.isnan(da_flat)]
    
    if da2 is not None:
        da2_when_d1nonan = da2.values.flatten()[~np.isnan(da_flat)]
        return no_nans1, da2_when_d1nonan
    else:
        return no_nans1
    
    
def w_colormap(w_bins):
    """ 
    Create colormap of w centered on zero/white based on 20 (prev. 21) bins.
    Centered on zero/white. Based on the "bwr" colormap. Default is
    6 negative bins (note: NOT bin edges).
    """
    w_colors = [
        "#1A00FF",
        # "#311AFF",
        "#4833FF",
        # "#5F4DFF",
        "#7666FF",
        # "#8D80FF",
        "#A499FF",
        # "#BBB3FF",
        "#D2CCFF",
        "#E9E6FF",
        # "#FFFFFF", # zero bin
        "#FFDCDB",
        "#FFC3C2",
        # "#FFAAA8",
        "#FF918F",
        # "#FF7775",
        "#FF6361",
        # "#FF4947",
        "#FF3533",
        # "#FF211F",
        "#FF0200"
    ]
    
    cmap = mcolors.ListedColormap(w_colors)
    norm = mcolors.BoundaryNorm(w_bins, len(w_bins) - 1)

    return cmap, norm


# ------ Plotting functions ------ #

def plot_diffs_hist(diffs, model, region, bins=DIFF_BINS, 
                    fsize=13, tsize=14, figsize=(7, 4), ylim=(0, 0.035), 
                    gridlines=True, save=False, save_dir=None,
                    return_hist=False, chunks={"time": 8}, ylog=True):
    """
    Plot a histogram of (brightness temperature - cold point 
    temperature). 
    Note - using dask for the histogram can cause some weird issues at
    the extreme bins - try to avoid (set chunks=None) if you can.
    """
    fig, ax = plt.subplots(figsize=figsize)
    n_pts = diffs.size
    if chunks is not None:
        diffs_chunked = diffs.chunk(chunks)
        diffhist, bin_edges = dask.array.histogram(diffs_chunked, bins=bins, range=[bins[0], bins[-1]])
        with ProgressBar():
            hist_comp = diffhist.compute()
    else:
        hist_comp, bin_edges = np.histogram(diffs.values.flatten(), bins=bins, range=[bins[0], bins[-1]])
    bin_means = 0.5*(bin_edges[:-1] + bin_edges[1:])
    
    ax.bar(bin_means, hist_comp/n_pts, width=2, edgecolor="w")    
    ax.set_ylabel("Frequency", fontsize=fsize)
    ax.set_xlabel("$T_b - T_{CP}$ (K)", fontsize=fsize)
    ax.set_xlim((bins[0], bins[-1]))
    if ylog:
        ax.set_yscale("log")
        ax.set_ylim((1e-5, 1))
    else:
        ax.set_ylim(ylim)
    ax.tick_params(axis="both", labelsize=fsize-1)  
    if gridlines:
        ax.grid(color="grey", linestyle=":")    
    ax.set_title("{m} ({r}): frequency of ($T_b - T_{s}$) bins".format(m=model, r=region, s="CP"),
            fontsize=tsize
        )    
    if save:
        if save_dir is None:
            raise Exception("Must provide save_dir if you want to save the plot")
        plt.savefig(save_dir + "{m}_Tb-cpT_bin_frequency_{r}.png".format(m=model, r=region))
    plt.show()
    
    if return_hist:
        return hist_comp, bins, bin_edges, n_pts
            
        
def plot_quick_hist(values, model, region, bins, varname, shortname, units, fsize=13, 
                    tsize=14, figsize=(7, 4), zoom=False, ylog=False, ylim=None,
                    gridlines=False, annotation=None, save=False, save_dir=None):
    """ 
    Plot a simple histogram of the variable you're binning by (OLR, Tb, FWP) for one 
    model/region
    """
    fig, ax = plt.subplots(figsize=figsize)
    n_pts = len(values.values.flatten())
    weights = np.ones((n_pts)) / float(n_pts)
    n, bins, patches = ax.hist(values.values.flatten(), weights=weights, bins=bins,
                                edgecolor="w")
    ax.set_ylabel("Frequency", fontsize=fsize)
    ax.set_xlabel("{n} ({u})".format(n=varname, u=units), fontsize=fsize)
    ax.set_title("{m} ({r}): frequency of {s} bins".format(m=model, r=region, s=shortname),
                 fontsize=tsize
                )
    ax.set_xlim((bins[0], bins[-1]))
    if shortname == "FWP":
        ax.set_xscale("log")
        ax.invert_xaxis()
        
    if ylog:
        ax.set_yscale("log")
        ax.set_ylim(ylim)
    else:
        if ylim is None:
            ax.set_ylim(bottom=0)
        else:
            ax.set_ylim(ylim)
            
    ax.tick_params(axis="both", labelsize=fsize-1)
    
    if annotation is not None:
        ax.annotate(annotation, xy=(0.05, 0.9), xycoords="axes fraction", fontsize=fsize-1)
    
    if gridlines:
        ax.grid(color="grey", linestyle=":")
    
    if save:
        if zoom:
            plt.savefig(save_dir + \
                        "{m}_{s}_bin_frequency_zoomed_{r}.png".format(m=model, 
                                                                      r=region,
                                                                      s=shortname), 
                        dpi=300, 
                        bbox_inches="tight"
                       )
        else:
            if ylog:
                plt.savefig(save_dir + "{m}_{s}_bin_frequency_{r}_ylog.png".format(m=model,
                                                                                   r=region,
                                                                                   s=shortname), 
                            dpi=300, 
                            bbox_inches="tight"
                           )
            else:
                plt.savefig(save_dir + "{m}_{s}_bin_frequency_{r}.png".format(m=model,
                                                                              r=region,
                                                                              s=shortname), 
                            dpi=300, 
                            bbox_inches="tight"
                           )
    
    plt.show()

    
# def plot_binned_by_var(qi_bin_means, qv_bin_means, w_bin_means, qg_bin_means, cp_inds, model, region, 
#                        ind_offsets, values, bins, bin_varname, bin_units, bin_shortname, 
#                        offset_labs=None, qi_lims=None, qg_lims=None, qv_lims=None, w_lims=None, fsize=16, 
#                        qv_ppmv=False, tsize=18, figsize=[13, 17], colormap="Spectral", zoom=False, 
#                        save=False, save_dir=None):


def plot_binned_by_var(qi_bin_means, w_bin_means, qg_bin_means, cp_inds, model, region, 
                       ind_offsets, values, bins, bin_varname, bin_units, bin_shortname, 
                       offset_labs=None, qi_lims=None, qg_lims=None, w_lims=None, w_bins=None, fsize=16, 
                       tsize=18, figsize=[13, 13], w_cmap="Spectral", colormap="Spectral", zoom=False, 
                       save=False, save_dir=None, statistic=None):
    """ 
    Plot variables binned by another variable at levels relaive to the cold point.
    Currently supports qi, qg (if available), and w.
    """
    # labels for offset from cold point
    if offset_labs is None:
        offset_labs = ["~1000 m below", 
               "~500 m below", 
               "At cold point", 
               "~500 m above", 
               "~1000 m above"
              ]

    # # w colormap (bins based on each model's max abs value)
    # if w_bins is None:
    #     max_abs = np.nanmax(np.abs(w_bin_means))
    #     min_abs = np.nanmin(np.abs(w_bin_means))
    #     pos_bins = np.logspace(np.log10(min_abs), np.log10(max_abs), 11)
    #     neg_bins = -1*pos_bins[::-1]
    #     w_bins = [*neg_bins, *pos_bins]
    # w_cmap, w_norm = w_colormap(w_bins)
    
    # colormap limits for qi and qg
    if qi_lims is None:
        # qi_lims = (1e-8, 5e-4)
        qi_lims = (1e-6, 5e-4)
    if qg_lims is None:
        qg_lims = (1e-7, 1e-3)
    if w_lims is None:
        w_lims = (-1, 1)
    # if qv_lims is None:
    #     qv_lims = (5e-7, 1e-6)

    # set up the figure (skip graupel if needed)
    fig = plt.figure(figsize=figsize)
    plt.subplots_adjust(hspace=0.5)

    # for counts - only plot ice
    if w_bin_means is None and qg_bin_means is None:
        gs = GridSpec(1, 1, height_ratios=[1])
        ax1 = fig.add_subplot(gs[0]) # ice
        
    # for means
    else:
        # gs = GridSpec(4, 1, height_ratios=[1, 1, 1, 1])
        gs = GridSpec(3, 1, height_ratios=[1, 1, 1])
        ax1 = fig.add_subplot(gs[0]) # ice
        # ax2 = fig.add_subplot(gs[1]) # wv
        if qg_bin_means is None:
            # ax3 = fig.add_subplot(gs[2]) # w
            # ax4 = fig.add_subplot(gs[3]) # graupel
            # ax4.axis("off")
            ax3 = fig.add_subplot(gs[1]) # w
            ax4 = fig.add_subplot(gs[2]) # graupel
            ax4.axis("off")
        else:
            # ax3 = fig.add_subplot(gs[3]) # w
            # ax4 = fig.add_subplot(gs[2]) # graupel
            ax3 = fig.add_subplot(gs[2]) # w
            ax4 = fig.add_subplot(gs[1]) # graupel


    # plot against avg of bin edges so the tick marks line up with the edges
    bin_mean_values = (bins[:-1] + bins[1:])/2
    # bin_mean_values = bins
    
    # qi
    if statistic is None:
        qi_pcm = ax1.pcolormesh(bin_mean_values, ind_offsets, qi_bin_means, cmap=colormap,
                                norm=mcolors.LogNorm(vmin=qi_lims[0], vmax=qi_lims[1]))
    else:
        qi_pcm = ax1.pcolormesh(bin_mean_values, ind_offsets, qi_bin_means, cmap=colormap,
                                vmin=qi_lims[0], vmax=qi_lims[1])
    ax1.set_yticks(ind_offsets)
    ax1.set_yticklabels(offset_labs)
    ax1.tick_params(axis="y", labelsize=fsize, length=0)
    if statistic == "count":
        cb_qi = plt.colorbar(qi_pcm, ax=ax1, fraction=0.046, pad=0.04, extend="max")
        ax1.set_title("Bin count", fontsize=fsize+1)
        cb_qi.ax.tick_params(labelsize=fsize)
        cb_qi.set_label("Count", fontsize=fsize)
    else:
        cb_qi = plt.colorbar(qi_pcm, ax=ax1, fraction=0.046, pad=0.04, extend="both")
        ax1.set_title("Cloud ice", fontsize=fsize+1)
        cb_qi.ax.tick_params(labelsize=fsize)
        cb_qi.set_label("Cloud ice (kg/kg)", fontsize=fsize)
    
    # # qv
    # if qv_lims is None:
    #     if qv_ppmv:
    #         qv_pcm = ax2.pcolormesh(bin_mean_values, ind_offsets, qv_bin_means, cmap=colormap, vmin=1, vmax=6)
    #     else:
    #         qv_pcm = ax2.pcolormesh(bin_mean_values, ind_offsets, qv_bin_means, cmap=colormap,
    #                                 norm=mcolors.LogNorm())
    # else:
    #     qv_pcm = ax2.pcolormesh(bin_mean_values, ind_offsets, qv_bin_means, cmap=colormap,
    #                             norm=mcolors.LogNorm(vmin=qv_lims[0], vmax=qv_lims[1]))
    # cb_qv = plt.colorbar(qv_pcm, ax=ax2, fraction=0.046, pad=0.04, extend="both")
    # ax2.set_yticks(ind_offsets)
    # ax2.set_yticklabels(offset_labs)
    # ax2.tick_params(axis="y", labelsize=fsize, length=0)
    # cb_qv.ax.tick_params(labelsize=fsize)
    # if qv_ppmv:
    #     ax2.set_title("Water vapor", fontsize=fsize+1)
    #     cb_qv.set_label("Water vapor (ppmv)", fontsize=fsize)
    # else:
    #     ax2.set_title("Specific humidity", fontsize=fsize+1)
    #     cb_qv.set_label("Specific humidity (kg/kg)", fontsize=fsize)
    
    
    # w 
    if w_bin_means is not None:
        # change the ticklabels to scientific notation
        fmt = lambda x, pos: '{:.1e}'.format(x)

        # w_cmap, w_norm = w_colormap(w_bins) # divergent color map
        w_cmap = "bwr"
        w_norm = mcolors.SymLogNorm(linthresh=1e-2, linscale=1, vmin=-1, vmax=1, base=10)
        w_pcm = ax3.pcolormesh(bin_mean_values, ind_offsets, w_bin_means, cmap=w_cmap, norm=w_norm)

        # normal (linear color scale, min/max)
        # w_pcm = ax3.pcolormesh(bin_mean_values, ind_offsets, w_bin_means, cmap=w_cmap,  vmin=w_lims[0], vmax=w_lims[1])  



        # w_pcm = ax3.pcolormesh(bin_mean_values, ind_offsets, w_bin_means, cmap=w_cmap, #cmap="Spectral", 
        #                        vmin=w_lims[0], vmax=w_lims[1], 
        #                        #cmap=w_cmap, norm=w_norm
        #                       )
        cb_w = plt.colorbar(w_pcm, ax=ax3, fraction=0.046, pad=0.04, extend="both")#, format=FuncFormatter(fmt))
        ax3.set_yticks(ind_offsets)
        ax3.set_yticklabels(offset_labs)
        ax3.tick_params(axis="y", labelsize=fsize, length=0)
        ax3.set_title("Vertical velocity", fontsize=fsize+1)
        cb_w.ax.tick_params(labelsize=fsize)
        cb_w.set_label("w (m/s)", fontsize=fsize)
    

    # graupel - if you have it
    if qg_bin_means is not None:
        qg_pcm = ax4.pcolormesh(bin_mean_values, ind_offsets, qg_bin_means, 
                                cmap="Spectral",
                                norm=mcolors.LogNorm(vmin=qg_lims[0], vmax=qg_lims[1])
                               )
        cb_qg = plt.colorbar(qg_pcm, ax=ax4, fraction=0.046, pad=0.04, extend="both")
        ax4.set_yticks(ind_offsets)
        ax4.set_yticklabels(offset_labs)
        ax4.tick_params(axis="y", labelsize=fsize, length=0)
        ax4.set_title("Graupel", fontsize=fsize+1)
        cb_qg.ax.tick_params(labelsize=fsize)
        cb_qg.set_label("Graupel (kg/kg)", fontsize=fsize)
        if zoom:
            ax4.set_xticks(bins)
        else:
            ax4.set_xticks(bins[::2])
        ax4.set_xlabel("{n} ({u})".format(n=bin_varname, u=bin_units), fontsize=fsize)
        ax4.tick_params(axis="x", rotation=45, labelsize=fsize-2)
        if bin_shortname == "FWP":
            ax4.set_xscale("log")
            ax4.invert_xaxis()

    # format x axes
    if w_bin_means is None:
        ax_list = [ax1]
    else:
        ax_list = [ax1, ax3]
        
    for ax in ax_list: #ax2]:
        if zoom:
            ax.set_xticks(bins)
        else:
            ax.set_xticks(bins[::2])        
        ax.set_xlabel("{n} ({u})".format(n=bin_varname, u=bin_units), fontsize=fsize)
        ax.tick_params(axis="x", rotation=45, labelsize=fsize-2)
        if bin_shortname == "FWP":
            ax.set_xscale("log")
            ax.invert_xaxis()

    # add horizontal borders
    for ind in ind_offsets[:-1]:
        if model == "SCREAM" or model == "GEOS":
            gap = 1
        else:
            gap = 0.5
        ax1.axhline(ind+gap, color="k", linewidth=2)
        # ax2.axhline(ind+gap, color="k", linewidth=2)
        if w_bin_means is not None:
            ax3.axhline(ind+gap, color="k", linewidth=2)
        if qg_bin_means is not None:
            ax4.axhline(ind+gap, color="k", linewidth=2)

    plt.suptitle("{m} ({r})".format(m=model, r=region), fontsize=tsize)

    if save:
        if zoom:
            plt.savefig(save_dir + \
                        "{m}_qi_qg_w_binned_by_{s}_zoomed_{r}.png".format(m=model,
                                                                             r=region,
                                                                             s=bin_shortname
                                                                            ), 
                        dpi=300, 
                        bbox_inches="tight"
                       )
        else:
            if statistic is None:
                plt.savefig(save_dir + "{m}_qi_qg_w_binned_by_{s}_{r}.png".format(m=model,
                                                                                     r=region,
                                                                                     s=bin_shortname
                                                                                    ), 
                            dpi=300, 
                            bbox_inches="tight"
                           )
            else:
                plt.savefig(save_dir + "{m}_qi_qg_w_binned_by_{s}_{t}_{r}.png".format(m=model,
                                                                         r=region,
                                                                         s=bin_shortname,
                                                                                      t=statistic
                                                                        ), 
                dpi=300, 
                bbox_inches="tight"
               )

    plt.show()



    
    
    
    # --- do the binning ---
    
#     (run the binning function)
    
#     if qi_bins is None:
#         qi_bins = np.logspace(np.log10(1e-8), np.log10(5e-4), 50)  

#     if olr_bins is None:
#         if zoom:
#             olr_bins = np.arange(70, 90.5, 1)
#         else:
#             olr_bins = np.arange(70, 351, 5)
        
#     # offset levels: -2 to +2 above cold point
#     ind_offsets = [-2, -1, 0, 1, 2]
#     if model == "SCREAM" or model == "GEOS":
#         ind_offsets = [2*x for x in ind_offsets] # double bc grid spacing finer
        
#     offset_labs = ["~1000 m below", 
#                    "~500 m below", 
#                    "At cold point", 
#                    "~500 m above", 
#                    "~1000 m above"
#                   ]
        
#     # make an array with dimensions (level, OLR bin) & fill with mean var values
#     # for FWP, it's only one level
#     qi_bin_means = np.zeros((len(ind_offsets), len(olr_bins)-1))
#     w_bin_means = np.zeros((len(ind_offsets), len(olr_bins)-1))
#     qg_bin_means = np.zeros((len(ind_offsets), len(olr_bins)-1))
    
#     for i, offset in enumerate(ind_offsets):
#         if model == "SAM":
#             qi_lev, olr_nonan = da_to_nonans(qi.isel(z=cp_inds+offset)/1000., olr)
#             w_lev, olr_nonan_w = da_to_nonans(w.isel(z=cp_inds+offset)/1000., olr)
#         elif model == "NICAM":
#             qi_lev, olr_nonan = da_to_nonans(qi.isel(lev=cp_inds+offset).isel(time=slice(None, -1)), olr)
#             w_lev, olr_nonan_w = da_to_nonans(w.isel(lev=cp_inds+offset).isel(time=slice(None, -1)), olr)
#             qg_lev, olr_nonan_qg = da_to_nonans(qg.isel(lev=cp_inds+offset).isel(time=slice(None, -1)), olr)
#         elif model == "ICON":
#             qi_lev, olr_nonan = da_to_nonans(qi.isel(height=cp_inds+offset), olr)
#             w_lev, olr_nonan_w = da_to_nonans(w.isel(height=cp_inds+offset), olr)
#         elif model == "SCREAM":
#             qi_lev, olr_nonan = da_to_nonans(qi.isel(lev=cp_inds+offset), olr)
#             w_lev, olr_nonan_w = da_to_nonans(w.isel(lev=cp_inds+offset), olr)
#         elif model == "GEOS":
#             qi_lev, olr_nonan = da_to_nonans(qi.isel(lev=cp_inds+offset), olr)
#             w_lev, olr_nonan_w = da_to_nonans(w.isel(lev=cp_inds+offset), olr)
#             qg_lev, olr_nonan_qg = da_to_nonans(qg.isel(lev=cp_inds+offset), olr)
#         elif model == "SHIELD":
#             qi_lev, olr_nonan = da_to_nonans(qi.isel(pfull_ref=cp_inds+offset), olr)
#             w_lev, olr_nonan_w = da_to_nonans(w.isel(pfull_ref=cp_inds+offset), olr)
#             qg_lev, olr_nonan_qg = da_to_nonans(qg.isel(pfull_ref=cp_inds+offset), olr)

#         # qi and w
#         mean_qi, bin_edges, inds = binned_statistic(olr_nonan, qi_lev, statistic="mean", bins=olr_bins)
#         qi_bin_means[i, :] = mean_qi
#         mean_w, bin_edges_w, inds_w = binned_statistic(olr_nonan_w, w_lev, statistic="mean", bins=olr_bins)
#         w_bin_means[i, :] = mean_w
        
#         # only NICAM, GEOS, and SHIELD for graupel
#         if model == "NICAM" or model == "SHIELD" or model == "GEOS":
#             mean_qg, bin_edges_qg, inds_qg = binned_statistic(olr_nonan_qg, qg_lev, statistic="mean", bins=olr_bins)
#             qg_bin_means[i, :] = mean_qg
            
    
    
    # def plot_2d_binned_by_OLR(var2d, olr, model, region, var_bins, var_name, var_units,
#                           var_abbrev, olr_bins=None, cb_ticks=None, fsize=16,
#                           tsize=18, figsize=(13, 1), colormap="Spectral", zoom=False, 
#                           save=False):
#     """ Plot one 2d variable binned by OLR
#     """
#     if olr_bins is None:
#         olr_bins = np.arange(70, 351, 5)
        
#     # dummy level
#     level = np.zeros((1))
#     level_lab = ["Total column"]
        
#     # make an array with dimensions (level, OLR bin) & fill with mean variable value
#     var_bin_means = np.zeros((len(level), len(olr_bins)-1))

#     mean_var, bin_edges, inds = binned_statistic(olr.values.flatten(),
#                                                  var2d.values.flatten(),
#                                                  statistic="mean", 
#                                                  bins=olr_bins
#                                                 )
#     var_bin_means[0, :] = mean_var
        
#     # Plot!
#     fig, ax = plt.subplots(figsize=figsize)

#     # plot against avg of bin edges so the tick marks line up with the edges
#     bin_mean_olr = (olr_bins[:-1] + olr_bins[1:])/2
#     var_pcm = ax.pcolormesh(var_bin_means, cmap=colormap,
#                             norm=mcolors.LogNorm(vmin=var_bins[0],
#                                                  vmax=var_bins[-1])
#                            )

#     cbar = plt.colorbar(var_pcm, ax=ax, shrink=2, extend="both")

#     ax.set_xticks(np.arange(len(olr_bins))[::2])
#     ax.set_xticklabels([str(x) for x in olr_bins[::2]])
#     ax.set_xlabel("OLR (W/m$^2$)", fontsize=fsize)
#     ax.tick_params(axis="x", rotation=45, labelsize=fsize-2)

#     ax.set_yticks([0.5])
#     ax.set_yticklabels(level_lab)
#     ax.tick_params(axis="y", labelsize=fsize, length=0)

#     cbar.ax.tick_params(labelsize=fsize)
#     cbar.set_label("{v} ({u})".format(v=var_abbrev, u=var_units), fontsize=fsize)
#     if cb_ticks is not None:
#         cbar.set_ticks(cb_ticks)

#     plt.title("{m} ({r}): {v}".format(m=model, r=region, v=var_name.lower()),
#               fontsize=tsize
#              )

#     if save:
#         if zoom:
#             plt.savefig(save_dir + \
#                         "{m}_{v}_binned_by_OLR_zoomed_{r}.png".format(m=model,
#                                                                       r=region,
#                                                                       v=var_abbrev), 
#                         dpi=300, bbox_inches="tight"
#                        )
#         else:
#             plt.savefig(save_dir + "{m}_{v}_binned_by_OLR_{r}.png".format(m=model,
#                                                                           r=region,
#                                                                        v=var_abbrev), 
#                         dpi=300, bbox_inches="tight"
#                        )

#     plt.show()