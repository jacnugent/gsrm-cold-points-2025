"""
model_grid.py

Module containing functions specifically to process DYAMOND model data.

Created by Jacqueline Nugent on December 10, 2019.
Last Modified: July 7, 2022

Functions:
    create_ICON_height: create an altitude variable for ICON
    read_coords: create arrays of coordinates from csv files
    create_coords_dict: map cell number to a lat-lon coordinate
    make_dummy_grid: make a dummy latlon grid to interpolate data onto
    interpolate_grid: interpolate native model grids to regular 
                        lat-lon
"""
import numpy as np
from scipy.interpolate import griddata

def create_ICON_height(height_file, nlevs):
    """
    Read in ICON height files and the number of levels actually in the
    data to create an array for the ICON altitude.

    Args: 
        height_file (string), file path to the vertical file (e.g. vlevs.grb)
        nlevs (integer), number of levels actually in the vertical data 
        
    Returns:
        alt_m (list of floats), heights at each level in m (top-down)

    """
    hght = cdo.fldmean(input=height_file, returnXDataset=True).to_array()[1,::-1,0,0,0,0] 
    levn = cdo.fldmean(input=height_file, returnXDataset=True).to_array()[0,::-1,0,0,0,0].values
    cdo.cleanTempDir()
    
    # calculate total levels in data, how many to skip, and indices to start & stop
    totlevs = len(hght)
    nskip = totlevs-nlevs
    stop = int(levn[0]-nskip)

    # create altitude and vertical coordinate (level #) arrays
    alt_m = hght[0:stop]
    levels = levn[0:stop]
    
    # swap the order so it is ordered top-down
    alt_m = np.flip(alt_m)
    
    return alt_m


def read_coords(csvfile):
    """
    Read in a csv file containing grid cell coordinates and return arrays
    of the latitude and longitude. File must be a CSV file with comma
    delimiters.
    
    Args:
        csvfile (string): name of the csv file
    
    Returns:
        lat (1D array): array of latitudes
        lon (1D array): array of longitudes
    """
    coords = np.loadtxt(csvfile, delimiter=',')
    lat = coords[:, 0]
    lon = coords[:, 1]
    
    return [lat, lon]


def create_coords_dict(ncells, clat, clon, radians=False, to_180=False):
    """
    Create a dictionary mapping cell number to the corresponding latitude 
    and longitude coordinates.

    Args:
        ncells (int): the number of cells
        clat (1D array): model cell latitude coordinates
        clon (1D array): model cell longitude coordinates

    Returns:
        coords_dict (dictionary): the dictionary with integer cell numbers
            as keys and tuples of floats (lon, lat) for values.
    """
    # cell_coords = [(clon[i], clat[i]) for i in range(ncells)]
    if radians:
        clon_d = np.rad2deg(clon)
        if to_180:
            clon_d = (clon_d + 180) % 360 - 180
        clat_d = np.rad2deg(clat)
        cell_coords = np.array((clon_d, clat_d)).T
    else:
        cell_coords = np.array((clon, clat)).T
    cells = np.arange(0, ncells)
    cell_coords_dict = dict(zip(cells, cell_coords))

    return cell_coords_dict


def make_dummy_grid(data, lat_lims, lon_lims, coords_file=None, clat=None, clon=None, to_180=False):
    """
    Make a dummy grid to interpolate to from lat-lon limits and number of
    cells. Makes the highest-resolution grid possible. Prints how many
    grid points will be lost.
    
    ** NOTE: if you want to interpolate FV3 native grid variables to match the
    latlon variables (qi, qc, etc.), then this function is not necessary;
    grid_x and grid_y in the interpolation function below will be the latlon
    values of those points. **
    
    Args:
        data (DataArray): the variable to interpolate
        lat_lims (tuple of floats): (south/min latitude, north/max latitude)
        lon_lims (tuple of floats): (west/min longitude, east/max longitude) 
        coords_file (string, OPTIONAL): name of the csv file containing
            coordinates for each cell if not given in the data (e.g. for
            ICON); if not given, assumes that the data array has dims or
            variables 'lat' and 'lon' containing the cell coordinates (e.g.
            for FV3)
     
     Returns:
         grid_x (array of floats): longitude values of the dummy grid
             (-180 to 180 scale)
         grid_y (array of floats): latitude values of the dummy grid
    """
    ltmin, ltmax = lat_lims
    lnmin, lnmax = lon_lims
    
    # get the lat and lon of each grid cell
    if coords_file is not None:
        [clat, clon] = read_coords(coords_file)
    else: 
        if clat is None or clon is None: 
            if "lat" in data.coords:
                clat = data.lat.values
                clon = data.lon.values
            else:
                clat = data.lats.values
                clon = data.lons.values
    
    # convert from 0 to 360 to -180 to 180 if necessary
    if to_180:
        for i in range(len(clon)):
            if clon[i] > 180:
                clon[i] = clon[i] - 360
            
    # how many points lost?
    target_x_deg = lon_lims[1] - lon_lims[0]
    target_y_deg = lat_lims[1] - lat_lims[0]
    ncells = data.shape[-1]
    cells_per_deg = int(np.sqrt(ncells/(target_x_deg*target_y_deg)))
    grid_len_x = cells_per_deg*target_x_deg
    grid_len_y = cells_per_deg*target_y_deg
    nlost = ncells - (grid_len_x*grid_len_y)
    pctlost = nlost/ncells*100.
    print('{x} grid points ({p:.2f}%) will be lost from interpolation.'.format(x=nlost, p=pctlost))
    
    # make the dummy grid
    grid_y = np.linspace(ltmin, ltmax, grid_len_y)
    grid_x = np.linspace(lnmin, lnmax, grid_len_x)
    
    return [grid_x, grid_y]


def interpolate_grid(data, is3D, data_array=False, clat=None, clon=None,
                     grid_x=None, grid_y=None, latlims=None, lonlims=None,
                     coords_file=None, to_180=False, radians=False):
    """
    Interpolate the native model grid data (with spatial dimension ncells)
    onto a regular latitude-longitude grid. Use this with FV3 variables for
    spatial plots or vertical columns and with ICON variables for
    spatial plots only. Assumes ncells is the last dimension in the data 
    (e.g. (time, height, ncells)).
    
    If cell lon/lat and regular grid lon/lat are not provided, a dummy
    grid will be created. 
    
    ** nearest neighbors interpolation **

    Args:
        data (DataArray or numpy array): the variable to interpolate
        is3D (bool): True if data is 3D (i.e. height, time, & ncells)
        data_array (boolean): True if data is a DataArray; False (default)
                             if it is a numpy array

        Input these if you already have the grid:
        clat (1D array, OPTIONAL): model cell latitude coordinates
        clon (1D array, OPTIONAL): model cell longitude coodinates
        grid_x (1D array, OPTIONAL): regular grid latitude coordinates
        grid_y (1D array, OPTIONAL): regular grid longitude coordinates
        
        Input these if you need to make a dummy grid:
        latlims (tuple of floats): (south/min latitude, north/max latitude)
        lonlims (tuple of floats): (west/min longitude, east/max longitude) 
        coords_file (string, OPTIONAL): csv file containing cell coordinates;
                                       pass in if creating dummy grid for ICON
        to_180 (bool): True if you want to convert 0-360 to -180-180; False to 
                       leave coords as is (default)

    Returns:
        if data_array=True (i.e. you made a dummy grid):
            interp_data (numpy array): the interpolated variable
            grid_x (numpy array): longitude values of the dummy grid
            grid_y (numpy array): latitude values of the dummy grid
        else:
            interp_data (numpy array): the interpolated variable 

    """
    shape = np.shape(data)
    
    # if you need to make a dummy grid and get cell coordinates first:
    if clat is None or clon is None or grid_x is None or grid_y is None:
        if not data_array:
            raise Exception('Data must be a DataArray if coordinate info is not given')
        
        print('Creating dummy grid...')
        grid_x, grid_y = make_dummy_grid(data, latlims, lonlims, coords_file, clat, clon, to_180)
        print('Dummy grid done.')
        
        if coords_file is not None:
            [clat, clon] = read_coords(coords_file)
        else: 
            if clat is None or clon is None: 
                if "lat" in data.coords:
                    clat = data.lat.values
                    clon = data.lon.values
                else:
                    clat = data.lats.values
                    clon = data.lons.values
    
    
    coords_dict = create_coords_dict(shape[-1], clat, clon, radians, to_180)
    coords = [v for k, v in coords_dict.items()]
    X, Y = np.meshgrid(grid_x, grid_y)

    
    # NOTE: previous function used coords_dict.values() in the for-loop
    # instead of coords... change that back if you have trouble while using
    # python 2 and/or regular numpy arrays
    
    if data_array:
        data_vals = data.values
    else:
        data_vals = data
        
    print('Interpolating data...')
    # 3D variables:
    if is3D:
        interp_data = np.empty((shape[0], shape[1], len(grid_x), len(grid_y)))
        for i in range(np.shape(data_vals)[0]):
            for j in range(np.shape(data_vals)[1]):
                interp_data[i, j, :, :] = griddata(coords,
                                                   data_vals[i, j, :], (X, Y),
                                                   method='nearest')
    # 1D & 2D variables:
    else:
        # 1D (no time, only cells)
        if len(shape) == 1:
            interp_data = np.empty((len(grid_x), len(grid_y)))
            interp_data = griddata(coords, data_vals, (X, Y), 
                                   method='nearest') 
        # 2D (time, cell)
        else:
            interp_data = np.empty((shape[0], len(grid_x), len(grid_y)))
            for i in range(np.shape(data_vals)[0]):
                interp_data[i, :, :] = griddata(coords, data_vals[i, :],
                                                (X, Y), method='nearest')

    print('Interpolation done.')
    
    if data_array:
        return interp_data, grid_x, grid_y
    else:
        return interp_data
    
