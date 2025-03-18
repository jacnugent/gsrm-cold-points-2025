#!/usr/bin/env python

# get info from here to make changes to the request: https://apps.ecmwf.int/data-catalogues/era5/?class=ea

import cdsapi

c = cdsapi.Client()

# temperature = param 130
# geopotential = param 129

# 49-78 is ~12-20 km
c.retrieve('reanalysis-era5-complete', {
    'class': 'ea',
    'date': '2020-02-01/to/2020-02-29',
    'expver': '1',
    'levelist': '49/50/51/52/53/54/55/56/57/58/59/60/61/62/63/64/65/66/67/68/69/70/71/72/73/74/75/76/77/78',
    'levtype': 'ml',
    'param': '130',
    'stream': 'oper',
    'time': '00:00:00/01:00:00/02:00:00/03:00:00/04:00:00/05:00:00/06:00:00/07:00:00/08:00:00/09:00:00/10:00:00/11:00:00/12:00:00/13:00:00/14:00:00/15:00:00/16:00:00/17:00:00/18:00:00/19:00:00/20:00:00/21:00:00/22:00:00/23:00:00',
    'type': 'an',
    'format': 'netcdf',
    'grid': '0.25/0.25',
    'area': [
        10, -180, -30, 180, # North West South East
    ],
}, '/home/disk/eos15/jnug/ERA5_ml/ERA5_temp_0.25deg_ml_12-20km_Feb2020_ITCZ.nc')
