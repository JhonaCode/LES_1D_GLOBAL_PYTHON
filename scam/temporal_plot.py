###############################################
###############################################

#My own functions

import  scam.data_own            as down

import  scam.figure_own_xr       as fown

import  scam.campain_data        as cd

import  scam.plotparameters      as pp

import  scam.default_values      as df

import matplotlib.ticker as ticker

import nc_time_axis


###from    files_direction                import file_fig, file_temporal,tplot_size

###############################################
# Python standard library datetime  module
import  datetime as dt  

# File to load files and location and # python libraries 
import  numpy               as  np

import  matplotlib          as mpl

import  matplotlib.pyplot    as plt

#to work with date in plots 
import  matplotlib.dates as mdates

#integration 
import  scipy.integrate as integrate

#Python functions
import  pandas as pd

import  cftime

#correlation 

from scipy.stats import pearsonr,spearmanr,kendalltau

#import seaborn as sb

import matplotlib.patches as mpat


import importlib

from   datetime import datetime

import subprocess, sys

#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/scam/', shell = True, executable="/bin/bash")

pars=importlib.import_module('.Parameters_default','scam',)


#var_all.append(var[ni:nf]) 
#
#ax=mean(ax,var_all,data,size)
#To make one reference time for al experiment 
#Where the hour and seconds are really important
#day0=0
#data = down.data_to_reference(ex.data,day0,days[0][4])

def temporal_diurnal_cycle_var_exp(
    exp,date=[],variables=[],var_to=[],explabel1=[],days=[],explabel2=[],lim=[],alt=[],lev=None,plot_def=[],color=[],date0=None,obs=None,date_obs=None,var_obs=None,var_to_obs=None,line=None,show=[],save=None,obs2=None,date_obs2=None,var_obs2=None,var_to_obs2=None, plotpara=None):

    #plotparameters
    if plotpara==None:
        plotpara=[]

    if save==None:
        save=[]

    if lev==None:
        lev=[]

    if line==None:
        line=[]

    if date0==None:
        date0=[]
    
    if obs is None:
        obs=[]

    if obs2 is None:
        obs2=[]

    date_format = '%Y-%m-%dT%H:%M'

    agora = datetime.now()
    # Formata e imprime
    data_formatada = agora.strftime(date_format)

    datenow=dt.datetime.strptime(data_formatada, date_format)


    j=0
    for var in variables:

        print("___________________")
        print("%s"%(var))
        print("___________________")

        plot_defu=df.default_plot(plot_def,j)

        size_wg = plot_defu[3][0]
        size_hf = plot_defu[3][1]
        cmm     = plot_defu[3][2]


        if plotpara:
            tama,figsize= pp.plotsize(plotpara.width,plotpara.height, plotpara.cmm,'temporal')
            tama= plotpara.tama 
            plotpara.parameters["figure.figsize"]=figsize
            mpl.rcParams.update(plotpara.parameters)
        else:
            tama,figsize= pp.plotsize(size_wg,size_hf, cmm,'temporal')

        fig  = plt.figure()
        ax   = plt.axes()


        k=0
        label=''
        for ex in exp:

            limu,altu,var_tou,coloru,explabel1u,explabel2u,plot_defu,showu=df.default_values_1d_new(ex,var,lim,alt,var_to,color,explabel1,explabel2,plot_def,show,k,j,diurnal_cycle=True)

            print("___________________")
            print("__%s__"%(ex.name))
            print("___________________")

            #if name:
            name    =   str(ex.name.values)#+'_'+dates[0]

            print("_temporal__%s__"%(name))

            #date_format = '%Y%m%d%H%M%S'

            datei=dt.datetime.strptime(date[k][0], date_format)
            datef=dt.datetime.strptime(date[k][1], date_format)
    
            time1 = cftime.DatetimeNoLeap(
            datei.year, datei.month, datei.day, datei.hour
            )

            time2 = cftime.DatetimeNoLeap(
                datef.year, datef.month, datef.day, datef.hour
            )

            ni,nf=down.data_n(time1,time2,ex.time.values) 

            tovar= ex.sel(time=slice(ex.time[ni],ex.time[nf-1]))

            data=tovar[var]*var_tou

            if lev:
                try: 
                    tovar= ex.sel(z=lev,method='nearest')
                except: 
                    tovar=tovar

            #time11   =   tovar.time
            #if date0:  
            #    date0 = date0
            #else:
            #    date0 =[1,1,datenow.year]
            #print(time11)
            #print(date0)
            #print(lim)
            #time22,limp=down.data_to_reference_vector(time11,date0,lim,plot_defu[1][1])
            #limu[0]=limp[0]
            #limu[1]=limp[1]

            data=tovar[var]*var_tou

            # Calculate mean diurnal cycle
            diurnal = data.groupby("time.hour").mean(dim="time")

            ax.grid(axis='x',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )
            ax.grid(axis='y',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )

            plt.grid(color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0] )

            #"""
            if line:
                plt.plot(diurnal.hour,diurnal.data,label='%s'%(explabel1u),color=coloru,linewidth=1.5,alpha=1.0,dashes=line[k])
            else:
                plt.plot(diurnal.hour,diurnal.data,label='%s'%(explabel1u),color=coloru,linewidth=1.5,alpha=1.0)

            #"""

            label=label+'_'+"%s"%(name)

            k+=1

        if obs:
    
            datei_obs=dt.datetime.strptime(date_obs[0][0], date_format)
            datef_obs=dt.datetime.strptime(date_obs[0][1], date_format)

            time1_obs = cftime.DatetimeNoLeap(
            datei_obs.year, datei_obs.month, datei_obs.day, datei_obs.hour
            )

            time2_obs = cftime.DatetimeNoLeap(
            datef_obs.year, datef_obs.month, datef_obs.day, datef_obs.hour
            )

            ni_obs,nf_obs=down.data_n(time1_obs,time2_obs,obs.time.values) 


            tovar_obs = obs.sel(time=slice(obs.time[ni_obs],obs.time[nf_obs-1]))

            time_obs  =   tovar_obs.time

            #time_obs,limp2=down.data_to_reference_vector(time_obs,date0,lim,plot_defu[1][1])

            data_obs=tovar_obs[var_obs[j]]*var_to_obs[j]

            # Calculate mean diurnal cycle
            diurnal_obs = data_obs.groupby("time.hour").mean(dim="time")

            try:
                plt.plot(diurnal_obs.hour,diurnal_obs.data[:,0,0],label='%s'%('Radar'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])
            except:                
                plt.plot(diurnal_obs.hour,diurnal_obs.data[:],label='%s'%('Radar'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])

        ###########################
        if obs2:
    
            datei_obs2=dt.datetime.strptime(date_obs[1][0], date_format)
            datef_obs2=dt.datetime.strptime(date_obs[1][1], date_format)

            time1_obs = cftime.DatetimeNoLeap(
            datei_obs.year, datei_obs.month, datei_obs.day, datei_obs.hour
            )

            time2_obs = cftime.DatetimeNoLeap(
            datef_obs.year, datef_obs.month, datef_obs.day, datef_obs.hour
            )

            ni_obs,nf_obs=down.data_n(time1_obs,time2_obs,obs2.time.values) 

            tovar_obs2 = obs2.sel(time=slice(obs2.time[ni_obs],obs2.time[nf_obs]))

            time_obs2  =   tovar_obs2.time

            #if date0:  
            #    date0 = date0
            #else:
            #    date0 =[1,1,datenow.year]
            #time_obs2,limp3=down.data_to_reference_vector(time_obs2,date0,lim,plot_defu[1][1])

            data_obs2=tovar_obs2[var_obs2[j]]*var_to_obs2[j]

            # Calculate mean diurnal cycle
            diurnal_obs2 = data_obs2.groupby("time.hour").mean(dim="time")

            try:
                plt.plot(diurnal_obs2.hour,diurnal_obs2.data[:,0,0],label='%s'%('TRMM'),color='black',linewidth=1.5,alpha=1.0,dashes=[1,1,0,0] )
            except:
                plt.plot(diurnal_obs2.hour,diurnal_obs2.data[:],label='%s'%('TRMM'),color='black',linewidth=1.5,alpha=1.0,dashes=[1,1,0,0])
        ###########################


        fig,ax=plot_temporal_diurnal_cycle_axis(fig,ax,ex,altu,limu,plot_defu,date0,diurnal.hour)

        label="%s_%s"%(name,var)

        if save:
                try: 

                    label=save[1]+"_%s"%(var)
                    plt.savefig('%s/diurnal_cycle_%s.pdf'%(pars.out_fig,label),bbox_inches='tight', format='pdf', dpi=200)
                except:
                    plt.savefig('%s/diurnal_cycle_%s.pdf'%(pars.out_fig,label),bbox_inches='tight', format='pdf', dpi=200)

        j+=1

    if showu:
        plt.show()

    return fig

def temporal_plot_var_exp(
    exp,date=[],variables=[],var_to=[],explabel1=[],days=[],explabel2=[],lim=[],alt=[],lev=None,plot_def=[],color=[],date0=None,obs=None,date_obs=None,var_obs=None,var_to_obs=None,line=None,show=[],save=None,obs2=None,date_obs2=None,var_obs2=None,var_to_obs2=None, plotpara=None):

    #plotparameters
    if plotpara==None:
        plotpara=[]

    if save==None:
        save=[]

    if lev==None:
        lev=[]

    if line==None:
        line=[]

    if date0==None:
        date0=[]
    
    if obs is None:
        obs=[]

    if obs2 is None:
        obs2=[]

    date_format = '%Y-%m-%dT%H:%M'

    agora = datetime.now()
    # Formata e imprime
    data_formatada = agora.strftime(date_format)

    datenow=dt.datetime.strptime(data_formatada, date_format)


    j=0
    for var in variables:

        print("___________________")
        print("%s"%(var))
        print("___________________")

        plot_defu=df.default_plot(plot_def,j)

        size_wg = plot_defu[3][0]
        size_hf = plot_defu[3][1]
        cmm     = plot_defu[3][2]


        if plotpara:
            tama,figsize= pp.plotsize(plotpara.width,plotpara.height, plotpara.cmm,'temporal')
            tama= plotpara.tama 
            plotpara.parameters["figure.figsize"]=figsize
            mpl.rcParams.update(plotpara.parameters)
        else:
            tama,figsize= pp.plotsize(size_wg,size_hf, cmm,'temporal')

        fig  = plt.figure()
        ax   = plt.axes()


        k=0
        label=''

        for ex in exp:

            limu,altu,var_tou,coloru,explabel1u,explabel2u,plot_defu,showu=df.default_values_1d_new(ex,var,lim,alt,var_to,color,explabel1,explabel2,plot_def,show,k,j,diurnal_cycle=True)

            print("___________________")
            print("__%s__"%(ex.name))
            print("___________________")

            #if name:
            name    =   str(ex.name.values)#+'_'+dates[0]

            print("_temporal__%s__"%(name))

            #date_format = '%Y%m%d%H%M%S'

            datei=dt.datetime.strptime(date[k][0], date_format)
            datef=dt.datetime.strptime(date[k][1], date_format)
    
            time1 = cftime.DatetimeNoLeap(
            datei.year, datei.month, datei.day, datei.hour
            )

            time2 = cftime.DatetimeNoLeap(
                datef.year, datef.month, datef.day, datef.hour
            )

            ni,nf=down.data_n(time1,time2,ex.time.values) 

            tovar= ex.sel(time=slice(ex.time[ni],ex.time[nf-1]))

            if lev:

                try: 
                    tovar= ex.sel(z=lev,method='nearest')
                except: 
                    tovar=tovar

            time11   =   tovar.time


            if date0:  
                date0 = date0
            else:
                date0 =[1,1,datenow.year]

            time22,limp=down.data_to_reference_vector(time11,date0,lim,plot_defu[1][1])
            limu[0]=limp[0]
            limu[1]=limp[1]

            data=tovar[var]*var_tou

            ax.grid(axis='x',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )
            ax.grid(axis='y',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )

            plt.grid(color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0] )

            #"""
            if line:

                plt.plot(time22,data,label='%s'%(explabel1u),color=coloru,linewidth=1.5,alpha=1.0,dashes=line[k])

            else:

                plt.plot(time22,data,label='%s'%(explabel1u),color=coloru,linewidth=1.5,alpha=1.0)

            #"""

            label=label+'_'+"%s"%(name)

            k+=1

        if obs:
    
            datei_obs=dt.datetime.strptime(date_obs[0][0], date_format)
            datef_obs=dt.datetime.strptime(date_obs[0][1], date_format)

            time1_obs = cftime.DatetimeNoLeap(
            datei_obs.year, datei_obs.month, datei_obs.day, datei_obs.hour
            )

            time2_obs = cftime.DatetimeNoLeap(
            datef_obs.year, datef_obs.month, datef_obs.day, datef_obs.hour
            )

            ni_obs,nf_obs=down.data_n(time1_obs,time2_obs,obs.time.values) 


            tovar_obs = obs.sel(time=slice(obs.time[ni_obs],obs.time[nf_obs-1]))

            time_obs  =   tovar_obs.time

            time_obs,limp2=down.data_to_reference_vector(time_obs,date0,lim,plot_defu[1][1])

            data_obs=tovar_obs[var_obs[j]]*var_to_obs[j]

            try:
                plt.plot(time_obs,data_obs[:,0,0],label='%s'%('Radar'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])
            except:
                plt.plot(time_obs,data_obs[:],label='%s'%('Radar'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])
        ###########################
        if obs2:
    
            datei_obs2=dt.datetime.strptime(date_obs[1][0], date_format)
            datef_obs2=dt.datetime.strptime(date_obs[1][1], date_format)

            time1_obs = cftime.DatetimeNoLeap(
            datei_obs.year, datei_obs.month, datei_obs.day, datei_obs.hour
            )

            time2_obs = cftime.DatetimeNoLeap(
            datef_obs.year, datef_obs.month, datef_obs.day, datef_obs.hour
            )

            ni_obs,nf_obs=down.data_n(time1_obs,time2_obs,obs2.time.values) 

            tovar_obs2 = obs2.sel(time=slice(obs2.time[ni_obs],obs2.time[nf_obs]))

            time_obs2  =   tovar_obs2.time

            #if date0:  
            #    date0 = date0
            #else:
            #    date0 =[1,1,datenow.year]

            time_obs2,limp3=down.data_to_reference_vector(time_obs2,date0,lim,plot_defu[1][1])

            data_obs2=tovar_obs2[var_obs2[j]]*var_to_obs2[j]

            try:
                plt.plot(time_obs2,data_obs2[:,0,0],label='%s'%('TRMM'),color='black',linewidth=1.5,alpha=1.0,dashes=[1,1,0,0] )
            except:
                plt.plot(time_obs2,data_obs2[:],label='%s'%('TRMM'),color='black',linewidth=1.5,alpha=1.0,dashes=[1,1,0,0])
        ###########################


        fig,ax=plot_temporal_axis(fig,ax,ex,altu,limu,plot_defu,date0,time22)


        label="%s_%s"%(name,var)

        label=label+"_%s"%(var)

        if save:
                try: 

                    label=save[1]+"_%s"%(var)
                    plt.savefig('%s/temporal_%s.pdf'%(pars.out_fig,label),bbox_inches='tight', format='pdf', dpi=200)
                except:
                    plt.savefig('%s/temporal%s.pdf'%(pars.out_fig,label),bbox_inches='tight', format='pdf', dpi=200)

        j+=1

    if showu:
        plt.show()

    return fig

def plot_temporal_diurnal_cycle_axis(fig,ax,ex,alt,lim,plot_def,date0,time):

    ax.xaxis.set_major_locator(ticker.MultipleLocator(lim[2]))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

    ax.tick_params(
    axis="x",
    which="minor",
    bottom=True,
    top=False,
    length=2,
    width=0.5,
    )

    plt.xlabel(r'%s'%(plot_def[0][0])) 
    plt.ylabel(r'%s'%(plot_def[0][1])) 

    if plot_def[2][0]:
        ax.legend(frameon=False,loc=plot_def[2][1])


    #"""
    ax.text(plot_def[1][1],plot_def[1][2], r'%s'%(plot_def[1][0]), fontsize=8, color='black')

    plt.axis([lim[0],lim[1],alt[0],alt[1]])


    return fig,ax

def plot_temporal_axis(fig,ax,ex,alt,lim,plot_def,date0,time):

    #majorFormatter = mpl.dates.DateFormatter(lim[3])
    #print(ex.time)
    #exit()

    #date_form = nc_time_axis.CFTimeFormatter(lim[3],'noleap') 
    #ax.xaxis.set_major_formatter(date_form)
    #ax.xaxis.set_major_locator(locatormax)

    #the first day of simulation if 2026-01-01
    t0_num = mdates.date2num(datetime(2026, 1, 1))

    def day_formatter(x, pos):
        return f'{int(round(x - t0_num)) + 1}'
    
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(day_formatter)
    )

    locatormax = nc_time_axis.NetCDFTimeDateLocator(
        max_n_ticks=10,
        calendar='noleap',
    )

    ax.xaxis.set_major_locator(locatormax)

    locatormin = nc_time_axis.NetCDFTimeDateLocator(
        max_n_ticks=20,
        calendar='noleap'
    )

    major = ax.xaxis.get_majorticklocs()

    minor = (major[:-1] + major[1:]) / 2.0

    ax.xaxis.set_minor_locator(
    mpl.ticker.FixedLocator(minor)
    )

    ax.tick_params(
    axis="x",
    which="minor",
    bottom=True,
    top=False,
    length=2,
    width=0.5,
    )

    plt.xlabel(r'%s'%(plot_def[0][0])) 
    plt.ylabel(r'%s'%(plot_def[0][1])) 

    if plot_def[2][0]:
        ax.legend(frameon=False,loc=plot_def[2][1])

    date_format = '%Y-%m-%dT%H:%M'
    pd=dt.datetime.strptime(plot_def[1][1], date_format)

    #"""
    ax.text(pd,plot_def[1][2], r'%s'%(plot_def[1][0]), fontsize=8, color='black')

    plt.axis([time[lim[0]],time[lim[1]],alt[0],alt[1]])


    return fig,ax

def polifit(x, y, degree):
    results = {}
    coeffs = np.polyfit(x, y, degree)
    p = np.poly1d(coeffs)
    #calculate r-squared
    yhat = p(x)
    ybar = np.sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)
    sstot = np.sum((y - ybar)**2)
    #results['r_squared'] = ssreg / sstot
    results= ssreg / sstot

    return results


def color_hours(hour): 
    line=[1,0]
    color='k'

    if    hour==0:
          #line=[3,2,1,2]
          line=[1,0]
          color='blue'
    if    hour==1:
          line=[1,0]
          color='orange'
    if    hour==2:
          line=[1,0]
          #line=[2,1]
          color='magenta'
    elif  hour==3:
          #line=[3, 1]
          line=[1,0]
          color='red'
    elif  hour==4:
          line=[4, 1]
          color='green'
    elif  hour==5:
          #line=[1,1]
          line=[1,0]
          color='purple'
    elif  hour==6:
          line=[1,2,1,2]
          color='tab:orange'
    elif  hour==7:
          line=[2,1,1,3]
          color='tab:brown'
    elif  hour==8:
          line=[2,1,5,3]
          color='navy'
    elif  hour==9:
          line=[4,2,1,2]
          color='y'
    elif  hour==10:
          line=[1,2,4,2]
          color='c'

    return line,color
