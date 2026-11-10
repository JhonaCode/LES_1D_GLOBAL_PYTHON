# python library to work with netcdf4 
#from    netcdf4         import dataset

# to save the time coordinate in specific format 
from    netCDF4         import num2date, date2num

# Python standard library datetime  module
import datetime as dt  

import xarray as xr

# To save the time coordinate in specific format 
from    cftime import num2date, num2pydate

import pandas as pd

import  scam.forcing_file_common as ffc

import numpy as np

def data_load_xr(path,name,UTC):

    exp            =  xr.open_dataset(path, engine='netcdf4')

    # To remove the column, that have lenght 1
    exp         = exp.squeeze()

    exp['name']    =  name

    #exp['BR']   =  exp['SHF']/exp['LHF']

    #exp['netsf']   =  exp['SWNS']-exp['LWNS']
    #exp['netsf_dw']=  exp['SWDS']-exp['LWDS']

    ltime = exp.time + dt.timedelta(hours=UTC)

    exp['ltime']   =  exp.time 

    exp['time']    =  ltime 

    #print("area:", exp['area'].values)
    #print("areawt:", exp['areawt'].values)
    #print("area attributes:", exp['area'].attrs)

    #print(exp['PRECC'].units)
    #m/s
    #exit()

    #m/s
    exp['PRECT']   = (exp['PRECC'] + exp['PRECL']) * 3600 * 1000  
    exp.PRECT.attrs['units']='mm/hr'

    exp.PRECT.attrs['long_name'] = 'Total precipitation rate'


    #Calculated the pressure levels from 
    #the hybrid sigma-pressure vertical coordinate  
    #P0 = 100000.0  # Pa
    #pressure = (
    #    exp["hyam"] * P0
    #    + exp["hybm"] * exp["PS"]
    #) / 100.0      # hPa    
    #print(exp.lev[0:10])
    #print(pressure[0:10])
    #It is not necessary, lev variable is it!!!
    #exit()

    #date_format = '%Y%m%d%H'
    ##to add the minutes to the original date
    #dis=date[0]#+'00'
    #dfs=date[1]#+'00'
    #di=dt.datetime.strptime(dis, date_format)
    #df=dt.datetime.strptime(dfs, date_format)

    ##initial hour
    #hi=di.hour
    ##final hour
    #hf=df.hour
    #time=exp.time.values

    #does not change the time 
    #exp['time']=exp.ltime.values
    #exp['ltime']=time
    #exp['ltime']==exp.ltime.values

    #exp['ltime']=exp.ltime.values

    T=exp.T

    Lev=exp.lev[::-1]

    #
    z_sfc=0.0

    #calculate for each time 
    #z=ffc.get_height_from_pres_temporal(T[::-1], Lev, z_sfc)
    #exp['z']= (("time","lev"),z)

    #make a mean and calculated unique z, the problem
    # it is that the surface pressure varies with time
    # but this difference is small. 
    z=ffc.get_height_from_pres(T.mean(dim='time'), Lev, z_sfc)
    exp['z']= (("lev"),z)


    return exp 

def data_n(idi,idf,data): 

    #indices achados
    ni=0
    nf=0

    #banderas 
    b1=0
    b2=0

    for i in range(0,data.shape[0]-1):


        if data[i]>=idi and b1==0: 
            ni =i  
            b1 =1
            #print("From:")
            #print("Data1:", data[i],i)

        if data[i]>=idf and b2==0:  
            nf =i  
            b2 =1
            #print("To:")
            #print("Data2:", data[i],i) 
    if nf==0:

        nf=data.shape[0]-1

    return ni,nf

def level_n(idi,idf,data): 

    #indices achados
    ni=0
    nf=0

    #banderas 
    b1=0
    b2=0

    for i in range(0,data.shape[0]-1):

        if data[i]>=idi and b1==0: 
            ni =i  
            b1 =1
            print("Level1:", data[i]) 

        if data[i]>=idf and b2==0:  
            nf =i  
            b2 =1
            print("Level2:", data[i]) 

    # To found the maximum date, even 
    # that required date not exists
    if nf==0:

        nf=data.shape[0]-1

    return ni,nf

def pressure_n(idi,idf,data,exp): 

    #indices achados
    ni=0
    nf=0

    #banderas 
    b1=0
    b2=0


    for i in range(0,data.shape[0]-1):

        if(data[i]<=idi and b1==0): 
            #print(data[i],idi,b1)
            ni =i  
            b1 =1
            #print("Level1:", data[i],idi,exp.z[i]) 

        if data[i]<=idf and b2==0:  
            #print(data[i],idf)
            nf =i  
            b2 =1
            #print("Level2:", data[i],exp.z[i]) 
    return ni,nf

def data_to_reference(date,date0): 

    try:
        month   =   date.dt.month
        day     =   date.dt.day
        hour    =   date.dt.hour 
        minute  =   date.dt.minute 
        second  =   date.dt.second 
        micro   =   date.dt.microsecond

    except:
        month   =   date.month
        day     =   date.day
        hour    =   date.hour 
        minute  =   date.minute 
        second  =   date.second 
        micro   =   date.microsecond

    data_ref =   dt.datetime( date0[2],date0[1],day,hour,minute, second,micro)

    return data_ref#,day.values 

def data_to_reference_vector(data,date0,lim,plotdef):

    i=0

    #to change the month, if 0 does change
    day_ant=-1
    month_ant=-1

    date0_ref=date0.copy()
    data_ref=[]
    dr=0

    lim1=-2
    lim2=-2
    plotd=-2

    for d in data:

        
        month   =   int(d.dt.month)
        day     =   int(d.dt.day)
        hour    =   int(d.dt.hour)
        minute  =   int(d.dt.minute)
        second  =   int(d.dt.second)
        micro   =   int(d.dt.microsecond)


        if day==day_ant+1:
            date0_ref[0]+=1
        if month==month_ant+1:
            date0_ref[0]+=1

        if (date0_ref[0])>31:

            date0_ref[1]+=1
            date0_ref[0]=1
            day_ant=1

        #print('x',day,date0_ref[0],date0_ref[1],)


        dr = dt.datetime( date0_ref[2],date0_ref[1],date0_ref[0],hour,minute, second,micro)

        #"""
        date_format = '%Y-%m-%dT%H:%M'
        l1=dt.datetime.strptime(lim[0], date_format)
        l2=dt.datetime.strptime(lim[1], date_format)

        #plot_def=dt.datetime.strptime(plotdef, date_format)

        if dr==l1:
            lim1=i

        if dr==l2:
            lim2=i

        data_ref.append(dr)

        day_ant = day
        month_ant = month

        i+=1

    return data_ref,[lim1,lim2]

