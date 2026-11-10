###########################################
# PYTHON FILE TO 
# DEFINED MULTIPLES PLOT PROJECTION
#USING THE BASEMAP LIBRARY
###########################################

import numpy  as np 

import matplotlib as mpl

import matplotlib.pyplot as plt

import sources.plotparameters as pn

import cartopy.crs as ccrs

import cartopy.feature as cfeature

from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import datetime as dt

import pandas   as pd

import  os,sys

import importlib

import subprocess, sys

#from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/sources/', shell = True, executable="/bin/bash")

#used the user parameter to plot(plotparameter.py) if para:
#pars=__import__('source.Parameters_default',globals())
pars=importlib.import_module('.Parameters_default','sources',)

#2014-02-01T00:00:00.00000000
date_format = '%Y-%m-%dT%H:%M'##+':00.00000000'

def profile_plot(data,varname=None,label=[],date_str=[],lat=None,lon=None,lev=[],vmulti=[],color=[],ylim=None,title=None,xtitle=None,ytitle=None,out='',para=[],figname=[],units=[],show=True,save=False):

    global pars
    #date_format = '%HZ%d%b%Y'
    date_format = '%Y%m%d%H'

    if varname==None:
        varname=[]

    if xtitle==None:
        xtitle=[]

    if ytitle==None:
        ytitle=[]

    if units==None:
       units=[]

    if para:
        pars=importlib.import_module('.%s'%(para),'source')

    #parans=pn.plotsize(pars.profile['plotdef'],pars.wf,pars.hf,pars.cmmais)
    parans=pn.plotsize(pars.profile['plotdef'],pars.profile['wf'],pars.profile['hf'],pars.profile['cmmais'])

    #fontsize=parans['font.size']
    fontsize=pars.profile['fontsize']


    fig = plt.figure()
    ax  = fig.add_subplot()

    ax.invert_yaxis()
    #plt.gca().invert_yaxis()


    j=0
    for da in data:

        if lat:
            lat=lat
        if lon:
            lon=lon

        if varname:
            var=ajust_var(da,varname,date_str[j],lev,lat,lon)
        else: 
            var=ajust_var(da,0,date_str[j],lev,lat,lon)

        if vmulti:
            var=var*vmulti[j]

        plt.plot(var[::1],var.lev[::-1],color=color[j],label=label[j])

        j+=1


    # Add the custom legend
    ax.legend( frameon=False, fontsize=fontsize-1,loc='center left')

    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.grid(True, axis="x", linestyle="--", alpha=0.6)
    
    #locatormax = mpl.dates.MonthLocator(interval=5)
    #ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d%b'))

    if ylim:

        ax.set_ylim(ylim)

    if title:

        plon=title

        ax.set_title("%s"%(plon),fontsize=fontsize,fontweight="bold")

        if xtitle:

            #ax.set_xlabel(xtitle,fontweight="bold",fontsize=fontsize)
            ax.set_xlabel(xtitle,fontsize=fontsize)

        if ytitle:

            #ax.set_ylabel(ytitle,fontweight="bold",fontsize=fontsize)
            ax.set_ylabel(ytitle,fontsize=fontsize)

    if figname:
        fign=figname
    else:
        fign=f'profile_{varname}_{date_str}'

    if save:

        fig.savefig('%s/%s.pdf'%(pars.out_fig,fign),bbox_inches='tight', format='pdf', dpi=200)

    if show:

        plt.show()
               
    return fig,ax     

def temporal_plot(data,varname=None,label=[],dates=None,date_str=[],lat=None,lon=None,lev=[],vmulti=[],color=[],ylim=None,title=None,xtitle=None,ytitle=None,out='',para=[],figname=[],units=[],show=True,save=False):

    global pars
    date_format = '%HZ%d%b%Y'

    if dates==None:
        dates=[]

    if dates:
        datei=dt.datetime.strptime(dates[0], date_format)
        datef=dt.datetime.strptime(dates[1], date_format)


    if varname==None:
        varname=[]

    if xtitle==None:
        xtitle=[]

    if ytitle==None:
        ytitle=[]

    if units==None:
       units=[]

    if para:
        pars=importlib.import_module('.%s'%(para),'source')
    
    pn.plotsize(pars.temporal['plotdef'],pars.temporal['wf'],pars.temporal['hf'],pars.temporal['cmmais'])

    fig = plt.figure()
    ax  = fig.add_subplot()

    j=0
    for da in data:

        if lev:
            lev=lev[j]
        if lat:
            lat=lat[j]
        if lon:
            lon=lon[j]

        if varname:
            var=ajust_var(da,varname,date_str,lev,lat,lon)
        else: 
            var=ajust_var(da,0,date_str,lev,lat,lon)

        if vmulti:
            var=var*vmulti[j]

        if dates:
            var= var.sel(time=slice(datei,datef))
            ax.set_xlim(datei,datef)

        plt.plot(var.time,var,color=color[j],label=label[j])

        j+=1

    # Add the custom legend
    ax.legend( frameon=False, fontsize=6)

    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.grid(True, axis="x", linestyle="--", alpha=0.6)

    #ax.xaxis.set_minor_locator(locatormin)
    #ax.xaxis.set_major_locator(locatormax )
    
    #majorformatter = mpl.dates.dateformatter('%d') #majorformatter = mpl.dates.dateformatter('%m-%d %h:%m:%s')
    #ax.xaxis.set_major_formatter(majorformatter)
    locatormax = mpl.dates.MonthLocator(interval=5)
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d%b'))
    #locatormin = mpl.dates.DayLocator(interval=2)
    #ax.xaxis.set_minor_formatter(mpl.dates.DateFormatter(''))
    #locatormin = mpl.dates.Daylocator(interval=30)


    if ylim:

        ax.set_ylim(ylim)

    if title:

        plon=title

        ax.set_title("%s"%(plon),fontsize=6,fontweight="bold")

        if xtitle:

            ax.set_xlabel(xtitle,fontweight="bold",fontsize=6)

        if ytitle:

            ax.set_ylabel(ytitle,fontweight="bold",fontsize=6)
    if figname:
        fign=figname
    else:
        fign=f'temporal_{varname}_{datei}_{datef}'

    if save:

        fig.savefig('%s/%s.pdf'%(pars.out_fig,fign),bbox_inches='tight', format='pdf', dpi=200)

    if show:

        plt.show()
               
    return fig,ax     


def countour_plot(data,varname=None,date_str=[],lats=[],lons=[],lev=[],vmulti=[],bcolor=[],lat=[],lon=[],xtitle=None,ytitle=None,plotname=[],color='RdBu_r',out='',cbar=True,para=[],figname=[],units=[],extend=[],show=True,save=True,fmt=".1f"):

    global pars
    
    if varname==None:
        varname=[]

    if xtitle==None:
        xtitle=[]

    if ytitle==None:
        ytitle=[]

    if units==None:
       units=[]

    if varname:
        var=ajust_var(data,varname,date_str,lev)
    else: 
        var=data
        var=ajust_var(var,0,date_str,lev)

    if not extend:
        extend=pars.extend

    if para:
        pars=importlib.import_module('.%s'%(para),'source')


    if vmulti:
        var=var*vmulti

    parans=pn.plotsize(pars.plotdef,pars.wf,pars.hf,pars.cmmais)

    fontsize=parans['font.size']


    fig = plt.figure()
    ax  = fig.add_subplot(1, 1, 1, projection=pars.projection)
    #ax  = plt.axes(projection=projection)

    ax=def_axis_states(ax)

    try:
        var.latitude
    except:
        var=latitude_lat(var)

    try:
        var.longitude
    except:
        var=longitude_lon(var)

    #Axis definitions
    ax,levels,latitude,longitude=axis_def(ax,var,bcolor,lats,lat,lons,lon,fontsize)

    #print(var) #exit()
    #lines  = ax.contour(longitude, latitude, var[:,:], levels=levels,
    #                    colors=['black'] ,alpha=0.8,linewidths=0.5,
    #                    transform=ccrs.PlateCarree())

     #Plot contours with automatic color mapping instead of fixed black


    cs = ax.contour(
                    longitude, latitude, var[:,:],
                    levels=levels,
                    #cmap="viridis",       # or "jet", "coolwarm", etc.
                    cmap=color,       # or "jet", "coolwarm", etc.
                    alpha=1.0,
                    linewidths=parans['lines.linewidth'],
                    transform=ccrs.PlateCarree()
                )

    # Add labels on contour lines
    ax.clabel(
        cs, 
        inline=True,          # nicely inline with the line
        fmt=f"%{fmt}",        # format numbers (1 decimal place)
        fontsize=fontsize-1, 
        colors="black",        # label text color (can also pass a dict per level)
        inline_spacing=1,    # smaller = more labels
        manual=False,        # label text color (can also pass a dict per level)
    )

    #for txt in cs.labelTexts:
    #    txt.set_clip_path(ax.patch)


     # Add a colorbar for the filled contour.
     #fig.colorbar(filled, orientation='horizontal',shrink=0.5)

    if plotname:

        plon=plotname

        ax.set_title("%s"%(plon),fontsize=fontsize+1,fontweight="bold")

        # Second title (subtitle) under the figure
        #fig.text(0.5, 0.22, f"Countors from {levels[0]} to {levels[-1]} each {levels[-1]-levels[0]}",ha="center",va='bottom',fontsize=6,fontweight="bold")
        if xtitle:

            ax.set_xlabel(xtitle,fontweight="bold",fontsize=fontsize+1)

        if ytitle:

            ax.set_ylabel(xtitle,fontweight="bold",fontsize=fontsize+1)



    else:
        if lev:
            try:
                plon='%s_%s\n%s_%shpa'%(data.name.values,varname,date_str,lev)
            except:
                plon=''
        else:
            try:
                plon='%s_%s\n%s'%(data.name.values,varname,date_str)
            except:
                plon=''

    if figname:
        fign=figname
    else:
        if lev:
            fign='contour_%s_%s_%s_%s'%(data.name.values,varname,date_str,lev)
        else:
            fign='contour_%s_%s_%s'%(data.name.values,varname,date_str)

    if save:

        fig.savefig('%s/%s.pdf'%(pars.out_fig,fign),bbox_inches='tight', format='pdf', dpi=200)

    if show:

        plt.show()
               
    return fig     


def cartopy_plot(data,varname=None,date_str=[],lats=[],lons=[],lev=[],vmulti=[],bcolor=[],lat=[],lon=[],plotname=[],color='RdBu_r',out='',cbar=True,para=[],figname=[],units=[],extend=[],show=True,save=True,contours=True,xtitle=None,ytitle=None,fmt='.f'):

    global pars

    if xtitle==None:
        xtitle=[]

    if ytitle==None:
        ytitle=[]
    
    if varname==None:
        varname=[]

    if units==None:
       units=[]

    if varname:
        var=ajust_var(data,varname,date_str,lev)
    else: 
        var=data
        var=ajust_var(var,0,date_str,lev)

    if not extend:
        extend=pars.extend

    if para:
        pars=importlib.import_module('.%s'%(para),'source')


    if vmulti:
        var=var*vmulti

    parans=pn.plotsize(pars.plotdef,pars.wf,pars.hf,pars.cmmais)

    fontsize=parans['font.size']

    fig = plt.figure()
    ax  = fig.add_subplot(1, 1, 1, projection=pars.projection)
    #ax  = plt.axes(projection=projection)

    ax=def_axis_states(ax)

    try:
        var.latitude
    except:
        var=latitude_lat(var)

    try:
        var.longitude
    except:
        var=longitude_lon(var)

    #Axis definitions
    ax,levels,latitude,longitude=axis_def(ax,var,bcolor,lats,lat,lons,lon)


    filled=ax.contourf(longitude, latitude, var[:,:], levels=levels,
                transform=ccrs.PlateCarree(),
                cmap=color,alpha=1.0,extend=extend)


    if contours:
        lines  = ax.contour(longitude, latitude, var[:,:], levels=filled.levels,
                        colors=['black'] ,alpha=0.8,linewidths=0.5,
                        transform=ccrs.PlateCarree())

        
        # Add labels on contour lines
        labels=ax.clabel(
            lines, 
            inline=True,          # nicely inline with the line
            fmt=f"%{fmt}",        # format numbers (1 decimal place)
            fontsize=fontsize, 
            colors="black",        # label text color (can also pass a dict per level)
            inline_spacing=10,    # smaller = more labels
            manual=False,        # label text color (can also pass a dict per level)
        )

    #for txt in labels:
    #    txt.set_fontweight('bold')


    if cbar: 
        CB=fig.colorbar(filled, orientation='vertical',shrink=0.5)
        CB.set_ticks(levels)

        if units:

            CB.ax.set_title(r'%s'%units,fontsize=fontsize-1,fontweight="bold")

        else:
            CB.ax.set_title(r'%s'%var.units,fontsize=fontsize,fontweight="bold")

        # Add a colorbar for the filled contour.
        #fig.colorbar(filled, orientation='horizontal',shrink=0.5)

    if plotname:

        plon=plotname

        ax.set_title("%s"%(plon),fontsize=fontsize,fontweight="bold")
        if xtitle:

            ax.set_xlabel(xtitle,fontweight="bold",fontsize=fontsize)

        if ytitle:

            ax.set_ylabel(xtitle,fontweight="bold",fontsize=fontsize)

    else:
        if lev:
            try:
                plon='%s_%s\n%s_%shpa'%(data.name.values,varname,date_str,lev)
            except:
                plon=''
        else:
            try:
                plon='%s_%s\n%s'%(data.name.values,varname,date_str)
            except:
                plon=''

        ax.set_title("%s"%(plon),fontsize=fontsize,fontweight="bold")

    if figname:
        fign=figname
    else:
        if lev:
            fign='contour_%s_%s_%s_%s'%(data.name.values,varname,date_str,lev)
        else:
            fign='contour_%s_%s_%s'%(data.name.values,varname,date_str)

    if save:

        fig.savefig('%s/%s.pdf'%(pars.out_fig,fign),bbox_inches='tight', format='pdf', dpi=200)

    if show:

        plt.show()
               
    return fig     

def cartopy_vector_1d(u_name,v_name,data,data2=[0],dates_str=[],scale=1, width=0.4,lats=[],lat=[],levs=[],lev=[],bcolor=[],plotname='',color='RdBu_r',cbar=True,magwind=1,para=[],xtitle=None,ytitle=None,units=None,figname=[],save=False,show=True,fmt=None,headlength=1,text=None):

    global pars

    if xtitle==None:
        xtitle=[]

    if ytitle==None:
        ytitle=[]

    if units==None:
       units=[]

    if para:
        pars=importlib.import_module('.%s'%(para),'source')

    try:
        u=data[u_name]
        v=data[v_name]
        u=ajust_var(data,u_name,dates_str)
        v=ajust_var(data,v_name,dates_str)
    except:

        u=u_name
        v=v_name

    parans=pn.plotsize(pars.epf['plotdef'],pars.epf['wf'],pars.epf['hf'],pars.epf['cmmais'])

    fontsize=parans['font.size']

    fig = plt.figure()
    ax  = plt.axes()

    #ax  = def_axis_states(ax)

    try:
        u.latitude
    except:
        u=latitude_lat(u)
    try:
        v.latitude
    except:
        v=latitude_lat(v)

    try:
        u.level
    except:
        u=level_lev(u)

    try:
        v.level
    except:
        v=level_lev(v)

    try:
        data2.level
    except:
        data2=level_lev(data2)

    try:
        data2.latitude
    except:
        data2=latitude_lat(data2)


    ax,level,latitude,dates,contorns=axis_def_1d(ax,u,bcolor,lats,lat,levs,lev,fontsize=fontsize)


    #print(u.latitude.values)
    #print(data2.latitude.values)
    #exit()

    x       = data2.latitude[:]
    y       = data2.level[:]


    X,Y     = np.meshgrid(x,y)

    #"""

    filled = ax.contour(
                    X,Y,
                    data2[0,:,:,0],
                    levels=contorns,
                    cmap=color,   
                    alpha=1.0,
                    linewidths=2.0,
                )

    # Add labels on contour lines
    labels=ax.clabel(
        filled, 
        inline=True,          # nicely inline with the line
        fmt=f"%{fmt}",        # format numbers (1 decimal place)
        fontsize=fontsize+1, 
        colors="black",        # label text color (can also pass a dict per level)
        inline_spacing=10,    # smaller = more labels
        manual=False,        # label text color (can also pass a dict per level)

    )

    for txt in labels:
        txt.set_fontweight('bold')
    #"""

    #Each arrow length ≈ vector magnitude × (1 / scale).
    max_speed = np.nanmax(np.sqrt(u**2 + v**2))
    scale = max_speed * scale 

    npp=pars.npp
    npp=4
    qv = ax.quiver(u.latitude[::npp], u.level[::1] ,u[::1,::npp].values, v[::1,::npp].values, color='black',alpha=0.75,scale=scale, width=width)#,headlength=headlength)


    ax.quiverkey(qv, X=0.99, Y=-0.06, U=magwind,label=f"($F_\psi,F_p$)\n{magwind} [m/s]", labelpos='S',fontproperties={'size':fontsize,'weight':'bold'}, labelsep=0.01)


    if text:

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='white', alpha=1.0,  edgecolor='white')
        ax.text(-69,20, text, color='black',fontsize=8,verticalalignment='top', bbox=props, zorder=100)

    if cbar:
    # Add a colorbar for the filled contour.
        CB=fig.colorbar(filled, orientation='vertical',shrink=0.5)
        CB.set_ticks(levels)

    if plotname:

        plon=plotname

        ax.set_title("%s"%(plon),fontsize=fontsize,fontweight="bold")

        if xtitle:

            ax.set_xlabel(xtitle,fontweight="bold",fontsize=fontsize)

        if ytitle:

            ax.set_ylabel(ytitle,fontweight="bold",fontsize=fontsize)


    else:
        if lev:
            try:
                plon='%s_%s\n%s_%shpa'%(data.name.values,varname,date_str,lev)
            except:
                plon=''
        else:
            try:
                plon='%s_%s\n%s'%(data.name.values,varname,date_str)
            except:
                plon=''

    if figname:
        fign=figname
    else:
        if lev:
            fign='vector_%s_%s_%s_%s'%(data.name.values,varname,date_str,lev)
        else:
            fign='vector_%s_%s_%s'%(data.name.values,varname,date_str)

    if save:

        fig.savefig('%s/%s.pdf'%(pars.out_fig,fign),bbox_inches='tight', format='pdf', dpi=200)

    if show:

        plt.show()
               
    return fig     

def cartopy_vector(u_name,v_name,data,data2=[0],date_str=[],lev=[],scale=1, width=0.4,lats=[],lons=[],bcolor=[],lat=[],lon=[],plotname='',color='RdBu_r',cbar=True,magwind=1,para=[],xtitle=None,ytitle=None,units=None,figname=[],save=False,show=True,fmt=None,headlength=1):

    global pars

    if xtitle==None:
        xtitle=[]

    if ytitle==None:
        ytitle=[]

    if units==None:
       units=[]

    if para:
        pars=importlib.import_module('.%s'%(para),'source')

    try:
        u=data[u_name]
        v=data[v_name]
        u=ajust_var(data,u_name,date_str,lev)
        v=ajust_var(data,v_name,date_str,lev)
    except:
        u=u_name
        v=v_name

    parans=pn.plotsize(pars.plotdef,pars.wf,pars.hf,pars.cmmais)

    fontsize=parans['font.size']

    fig = plt.figure()
    ax  = plt.axes(projection=pars.projection)

    ax  = def_axis_states(ax)

    try:
        u.latitude
    except:
        u=latitude_lat(u)
    try:
        v.latitude
    except:
        v=latitude_lat(v)

    try:
        u.longitude
    except:
        u=longitude_lon(u)

    try:
        v.longitude
    except:
        v=longitude_lon(v)

    ax,levels,latitude,longitude=axis_def(ax,u,bcolor,lats,lat,lons,lon,fontsize=fontsize)

    #if(len(data2)==1):
    #    data2 = np.sqrt(u**2 + v**2)


    """
    filled=ax.contourf(longitude, latitude, data2[0,:,:], levels=levels,
                transform=ccrs.PlateCarree(),
                #cmap='coolwarm',alpha=1.0)
                #cmap='Spectral_r',alpha=1.0)
                #cmap='RdYlBu_r',alpha=1.0)
                cmap=color,alpha=1.0,extend='both')
    """
    filled = ax.contour(
                    longitude, latitude, data2[0,:,:],
                    levels=levels,
                    cmap=color,   
                    alpha=1.0,
                    linewidths=1.4,
                    transform=ccrs.PlateCarree()
                )

    # Add labels on contour lines
    labels=ax.clabel(
        filled, 
        inline=True,          # nicely inline with the line
        fmt=f"%{fmt}",        # format numbers (1 decimal place)
        fontsize=fontsize+1, 
        colors="black",        # label text color (can also pass a dict per level)
        inline_spacing=10,    # smaller = more labels
        manual=False,        # label text color (can also pass a dict per level)
    )

    for txt in labels:
        txt.set_fontweight('bold')
    #
    #qv = ax.quiver(lons, lats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=800, width=0.002)

    #qv = ax.quiver(lons, lats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=250, width=0.0035)#,headlength=0.05)

    npp=pars.npp

    qv = ax.quiver(longitude[::npp], latitude[::npp] ,u[0,::npp,::npp].values, v[0,::npp,::npp].values, transform=ccrs.PlateCarree(),color='navy',alpha=0.75,scale=scale, width=width)#,headlength=headlength)

    #ax.quiverkey(qv, X=1.00, Y=1.10, U=100,label=r'100[kgkg$^{-1}$ms$^{-1}$Pa]', labelpos='E',fontproperties={'size':5})
    ax.quiverkey(qv, X=.94, Y=-0.09, U=magwind,label=f"{magwind}\n[m/s]", labelpos='E',fontproperties={'size':fontsize,'weight': 'bold'}, labelsep=0.01)
    
    #qv = ax.quiver(lons, lats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=1, width=0.0015)#,headlength=0.05)

    if cbar:
    # Add a colorbar for the filled contour.
        CB=fig.colorbar(filled, orientation='vertical',shrink=0.5)
        CB.set_ticks(levels)

    if plotname:

        plon=plotname

        ax.set_title("%s"%(plon),fontsize=fontsize,fontweight="bold")

        # Second title (subtitle) under the figure
        #fig.text(0.5, 0.22, f"Countors from {levels[0]} to {levels[-1]} each {levels[-1]-levels[0]}",ha="center",va='bottom',fontsize=6,fontweight="bold")
        if xtitle:

            ax.set_xlabel(xtitle,fontweight="bold",fontsize=fontsize)

        if ytitle:

            ax.set_ylabel(xtitle,fontweight="bold",fontsize=fontsize)



    else:
        if lev:
            try:
                plon='%s_%s\n%s_%shpa'%(data.name.values,varname,date_str,lev)
            except:
                plon=''
        else:
            try:
                plon='%s_%s\n%s'%(data.name.values,varname,date_str)
            except:
                plon=''

    if figname:
        fign=figname
    else:
        if lev:
            fign='vector_%s_%s_%s_%s'%(data.name.values,varname,date_str,lev)
        else:
            fign='vector_%s_%s_%s'%(data.name.values,varname,date_str)

    if save:

        fig.savefig('%s/%s.pdf'%(pars.out_fig,fign),bbox_inches='tight', format='pdf', dpi=200)

    if show:

        plt.show()
               
    return fig     

def cartopy_vector_uv(u,v,data=[0],date_str=[],lev=[],scale=1, width=0.4,lats=[],lons=[],bcolor=[],lat=[],lon=[],plotname='',figname='',color='RdBu_r',out='',cbar=True,xtitle=None):

    u=ajust_var(u,'u',date_str,lev)
    v=ajust_var(v,'v',date_str,lev)

    pn.plotsize(plotdef,wf,hf,cmmais)

    fig = plt.figure()
    ax  = plt.axes(projection=projection)

    ax  = def_axis_states(ax)

    ax,levels,latitude,longitude=axis_def(ax,u,bcolor,lats,lat,lons,lon)

    if(len(data)==1):

        data = np.sqrt(u**2 + v**2)

    filled=ax.contourf(longitude, latitude, data[0,0,:,:], levels=levels,
                transform=ccrs.PlateCarree(),
                #cmap='coolwarm',alpha=1.0)
                #cmap='Spectral_r',alpha=1.0)
                #cmap='RdYlBu_r',alpha=1.0)
                cmap=color,alpha=1.0,extend='both')
    #
    #qv = ax.quiver(lons, lats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=800, width=0.002)

    #qv = ax.quiver(lons, lats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=250, width=0.0035)#,headlength=0.05)

    npp=10

    qv = ax.quiver(longitude[::npp], latitude[::npp] ,u[0,0,::npp,::npp].values, v[0,0,::npp,::npp].values, transform=ccrs.PlateCarree(),color='black',scale=scale, width=width)#,headlength=0.05)

    #ax.quiverkey(qv, X=1.00, Y=1.10, U=100,label=r'100[kgkg$^{-1}$ms$^{-1}$Pa]', labelpos='E',fontproperties={'size':5})
    ax.quiverkey(qv, X=1.05, Y=1.02, U=10,label=r'10', labelpos='E',fontproperties={'size':5}, labelsep=0.01)
    
    #qv = ax.quiver(lons, lats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=1, width=0.0015)#,headlength=0.05)

    if cbar:
    # Add a colorbar for the filled contour.
        CB=fig.colorbar(filled, orientation='vertical',shrink=0.5)
        CB.set_ticks(levels)

    ax.set_title("%s"%(plotname),fontsize=6)

    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=200)
               
    return fig,qv     

def barra(color='RdBu_r',b1=100,b2=100,nn=10,plotname='',figname='',out='',label=''):

    if b1==b2 and b1==100:

        b1=np.min(data[:].values)
        b2=np.max(data[:].values)

    levels= np.linspace(b1,b2,nn,endpoint=True)

    fig,ax = plt.subplots(figsize=(4,0.5))
    fig.subplots_adjust(bottom=0.5)

    cmap = color
    norm = mpl.colors.Normalize(vmin=b1, vmax=b2)
    CB=fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),cax=ax, orientation='horizontal',shrink=1.0,extend='both',label=label)
    cbarlabels = np.linspace(b1,b2,11,endpoint=True)

    #CB.set_ticks(cbarlabels[::3])
    #CB.ax.set_title(r'%s'%clabel,fontsize=6)

    #ax.quiverkey(q, X=0.25, Y=0.45, U=500,label=r'[kgkg$^{-1}$ms$^{-1}$Pa]', labelpos='E')


    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=100)

def narrow_q(q,plotname='',figname='',out='',label=''):


    fig,ax = plt.subplots(figsize=(8,0.5))
    #fig.subplots_adjust(bottom=0.5)

    ax.quiverkey(q, X=0.25, Y=0.45, U=500,label=r'[kgkg$^{-1}$ms$^{-1}$Pa]', labelpos='E')


    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=100)
               
    return fig     


def ajust_var(data,varname,date_str=[],lev=None,lat=None,lon=None):

    global pars

    if lat==None:
        lat=[]
    if lon==None:
        lon=[]
    if lev==None:
        lev=[]

    if varname!=0:

        var=getattr(data,varname)

        try:
            var.time
        except:
            var=time_Time(var)
    
    else:
        var=data

    
    if lev: 

        try:
            var.level
        except:
            var=level_lev(var)

        var= var.sel(level=var.level.isin([lev]))
        var= np.squeeze(var,1)

    else: 
        var=var 


    if lat:

        try:
            var.latitude 
        except:
            var=latitude_lat(var)
        var = var.sel(latitude=lat, method='nearest')

        print(var.latitude)


    if lon:

        try:
            var.longitude
        except:
            var=longitude_lon(var)

        var = var.sel(longitude=lon, method='nearest')

    if date_str: 

        #date_format  = '%Y-%m-%d_%H.%M'+'.00'
        date_obj=dt.datetime.strptime(date_str, date_format)

        #print(var)
        var= var.sel(time=[date_obj])

    try:
        var=var.squeeze(drop=True)
    except:
        var=var

    #else:
    #
    #    var= var.isel(time=[0])
    

    return var

def time_select(date_str,var): 

    #print(var.time)
    #exit()
    #date_format  = '%Y-%m-%d_%H.%M'+'.00'
    date_obj=dt.datetime.strptime(date_str, date_format)

    var= var.sel(time=[date_obj])

    return var


def def_axis_1(ax):

    #ax.set_global()
    #ax.stock_img()
    ax.coastlines()
    gl=ax.gridlines(draw_labels=False, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')


    #MOMO STATES
    ax.add_feature(cfeature.STATES.with_scale('50m'))


    return ax

def def_axis_states(ax):

    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    #ax.set_global()
    #ax.stock_img()
    
    ax.coastlines( linestyle='-', alpha=1.00,linewidth=0.5)

    #grid
    ax.gridlines(draw_labels=False)

    #ax.add_feature(cfeature.LAND)

    #Contries
    ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=1.00,facecolor='none',linewidth=0.25)

    ax.add_feature(cfeature.LAKES, edgecolor='navy',alpha=1.00,facecolor='none',linewidth=0.25)

    ax.add_feature(cfeature.RIVERS, edgecolor='navy',alpha=1.00,facecolor='none',linewidth=0.25)


    #MOMO STATES
    #ax.add_feature(cfeature.STATES.with_scale('50m'))

    states = cfeature.NaturalEarthFeature(category='cultural', scale='50m', facecolor='none', name='admin_1_states_provinces_lines')

    ax.add_feature(states, edgecolor='black',alpha=1.0,linewidth=0.25)

    #resol = '50m'
    #bodr = cfeature.NaturalEarthFeature(category='cultural', 
    #name='admin_0_boundary_lines_land', scale=resol, facecolor='none', alpha=0.7)
    #ax.add_feature(bodr, linestyle='--', edgecolor='k', alpha=1)
    #plt.show()
    #exit()

    return ax

def time_Time(ds):

    ds = ds.rename({"Time": "time"})

    return ds

def level_lev(ds):

    ds = ds.rename({"lev": "level"})

    return ds

def latitude_lat(ds):

    ds = ds.rename({"lat": "latitude"})

    return ds

def longitude_lon(ds):

    ds = ds.rename({"lon": "longitude"})

    return ds


def axis_def(ax,var,bcolor,lats,lat,lons,lon,fontsize=6):


    if lats:
        latitude =lats
    else:
        latitude =var.latitude

    if lons:
        try:
            longitude=lons
        except:
            longitude=var.longitude


    if bcolor:
        b1=bcolor[0]
        b2=bcolor[1]
        bn=bcolor[2]
    else: 
        b1=np.min(var[:])
        b2=np.max(var[:])
        bn=5

    levels= np.linspace(b1,b2,bn,endpoint=True)

    #levels = np.arange(b1,b2,bn)

    if(lat):
        maxlat= lat[0]
        minlat= lat[1]
        nlat  = lat[2] 
        levels_lat= np.linspace(minlat,maxlat,nlat,endpoint=True)
        
    else:

        maxlat= np.max(var.latitude)
        minlat= np.min(var.latitude)
        levels_lat= np.linspace(minlat,maxlat,5,endpoint=True)

    if(lon):

        maxlon= lon[0]
        minlon= lon[1]
        nlon  = lon[2] 

        levels_lon= np.linspace(minlon,maxlon,nlon,endpoint=True)

    else:
        maxlon= max(var.longitude)
        minlon= min(var.longitude)
        levels_lon= np.linspace(minlon,maxlon,5,endpoint=True)

    #ax.set_xlim([minlon, maxlon])
    #ax.set_ylim([minlat ,maxlat])
    ax.set_extent([minlon, maxlon, minlat,maxlat],crs=ccrs.PlateCarree())

    ax.set_xticks(levels_lon, crs=ccrs.PlateCarree())
    ax.set_yticks(levels_lat, crs=ccrs.PlateCarree())

    lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')

    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    #ax.xlabel_style = {'size': 6, 'color': 'red'}
    #xlabel_style = {'color': 'red', 'weight': 'bold'}
    #ax.tick_params(axis='both', labelsize=8)
    ax.tick_params(axis='x', labelsize=fontsize)
    ax.tick_params(axis='y', labelsize=fontsize)


    # Use the line contours to place contour labels.
    #ax.clabel(
    #    lines,  # Typically best results when labelling line contours.
    #    colors=['black'],
    #    manual=False,  # Automatic placement vs manual placement.
    #    inline=True,  # Cut the line where the label will be placed.
    #    fmt=' {:.0f} '.format,  # Labes as integers, with some extra space.
    #)

    return ax,levels,latitude,longitude

def axis_def_1d(ax,var,bcolor,lats,lat,levs,lev,fontsize=6,dates=None):


    if lats:
        latitude =lats
    else:
        latitude =var.latitude

    if levs:
        level=levs
    else:
        level=var.level

    if bcolor:
        b1=bcolor[0]
        b2=bcolor[1]
        bn=bcolor[2]
    else: 
        b1=np.min(var[:])
        b2=np.max(var[:])
        bn=5

    levels= np.linspace(b1,b2,bn,endpoint=True)

    if(lat):
        minlat= lat[0]
        maxlat= lat[1]
        nlat  = lat[2] 
        levels_lat= np.linspace(minlat,maxlat,nlat,endpoint=True)
    else:
        maxlat= np.max(var.latitude)
        minlat= np.min(var.latitude)
        levels_lat= np.linspace(minlat,maxlat,5,endpoint=True)


    ax.set_xticks(levels_lat, crs=ccrs.PlateCarree())

    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')

    ax.xaxis.set_major_formatter(lat_formatter)

    ax.set_xlim([minlat ,maxlat])

    if(lev):
        maxlev   = lev[0]
        minlev   = lev[1]
        #step     = lev[2]
        #nlev     = int((maxlev - minlev+ 1)/step )
        nlev     = lev[2]
        levels_lev= np.linspace(minlev,maxlev,nlev,endpoint=True)
    else:
        maxlev= np.max(var.level)
        minlev= np.min(var.level)
        levels_lev= np.linspace(minlev,maxlev,5,endpoint=True)
        #levels_lev= np.linspace(minlev,maxlev,nlev,endpoint=True)


    ax.set_ylim([maxlev, minlev])
    ax.set_yticks(levels_lev)

    loc=mpl.ticker.MultipleLocator(100)
    ax.yaxis.set_major_locator(loc)

    #if dates==None:
    #    dates=[]
    #else:
    #    date_format = '%HZ%d%b%Y'
    #    datei=dt.datetime.strptime(dates[0], date_format)
    #    datef=dt.datetime.strptime(dates[1], date_format)
    #    ax.set_xlim(datei,datef)
    #locatormax = mpl.dates.MonthLocator(interval=5)
    #ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d%b'))

    ax.tick_params(axis='x', labelsize=fontsize)
    ax.tick_params(axis='y', labelsize=fontsize)

    return ax,level,latitude,dates,levels
