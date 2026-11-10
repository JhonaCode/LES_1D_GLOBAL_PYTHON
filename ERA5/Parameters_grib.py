#!/usr/bin/python
# -*- coding: UTF-8 -*-

#################################
#PYTHON CODE TO PLOT DIFFERENS 
#MPAS DATA USING CARTOPY AND XARRAY. 
#################################
#PYTHON CODE TO PLOT DIFFERENS 
# Data:01/11/23
#################################
# By: Jhonatan A. A Manco
#################################

# Function to load the ncfiles
import xarray as xr


#pip install ecmwflibs
#pip install cfgrib 

import cfgrib

import  os,sys


#Path to the files 
path1='/oper/dados/ioper/tempo/NCEP/input/2024/06/01/00/'

file1=path1+'rtgssthr_grb_0.083.grib2.20240601'
file2=path1+'rtgssthr_grb_0.5.grib2.20240601'

# Out figure folder
out_fig='/dados/bamc/jhonatan.aguirre/git_repositories/ERA5_python/fig'

#out python nc files
out_files= path1+'/python_nc'

#file1=cfgrib.open_dataset('%s'%(file1), engine='cfgrib')
#file2=cfgrib.open_dataset('%s'%(file2), engine='cfgrib')
file1=xr.open_dataset('%s'%(file1), engine='cfgrib')
file2=xr.open_dataset('%s'%(file2), engine='cfgrib')


#TO see the variables
print(file1.variables)
print('xxxxxxxxxxxxxxx')
print(file2.variables)
#print(file1.variables)
#[print(i) for i in m15.data_vars]
#print(list(m15.keys()))
#exit()
#print(ds.time)
#print(ncdatas)

#exit()

