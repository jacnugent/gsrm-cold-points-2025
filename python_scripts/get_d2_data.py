"""
get_d2_data.py

Script to read in DYAMOND2 data for the 
10x10 regions and full ITCZ (30S-10N) region.

Also includes a function to interpolate a cell dim
variable to a 2d lat/lon file.

* cpT
* Tb
* qtot (ice + snow + graupel)
* diffs (Tb-cpT)
* os frequencies/counts

"""
import sys
sys.path.append("/home/b/b380887/cold-point-overshoot/python_scripts")
import xarray as xr
import numpy as np
import model_grid as mg
from dask.diagnostics import ProgressBar

# start/end date for the files (drop spinup)
START_DATE = "2020-01-30"
END_DATE = "2020-02-28"

# minimum qi (kg/kg)
QI_MIN = 1e-6

# minimum IWC (kg/m3) for DARDAR
DAR_MIN = 1e-7

# Based on SHIELD median cold point/pressure levels...
REF_DENSITIES = [
    0.180602, # -1000 m
    0.164667, # -500 m
    0.151853, # at cold point
    0.136337, # +500 m
    0.122172  # +1000 m
]


def calc_Tb(OLR):
    """ Calculate brightness temp from OLR
    """
    sigma = 5.670374419e-8
    Tb = (OLR/sigma)**0.25
    
    return Tb


def get_cold_point_itcz(model, file_path, remapped=True, return_inds=False,
                        start_date=START_DATE, end_date=END_DATE):
    """ 
    Get the cold point file (remapped/default or 0.25deg) for the whole
    30S-10N region.
    """
    if not remapped:
        cpT = xr.open_dataset(file_path + "local_cold_points/{m}_cpT_0.25deg_ITCZ.nc".format(m=model))["ta"]
    else:
        cpT = xr.open_dataset(file_path + "local_cold_points/{m}_cpT_remapped_ITCZ.nc".format(m=model))["ta"]
        
    return cpT

    
def get_cold_point(region, model, file_path, return_inds=False,
                   start_date=START_DATE, end_date=END_DATE):
    """ 
    Get the cold point (3 hourly, native grid) 
    for that region/model
    """
    if model == "SCREAM":
        temp = xr.open_dataset(file_path + "{r}/{m}_temp_025_remapped_{r}.nc".format(r=region, m=model))["ta"].sel(time=slice(start_date, end_date))
        temp = temp.reindex(lev=temp.lev[::-1]).isel(lev=slice(None, -5))
        cp_inds = temp.argmin(dim="lev")
        cpT = temp.isel(lev=cp_inds)
        
    elif model == "SHIELD":
        temp = xr.open_dataset(file_path + "{r}/{m}_temp_025_remapped_{r}.nc".format(r=region, m=model))["ta"].sel(time=slice(start_date, end_date))
        temp = temp.reindex(pfull_ref=temp.pfull_ref[::-1]).isel(pfull_ref=slice(None, -3))
        cp_inds = temp.argmin(dim="pfull_ref")
        cpT = temp.isel(pfull_ref=cp_inds)
        
    elif model == "GEOS":
        temp = xr.open_dataset(file_path + "{r}/{m}_temp_025_remapped_{r}.nc".format(r=region, m=model))["ta"].sel(time=slice(start_date, end_date))
        temp = temp.reindex(lev=temp.lev[::-1]).isel(lev=slice(None, -5)) 
        cp_inds = temp.argmin(dim="lev")
        cpT = temp.isel(lev=cp_inds)
        
    elif model == "ICON":
        temp = xr.open_dataset(file_path + "{r}/{m}_temp_025_remapped_{r}.nc".format(r=region, m=model))["ta"].sel(time=slice(start_date, end_date))
        temp = temp.reindex(height=temp.height[::-1]).isel(height=slice(None, -3))
        cp_inds = temp.argmin(dim="height")
        cpT = temp.isel(height=cp_inds)
        
    elif model == "SAM":
        temp = xr.open_dataset(file_path + "{r}/{m}_temp_0.25deg_12-20km_winter_{r}.nc".format(r=region, m=model))["ta"].sel(time=slice(start_date, end_date))
        temp = temp.isel(z=slice(None, -3)) 
        qi = xr.open_dataset(file_path + "{r}/{m}_qi_12-20km_winter_{r}.nc".format(r=region, m=model))["cli"].sel(time=slice(start_date, end_date))
        temp_ri = temp.reindex_like(qi, method="nearest")
        cp_inds = temp_ri.argmin(dim="z")
        cpT = temp_ri.isel(z=cp_inds)
        
    if return_inds:
        return cpT, cp_inds
    else:
        return cpT


def get_brightness_temp_itcz(model, file_path,
                        start_date=START_DATE, end_date=END_DATE):
    """ 
    Get the brightness temperature (3 hourly, native grid)
    for that model in the 30S-10N region.
    """
    tb = xr.open_dataset(file_path + "tb_3hourly/{m}_tb_3hrly_ITCZ.nc".format(m=model))["Tb"]
    return tb
    
    
def get_brightness_temp(region, model, file_path,
                        start_date=START_DATE, end_date=END_DATE):
    """ 
    Get the brightness temperature (3 hourly, native grid)
    for that model/region. 
    """
    if model == "SCREAM" or model == "ICON" or model == "SAM":
        varname = "rlt"
    elif model == "SHIELD" or model == "GEOS":
        varname = "rlut"

    olr = xr.open_dataset(file_path + "{r}/{m}_OLR_winter_{r}.nc".format(r=region, m=model))[varname].sel(time=slice(start_date, end_date))
    olr_3h = olr.resample({"time": "3H"}).nearest()
    
    # rename xdim for SCREAM to match 3d vars
    if model == "SCREAM":
        olr_3h = olr_3h.rename({"grid_size": "ncol"})
    
    tb = calc_Tb(olr_3h)
    
    return tb


def get_diffs(model, file_path):
    """ Get the tb-cpT file for the 30S-10N region
    """
    diffs = xr.open_dataset(file_path + "diffs/{m}_tb-cpT_ITCZ.nc".format(m=model))["Tb"]
    return diffs


def get_os(model, file_path):
    """ Get the os frequency & count file for the 30S-10N region
    """
    os = xr.open_dataset(file_path + "os_frequencies/{m}_os_freq_count.nc".format(m=model))
    return os


def get_ci(model, file_path, layer):
    """ 
    Get the rad active cirrus count file for the 30S-10N region.
    Layer is "above" (zcp to +1000m), "below" (-1000m to zcp), or
    "at" (-500m to +500m); throws exepction if something else given.
    """
    if layer == "above": 
        layer_ext = "0_to_a1000"
    elif layer == "at": 
        layer_ext = "b500_to_a500"
    elif layer == "below":
        layer_ext = "b1000_to_0"
    elif layer == "at_zcp":
        layer_ext = layer
    else:
        raise Exception("Input `layer` must be \"above\" (zcp to +1000m), \"below\" (-1000m to zcp), or \"at\" (-500m to +500m) OR \"at_zcp\" (zcp)")
        
    try:
        ci = xr.open_dataset(file_path + "cirrus_frequencies/{m}_cp_cirrus_counts_{e}.nc".format(m=model, e=layer_ext))
    except:
        ci = xr.open_dataset(file_path + "{m}_cp_cirrus_counts_{e}.nc".format(m=model, e=layer_ext))
    
    return ci


def get_qtot(region, model, file_path, qi_min=QI_MIN, dar_min=DAR_MIN,
             chunks={"time": 8}, obs_year_list=[2007, 2008, 2009, 2010],
             start_date=START_DATE, end_date=END_DATE, obs_cp_relative=False):
    """ 
    Get the total frozen water (qi+qs+qg) (3 hourly, native grid)
    for that model/region. Switches to vertical levels are bottom-up.
    """
    if model == "SCREAM": 
        qtot = xr.open_dataset(file_path + "{r}/{m}_qi_12-20km_winter_{r}.nc".format(r=region, m=model))["cli"].sel(time=slice(start_date, end_date))
        qtot_nz = qtot.reindex(lev=qtot.lev[::-1]).where(qtot > qi_min)
        
    elif model == "SHIELD" or model == "GEOS": 
        qi = xr.open_dataset(file_path + "{r}/{m}_qi_12-20km_winter_{r}.nc".format(r=region, m=model), chunks=chunks)["cli"].sel(time=slice(start_date, end_date))
        qs = xr.open_dataset(file_path + "{r}/{m}_qs_12-20km_winter_{r}.nc".format(r=region, m=model), chunks=chunks)["snowmxrat"].sel(time=slice(start_date, end_date))
        qg = xr.open_dataset(file_path + "{r}/{m}_qg_12-20km_winter_{r}.nc".format(r=region, m=model), chunks=chunks)["grplmxrat"].sel(time=slice(start_date, end_date))
        qtot_chunked = qi + qs + qg
        with ProgressBar():
            qtot = qtot_chunked.compute()
        if model == "SHIELD":
            qtot_nz = qtot.reindex(pfull_ref=qtot.pfull_ref[::-1]).where(qtot > qi_min)
        elif model == "GEOS":
            qtot_nz = qtot.reindex(lev=qtot.lev[::-1]).where(qtot > qi_min)
        
    elif model == "SAM" or model == "ICON": 
        print("**ice only** - no snow or graupel for", model)
        if model == "SAM":
            qtot = xr.open_dataset(file_path + "{r}/{m}_qi_12-20km_winter_{r}.nc".format(r=region, m=model))["cli"].sel(time=slice(start_date, end_date))
            qtot_nz = qtot.where(qtot > qi_min)
        elif model == "ICON":
            qtot = xr.open_dataset(file_path + "{r}/{m}_qi_12-20km_winter_{r}.nc".format(r=region, m=model))["cli"].sel(time=slice(start_date, end_date))
            qtot_nz = qtot.reindex(height=qtot.height[::-1]).where(qtot > qi_min)
            
    elif model == "OBS":
        print("*** returning DARDAR IWC, not mixing ratio ***")
        dar_years = [[]]*len(obs_year_list)
        for i, year in enumerate(obs_year_list):
            if obs_cp_relative:
                dar_years[i] = xr.open_dataset(file_path + "{r}/DARDAR_cp_relative_iwc_DJF{y}_{r}.nc".format(r=region, y=year))
            else:
                dar_years[i] = xr.open_dataset(file_path + "{r}/DARDAR-v3_iwc_DJF{y}_{r}.nc".format(r=region, y=year))
        qtot = xr.concat(dar_years, dim="time")
        qtot_nz = qtot.where(qtot > dar_min)
        
    return qtot_nz


def get_qsg(region, model, file_path, qi_min=QI_MIN, chunks={"time": 8},
             start_date=START_DATE, end_date=END_DATE):
    """ 
    Get the snow+graupel (3 hourly, native grid)
    for that model/region. Switches to vertical levels are bottom-up.
    """
    if model == "SCREAM": 
        raise Exception("No separate hydrometeors for ", model)
        
    elif model == "SHIELD" or model == "GEOS": 
        qs = xr.open_dataset(file_path + "{r}/{m}_qs_12-20km_winter_{r}.nc".format(r=region, m=model), chunks=chunks)["snowmxrat"].sel(time=slice(start_date, end_date))
        qg = xr.open_dataset(file_path + "{r}/{m}_qg_12-20km_winter_{r}.nc".format(r=region, m=model), chunks=chunks)["grplmxrat"].sel(time=slice(start_date, end_date))
        qsg_chunked = qs + qg
        with ProgressBar():
            qsg = qsg_chunked.compute()
        if model == "SHIELD":
            qsg_nz = qsg.reindex(pfull_ref=qsg.pfull_ref[::-1]).where(qsg > qi_min)
        elif model == "GEOS":
            qsg_nz = qsg.reindex(lev=qsg.lev[::-1]).where(qsg > qi_min)
        
    elif model == "SAM" or model == "ICON": 
        raise Exception("No snow or graupel for ", model)
            
    return qsg_nz


def get_qi(region, model, file_path, qi_min=QI_MIN, 
             start_date=START_DATE, end_date=END_DATE, no_nz=False):
    """ 
    Get the ice (qi) only (3 hourly, native grid)
    for that model/region. Switches to vertical levels are bottom-up.
    """
    if region != "ITCZ":
        file_path += "{r}/".format(r=region)
        
    if model == "SCREAM": 
        raise Exception("No separate hydrometeors for ", model)
        
    elif model == "SHIELD" or model == "GEOS": 
        qi = xr.open_dataset(file_path + "{m}_qi_12-20km_winter_{r}.nc".format(r=region, m=model))["cli"].sel(time=slice(start_date, end_date))
        if model == "SHIELD":
            if no_nz:
                qi_nz = qi # fake it
            else:
                qi_nz = qi.reindex(pfull_ref=qi.pfull_ref[::-1]).where(qi > qi_min)
        elif model == "GEOS":
            if no_nz:
                qi_nz = qi # fake it
            else:
                qi_nz = qi.reindex(lev=qi.lev[::-1]).where(qi > qi_min)
        
    elif model == "SAM" or model == "ICON": 
        if model == "SAM":
            qi = xr.open_dataset(file_path + "{m}_qi_12-20km_winter_{r}.nc".format(r=region, m=model))["cli"].sel(time=slice(start_date, end_date))/1000. # g/kg --> kg/kg
            if no_nz:
                qi_nz = qi # fake it
            else:
                qi_nz = qi.where(qi > qi_min)
        elif model == "ICON":
            qi = xr.open_dataset(file_path + "{m}_qi_12-20km_winter_{r}.nc".format(r=region, m=model))["cli"].sel(time=slice(start_date, end_date))
            if no_nz:
                qi_nz = qi # fake it
            else:
                qi_nz = qi.reindex(height=qi.height[::-1]).where(qi > qi_min)
            
    return qi_nz


def get_cp_relative_dardar(region, months, file_path, year_list, qi_min=QI_MIN, 
                           ref_densities=REF_DENSITIES, drop_extra=True, unique_times=False):
    """ 
    Get DARDAR IWC for all year(s) in `year_list` at 
    cold point-relative levels and convert to qi. Returns dataset with qi > qi_min for all retrievals where each relative level is a variable.
    Drops extra variables (level heights, levels, longitude, latitude) if drop_extra=True.
    Drops duplicate time values (<5% for 2007-2010) if unique_times=True.
    """
    var_list = ["iwc_b1000", "iwc_b500", "iwc_cp", "iwc_a500", "iwc_a1000"]
    dar_list = [[]]*len(year_list)
    
    for i, year in enumerate(year_list):
        iwc = xr.open_dataset(file_path + "DARDAR_cp_relative_iwc_{m}{y}_{r}.nc".format(m=months, r=region, y=year))[var_list]
        print("DIVIDING by reference density to go from kg/m3 to kg/kg")
        iwc["iwc_b1000"] = iwc["iwc_b1000"]/ref_densities[0]
        iwc["iwc_b500"] = iwc["iwc_b500"]/ref_densities[1]
        iwc["iwc_cp"] = iwc["iwc_cp"]/ref_densities[2]
        iwc["iwc_a500"] = iwc["iwc_a500"]/ref_densities[3]
        iwc["iwc_a1000"] = iwc["iwc_a1000"]/ref_densities[4]
        for variable in var_list:
            iwc[variable].attrs["units"] = "kg/kg"
            iwc[variable].attrs["long_name"] = "Calculated ice mixing ratio"
        qi = iwc.rename({"iwc_b1000": "qi_b1000",
                         "iwc_b500": "qi_b500",
                         "iwc_cp": "qi_cp",
                         "iwc_a500": "qi_a500",
                         "iwc_a1000": "qi_a1000"})
        dar_list[i] = qi
    dar_all = xr.concat(dar_list, dim="time")
    
    if drop_extra:
        drop_list = ["level", "height_b1000", "height_b500", "height_cp", 
                     "height_a500", "height_a1000", "longitude", "latitude"]
        dar_all = dar_all.drop(drop_list)
    if unique_times:
        time_inds = np.arange(0, len(dar_all.time))
        _, unique_inds = np.unique(dar_all['time'], return_index=True)
        dar_all = dar_all.isel(time=unique_inds)
        
    if qi_min is None:
        dar = dar_all
    else:
        dar = dar_all.where(dar_all > qi_min)
    
    return dar  
    

def interp_var2d(var2d, model, pickle_dir, coords=[0, 360, -30, 10], region="ITCZ", has_cell_coords=True):
    """
    Interp cell var (no time dim) onto lat/lon
    """
    if model == "GEOS":
        print("Interpolating GEOS")
        if has_cell_coords:
            clat = var2d.lats
            clon = var2d.lons
        else:
            qi = get_qi("ITCZ", "GEOS", "/work/bb1153/b380887/global_tropics/GEOS/", no_nz=True)
            clat = qi.lats
            clon = qi.lons
        var_interp_vals = mg.interpolate_grid(var2d, is3D=False, data_array=True,
                                              clat=clat, clon=clon,
                                              latlims=coords[2:], lonlims=coords[:2],
                                              to_180=False)
        var2d_interp = xr.DataArray(var_interp_vals[0], dims=["lat", "lon"],
                                    coords={"lon": var_interp_vals[1], "lat": var_interp_vals[2]}) 

    elif model == "ICON":
        print("Interpolating ICON")
        if has_cell_coords:
            clat = var2d.clat.values
            clon = var2d.clon.values
        else:
            qi = get_qi("ITCZ", "ICON", "/work/bb1153/b380887/global_tropics/ICON/", no_nz=True)
            clat = qi.clat.values
            clon = qi.clon.values
        lonlims = coords[:2]
        var_interp_vals = mg.interpolate_grid(var2d, is3D=False, data_array=True,
                                                clat=clat, 
                                              clon=clon,
                                                latlims=coords[2:], lonlims=(-180, 180),
                                                to_180=True, radians=True) 
        var2d_interp = xr.DataArray(var_interp_vals[0], dims=["lat", "lon"],
                                    coords={"lon": var_interp_vals[1], "lat": var_interp_vals[2]}) 

    elif model == "SCREAM":
        print("Interpolating SCREAM")
        itcz_coords_file = pickle_dir + "coord_csvs/SCREAM_coords_ITCZ.csv"
        var_interp_vals = mg.interpolate_grid(var2d, is3D=False, data_array=True,
                                              coords_file=itcz_coords_file, 
                                              latlims=coords[2:],
                                              lonlims=coords[:2], to_180=False)
        var2d_interp = xr.DataArray(var_interp_vals[0], dims=["lat", "lon"],
                                    coords={"lon": var_interp_vals[1], "lat": var_interp_vals[2]})

    elif model.upper() == "SHIELD":
        print("Interpolating SHIELD")
        if has_cell_coords:
            clat = var2d.lat
            clon = var2d.lon
        else:
            qi = get_qi("ITCZ", model, "/work/bb1153/b380887/global_tropics/SHiELD/", no_nz=True)
            clat = qi.lat
            clon = qi.lon
        var_interp_vals = mg.interpolate_grid(var2d, is3D=False, data_array=True,
                                              clat=clat, clon=clon,
                                              latlims=coords[2:], lonlims=coords[:2],
                                              to_180=False, radians=True, 
                                             )
        var2d_interp = xr.DataArray(var_interp_vals[0], dims=["lat", "lon"],
                                    coords={"lon": var_interp_vals[1], "lat": var_interp_vals[2]}) 
    
    elif model == "SAM":
        print("SAM already has lat/lon coordinates; no interpolation needed")
        var2d_interp = var2d
        
    elif model == "OBS":
        print("OBS already has lat/lon coordinates; no interpolation needed")
        var2d_interp = var2d

    return var2d_interp
