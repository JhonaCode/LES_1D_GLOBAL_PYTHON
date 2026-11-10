import numpy as np
import xarray as xr
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import   sources.cartopyplot   as ma 

import importlib

import subprocess, sys
# Function with the definition of differents projetions


#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/sam_python/', shell = True, executable="/bin/bash")

#used the user parameter to plot(plotparameter.py) if para:
#pars=__import__('source.Parameters_default',globals())
pars=importlib.import_module('.Parameters_default','sam_python',)

date_format = '%Y%m%d%H%M'


def accomulate(exp,variables,dates=None,lats=None,lons=None,lim=None,var2=None,show=None,step_era5=False): 

    di=dt.datetime.strptime(dates[0], date_format)
    df=dt.datetime.strptime(dates[1], date_format)


    if dates==None:
        dates=[]

    if lats==None:
        lats=[]

    if lons==None:
        lons=[]


    k=0
    accomulate=[]#np.zeros(len(exp))
    for ex in exp:

        j=0
        for var in variables[k]:

            toacomm = ex


            if dates:
                toacomm = toacomm.sel(time=slice(di,df))

            try:
                toacomm.latitude
            except:
                toacomm=ma.latitude_lat(toacomm)

            if lats:
                toacomm = toacomm.sel(latitude=slice(lats[0],lats[1]))

            try:
                toacomm.longitude
            except:
                toacomm=ma.longitude_lon(toacomm)

            if lons:

                toacomm = toacomm.sel(longitude=slice(lons[0],lons[1]))


            name    =   str(ex.name.values)+'_'+var
            print("__%s__"%(name))


            i=0
            accom=0
            for d in toacomm.time: 

                accom = toacomm[var][i]+accom

                i+=1

            #print(var2[k][j],k,j,'x')
            accom=accom*var2[k][j]


            j+=1

            accomulate.append(accom)
        k+=1

    return accomulate

def mean(exp,variables,dates=None,lats=None,lons=None,lim=None,var2=None,show=None,step_era5=False): 

    di=dt.datetime.strptime(dates[0], date_format)
    df=dt.datetime.strptime(dates[1], date_format)

    if dates==None:
        dates=[]

    if lats==None:
        lats=[]

    if lons==None:
        lons=[]


    k=0
    mean=[]
    for ex in exp:

        j=0
        for var in variables[k]:

            toacomm = ex

            if dates:
                toacomm = toacomm.sel(time=slice(di,df))

            try:
                toacomm.latitude
            except:
                toacomm=ma.latitude_lat(toacomm)

            if lats:
                toacomm = toacomm.sel(latitude=slice(lats[0],lats[1]))

            try:
                toacomm.longitude
            except:
                toacomm=ma.longitude_lon(toacomm)

            if lons:

                toacomm = toacomm.sel(longitude=slice(lons[0],lons[1]))

            name    =   str(ex.name.values)+'_'+var
            print("__%s__"%(name))

            mean_1  = toacomm[var].mean(axis=0)

            j+=1

        mean.append(mean_1)

        k+=1

    return mean


def statist(data,dates):

    ###nh  = [i for i in range(hi,hf,hour_step)]
    ###hours = [f'{int(h):0>2}' for h in nh]
    #data[var] for var in data.variables
    #variables=['qv_isobaric']

    variables=['cldfrac_isobaric']
    var=[]
    k=0

    fig = plt.figure()
    ax  = plt.axes()
    plt.gca().invert_yaxis() 

    for d in dates: 

        print(d)

        tomean = data.sel(Time=[d],method='nearest')
        for var in variables:

            lat  = tomean[var].mean(dim='latitude') 
            lon  = lat.mean(dim='longitude') 
            loni = lon[0,::-1]
            levi = data.level[::-1]
            plt.plot(loni, levi, label=lon.Time[0].dt.hour.values)
            ax.legend()


    plt.show()
    exit()

    #   meanlat= tomean['qv_isobaric'].mean(dim='latitude')
    #    mean= mean.assign_coords(time = dd)
    #    mean= mean.expand_dims(dim="time")


def mean_hours_xr(data,name,day):

    """
    data=data to mean 
    day =day of the new metric in a reference time.
    """

    hour =[0,4,8,12,16,20]
    hours=['00','04','08','12','16','20',]

    var=[]

    k=0
    for j in hour: 

        time='%sT%s:00'%(day,hours[k])
        dd = dt.datetime.strptime(time,"%Y-%m-%dT%H:%M")
        dd = pd.to_datetime(dd) 

        tomean=data.sel(time=data.time.dt.hour.isin([j]),method='nearest')
        mean= tomean.mean(dim='time')
        mean= mean.assign_coords(time = dd)
        mean= mean.expand_dims(dim="time")

        #print(mean)
        #exit()
        ##if k==0:
        ##    #print(data.time.dt.hour.isin([j]))
        ##    var=mean
        ##else:
        ###    #var.append(mean)
        ###    #var.concatenate(mean)
        ###    xr.concat(var,mean)

        var.append(mean)

        k+=1

    var = xr.combine_by_coords(var)

    var['name'] = name

    return var

def shallow_xarray(data,days):

    dates=[]

    hour=['00','04','08','12','16','20']

    for i in days:

        for j in hour: 
        
            date_format = '%Y-%m-%dT%H'

            dt_obj=dt.datetime.strptime( '2014-'+i+'T'+j,date_format,) 

            date_obj='2014-'+i+'T'+(j)

            dates.append(date_obj)


    var= data.sel(time=dates,method='nearest')

    #print('creating %s.nc ........... '%(name))
    #var.to_netcdf('%s/%s.nc'%(out_files,name))

    return var

def season_xarray(data,var,lats,lons,levs):

    #summer = var.sel(time=var.time.dt.month.isin([1, 2, 12]))
    #autum  = var.sel(time=var.time.dt.month.isin([3, 4, 5]))
    #winter = var.sel(time=var.time.dt.month.isin([6, 7, 8]))
    #spring = var.sel(time=var.time.dt.month.isin([9, 10, 11]))
    feb    = var.sel(time=var.time.dt.month.isin([2]))

    dd = xr.Dataset(
             data_vars={
                        #'summer':(['timesummer','lev','latitude','longitude'],summer.data),
                        #'winter':(['timewinter','lev','latitude','longitude'],winter.data),
                        #'autum':(['timeautum ' ,'lev','latitude','longitude'],autum.data),
                        #'spring':(['timespring','lev','latitude','longitude'],spring.data),
                        'feb':(['time','levs','latitude','longitude'],feb.data),
                        },
             coords={
             'latitude'   :lats.data,
             'longitude'  :lons.data,
             'levs':levs.data,
             'time':feb.time.data,
             #'timesummer':summer.time.data,
             #'timewinter':winter.time.data,
             #'timeautum': autum.time.data,
             #'timespring':spring.time.data,
             },
        )

    return dd

def anom(index1,index2,data,lats,lons):

	anomalia=np.zeros((index2-index1,len(lats),len(lons)))
	anualmedia=np.mean(data[index1:index2,:,:],axis=0)

	j=0
	for i in range(index1,index2):

		anomalia[j,:,:] = data[i,:,:] - anualmedia[:,:]
		j+=1

	return anomalia
	

def anom2(data,time):

    media=np.mean(data,axis=0)
    std=np.std(data,axis=0)
    
    #anomalia = (datatoanom-media)

    anomalia = (data-media)/std


    return anomalia,media,std

def anom_xarray(data,dim):


    #media=np.mean(data,axis=0)
    mean=data.mean(dim='time')
    std=np.std(data,axis=0)




    #anomalia = (data-data.mean(dim='%s'%(dim)))
    anomalia = (data-mean)/std
    #anomalia = (data-mean)
    dd = xr.Dataset(
             data_vars={'anomaly':(['time','levs','latitude','longitude'],anomalia.data),
                        'mean_time':(['levs','latitude','longitude'],mean.data),
                   'standart_deviation':(['lev.','latitude','longitude'],std.data)
                        },
             coords={
             'latitude':data.latitude.data,
             'longitude':data.longitude.data,
             'levs':data.levs.data,
             'time':data.time.data,
             },
             #name='dsummer'
        )
    
    return dd#,anomalia,media,std

    #anomalia > 0 = chuva maior que a media
    #anomali < 0 = seca
    #

