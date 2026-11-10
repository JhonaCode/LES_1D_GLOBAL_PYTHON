###############################################
###############################################

#My own functions

import  sam_python.data_own            as down

import  sam_python.figure_own          as fown

import  sam_python.campain_data        as cd

import  sam_python.plotparameters      as pp

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

from    cftime import num2date, num2pydate

#correlation 

from scipy.stats import pearsonr,spearmanr,kendalltau

#import seaborn as sb

import matplotlib.patches as mpat


import  sam_python.default_values as df

#import  campain_data  as cd
import  sam_python.data_own       as down

import importlib

from   datetime import datetime

import subprocess, sys

#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/sam_python/', shell = True, executable="/bin/bash")

pars=importlib.import_module('.Parameters_default','sam_python',)


#var_all.append(var[ni:nf]) 
#
#ax=mean(ax,var_all,data,size)
#To make one reference time for al experiment 
#Where the hour and seconds are really important
#day0=0
#data = down.data_to_reference(ex.data,day0,days[0][4])

def temporal_plot_exp_var_xr(exp,date=[],variables=[],var_to=[],explabel1=[],days=[],explabel2=[],lim=[],alt=[],lev=None,plot_def=[],color=[],date0=None,obs=None,date_obs=None,var_obs=None,var_to_obs=None,line=None,show=[],save=None,obs2=None,date_obs2=None,var_obs2=None,var_to_obs2=None):


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

        tama= pp.plotsize(size_wg,size_hf, cmm,'temporal')

        fig  = plt.figure()
        ax   = plt.axes()


        k=0
        label=''

        for ex in exp:

            limu,altu,var_tou,coloru,explabel1u,explabel2u,plot_defu,showu=df.default_values_1d_new(ex,var,lim,alt,var_to,color,explabel1,explabel2,plot_def,show,k,j)

            print("___________________")
            print("__%s__"%(ex.name))
            print("___________________")

            #if name:
            name    =   str(ex.name.values)#+'_'+dates[0]

            print("_temporal__%s__"%(name))

            #date_format = '%Y%m%d%H%M%S'

            datei=dt.datetime.strptime(date[k][0], date_format)
            datef=dt.datetime.strptime(date[k][1], date_format)
    
            time1 = np.datetime64(date[k][0]) 
            time2 = np.datetime64(date[k][1])
    

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


            time22=down.data_to_reference_vector(time11,date0)

            data=tovar[var]*var_tou

            #ax.grid(axis='y',linewidth=1.0,alpha=0.6,linestyle='--')#,dashes=[1,1,0,0] )
            ax.grid(axis='x',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )
            ax.grid(axis='y',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )

            plt.grid(color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0] )

            #"""
            if line:

                plt.plot(time22,data,label='%s'%(explabel1u),color=coloru,linewidth=1.5,alpha=1.0,dashes=line[k])

            else:

                plt.plot(time22,data,label='%s'%(explabel1u),color=coloru,linewidth=1.5,alpha=1.0)

            #"""
            k+=1

            label=label+'_'+"%s"%(name)

        if obs:
    
            time1_obs = np.datetime64(date_obs[j][0]) 
            time2_obs = np.datetime64(date_obs[j][1])

            ni_obs,nf_obs=down.data_n(time1_obs,time2_obs,obs.time.values) 

            tovar_obs = obs.sel(time=slice(obs.time[ni_obs],obs.time[nf_obs-1]))

            time_obs  =   tovar_obs.time

            if date0:  
                date0 = date0
            else:
                date0 =[1,1,datenow.year]

            #print(time_obs)
            #exit()
            #print('xx',var_obs[j])
            #print(data_obs[:])

            time_obs=down.data_to_reference_vector(time_obs,date0)

            data_obs=tovar_obs[var_obs[j]]*var_to_obs[j]

            try:
                plt.plot(time_obs,data_obs[:,0,0],label='%s'%('Radar'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])
            except:
                plt.plot(time_obs,data_obs[:],label='%s'%('Radar'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])
        ###########################
        if obs2:
    
            time1_obs = np.datetime64(date_obs[j][0]) 
            time2_obs = np.datetime64(date_obs[j][1])

            ni_obs,nf_obs=down.data_n(time1_obs,time2_obs,obs2.time.values) 

            tovar_obs2 = obs2.sel(time=slice(obs2.time[ni_obs],obs2.time[nf_obs]))

            time_obs2  =   tovar_obs2.time

            if date0:  
                date0 = date0
            else:
                date0 =[1,1,datenow.year]


            time_obs2=down.data_to_reference_vector(time_obs2,date0)

            data_obs2=tovar_obs2[var_obs2[j]]*var_to_obs2[j]

            try:
                plt.plot(time_obs2,data_obs2[:,0,0],label='%s'%('TRMM'),color='black',linewidth=1.5,alpha=1.0,dashes=[1,1,0,0] )
            except:
                plt.plot(time_obs2,data_obs2[:],label='%s'%('TRMM'),color='black',linewidth=1.5,alpha=1.0,dashes=[1,1,0,0])
        ###########################

        fig,ax=plot_temporal_axis(fig,ax,ex,altu,limu,plot_defu,date0)

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

def temporal_plot_cloud_xr(exp,date=[],variables=[],var_to=[],explabel1=[],days=[],explabel2=[],alt=[],plot_def=[],color=[],show=[]):

    print("___________________")
    print("%s"%(variables))
    print("___________________")
    
    plot_defu=df.default_plot(plot_def,0)
    
    size_wg = plot_defu[3][0]
    size_hf = plot_defu[3][1]
    cmm     = plot_defu[3][2]
    
    tama= pp.plotsize(size_wg,size_hf, cmm,'temporal')
    
    fig  = plt.figure()
    ax   = plt.axes()
    
    k=0
    label=''
    for ex in exp:
    
        limu,altu,var_tou,coloru,explabel1u,explabel2u,plot_defu,showu=df.default_values_1d_new(ex,variables[0],date,alt,var_to,color,explabel1,explabel2,plot_def,show,k,0)

        #limu2,altu2,var_tou2,coloru2,explabel1u,explabel2u,plot_defu,showu=df.default_values_1d_new(ex,variable[1],date,alt,var_to,color,explabel1,explabel2,plot_def,show,k,j)
    
        print("___________________")
        print("__%s__"%(ex.name))
        print("___________________")
    
        #if name:
        name    =   str(ex.name.values)#+'_'+dates[0]
    
        print("_temporal__%s__"%(name))
    
        #date_format = '%Y%m%d%H%M%S'
        date_format = '%Y-%m-%dT%H'
        datei=dt.datetime.strptime(date[k][0], date_format)
        datef=dt.datetime.strptime(date[k][1], date_format)
    
        time1 = np.datetime64(date[k][0]) 
        time2 = np.datetime64(date[k][1])
    
        ni,nf=down.data_n(time1,time2,ex.time.values) 
        #print(time1,ni)
        #print(time2,nf)
        #print('llltime2')
    
        tovar= ex.sel(time=slice(ex.time[ni],ex.time[nf-1]))
    
        #time1=tovar.time.values 
        time11   =   tovar.ltime[ni:nf]
        #time1   =   ex.ltime[0].dt.day
        #print(time1.values)
        #exit()
        time22=down.data_to_reference_vector(time11,1,1,2025)
        #print(time22)
        #exit()
    
        data1=tovar[variables[0]]*var_tou
        data2=tovar[variables[1]]*var_tou
    
        ax.grid(axis='y',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )

        plt.plot(time22,data1,label='%s'%(explabel1u),color=coloru,linewidth=1.0,alpha=1.0)
        plt.plot(time22,data2 , color=coloru,linewidth=1.0,alpha=1.0)
    
        k+=1
    
        label=label+'_'+"%s"%(name)
    
    fig,ax=plot_temporal_axis(fig,ax,ex,altu,limu,plot_defu)
    
    #label="%s_%s"%(name,var)
    label=label+"_%s_%s"%(variables[0],variables[1])
    
    plt.savefig('%s/cloud_1d_%s.pdf'%(pars.out_fig,label),bbox_inches='tight', format='pdf', dpi=200)
    
    if showu:
        plt.show()

    return fig

def temporal_plot_var_exp(exp,var=[],var_to=[],explabel1=[],days=[],explabel2=[],alt=[],plot_def=[],lim=[],color=[],show=[]):

    exp_var=var

    k=0
    for vtex in exp_var:

        if k==0:

            if not var:
                exp_var=exp[k].var1d

        lim,alt,var_to,color,explabel1,explabel2,plot_def,show = df.default_values_1d(exp,exp_var,lim,alt,var_to,color,explabel1,explabel2,plot_def,show,k)


        size_wg = plot_def[k][0][3][0] 
        size_hf = 0.5
        plotsize(size_wg,size_hf, plot_def[k][0][3][1],'temporal')

        fig  = plt.figure()
        ax   = plt.axes()

        j=0
        for ex in exp:

            print('\n')
            print('_______________________________________')
            print('       ________%s_______'%(ex.name))
            print('_______________________________________')
            print('\n')

            if days:

                idi     = dt.datetime(days[k][0][0][0], days[k][0][0][1] ,days[k][0][0][2], days[k][0][0][3],days[k][0][0][4],0) 
                idf     = dt.datetime(days[k][0][1][0], days[k][0][1][1] ,days[k][0][1][2], days[k][0][1][3],days[k][0][1][4],0)

                ni,nf= down.data_n(idi,idf,ex.date[:])

                if ni>len(ex.date):
                    ni=ni-1

            else:
                #days=ex.datei+ex.datef
                ni,nf= down.data_n(ex.datei,ex.datef,ex.date[:])


            var=getattr(ex, vtex)
            var=var[ni:nf]*var_to[j][k]

            print(var_to[j][k])

            date=ex.date[ni:nf]

            ax.grid(axis='y',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )

            print('For '+ex.name+' ploting '+vtex)


            plt.plot(date,var,label='%s'%(explabel1[j][k]),color=color[k][j],linewidth=1.0,alpha=1.0)


            exname=ex.name

            j+=1

        fig,ax=plot_temporal_axis(fig,ax,ex,alt[k][0],lim[k][0],plot_def[k][0])

        plt.savefig('%s/temporal_%s.pdf'%(file_temporal,vtex),bbox_inches='tight', format='pdf', dpi=1000)

        if show[k]:
            plt.show()

        k+=1


    return fig

def temporal_plot_exp_var(exp,var=[],var_to=[],explabel1=[],days=[],explabel2=[],alt=[],plot_def=[],lim=[],color=[],show=[]):

    exp_var=var

    k=0

    for ex in exp:

        if k==0:

            if not var:
                exp_var=ex.var1d

        print('\n')
        print('_______________________________________')
        print('       ________%s_______'%(ex.name))
        print('_______________________________________')
        print('\n')


        lim,alt,var_to,color,explabel1,explabel2,plot_def,show = df.default_values_1d(exp,exp_var,lim,alt,var_to,color,explabel1,explabel2,plot_def,show,k)


        j=0
        for vtex in exp_var:

            if days:

                idi     = dt.datetime(days[k][j][0][0], days[k][j][0][1] ,days[k][j][0][2], days[k][j][0][3],days[k][j][0][4],0) 
                idf     = dt.datetime(days[k][j][1][0], days[k][j][1][1] ,days[k][j][1][2], days[k][j][1][3],days[k][j][1][4],0)

                ni,nf= down.data_n(idi,idf,ex.date[:])

                if ni>len(ex.date):
                    ni=ni-1

            else:
                #days=ex.datei+ex.datef
                ni,nf= down.data_n(ex.datei,ex.datef,ex.date[:])


            var=getattr(ex, vtex)
            var=var[ni:nf]*var_to[k][j]
            date=ex.date[ni:nf]

            #ax.grid(axis='y',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )

            print('For '+ex.name+' ploting '+vtex)

            #ni,nf= down.data_n(ex.datei,ex.datef,ex.date[:])
            #date= ex.date[ni:nf]
            #to make the plot with the variables defined
            #fig,ax=temporal_plot(fig,ax,date,var,k=j,exp_label=exp_label[k][j],color=color[j])
            #plt.plot(data,var,label='%s'%(exp_label1),color=color,linewidth=1.0,alpha=1.0,dashes=line,marker='')

            size_wg = plot_def[k][j][3][0] 
            size_hf = 0.5
            plotsize(size_wg,size_hf, plot_def[k][j][3][1],'diurnal')

            fig  = plt.figure()
            ax   = plt.axes()

            plt.plot(date,var,label='%s'%(explabel1[k][j]),color=color[k][j],linewidth=1.0,alpha=1.0)

            fig,ax=plot_temporal_axis(fig,ax,ex,alt[k][j],lim[k][j],plot_def[k][j])

            #exname=ex.name

            j+=1


        #to defined the plot characteristics 
        #fig,ax=plot_temporal_axis(fig,ax,ex,lim=lim[k],plot_def=plot_def[k])

        plt.savefig('%s_%s_%s.pdf'%(file_temporal,exname,vn),bbox_inches='tight', format='pdf', dpi=1000)

        if show[k][j]:
            plt.show()

        k+=1


    return fig

def temporal_plot_dict(exp,var_to=0,exp_label=0,plot_def=0,lim=0,color=0,show=0):

    size_wg = tplot_size 
    size_hf = 0.5
    plotsize(size_wg,size_hf, 0.0,'diurnal')

    k=0
    for vn in exp.var_to_plot:

        #To plot 
        fig  = plt.figure()
        ax   = plt.axes()

        ni,nf= down.data_n(exp.datei,exp.datef,exp.data[:])

        ##Extract the variables to plot
        if var_to==0:
            var=exp.nc_f[vn][ni:nf]
        else:
            var=exp.nc_f[vn][ni:nf]*var_to[k]

        data= exp.data[ni:nf]

        #to make the plot with the variables defined
        fig,ax=temporal_plot(fig,ax,data,var,k=k,exp_label=exp_label[k],color=color)
        #to defined the plot characteristics 
        fig,ax=plot_temporal_axis(fig,ax,exp,lim=lim[k],plot_def=plot_def[k])

        plt.savefig('%s_%s_%s.pdf'%(file_temporal,exp.name,vn),bbox_inches='tight', format='pdf', dpi=1000)

        if show==0:
            plt.show()
        elif show[k]:
            plt.show()

        k+=1

    return fig

def temporal_plot_exp(exp,var_to=0,exp_label=0,plot_def=0,lim=0,color=0,show=True):

    size_wg = tplot_size 
    size_hf = 0.5
    plotsize(size_wg,size_hf, 0.0,'diurnal')

    #print(var_to,'xxxxxxxxxxxxx')
    k=0
    for vn in exp[k].var1d:

        #To plot 
        fig  = plt.figure()
        ax   = plt.axes()

        j=0
        exname=''
        for ex in exp:

            print('For '+ex.name+' ploting '+vn)

            ni,nf= down.data_n(ex.datei,ex.datef,ex.date[:])

            ##Extract the variables to plot
            if var_to==0:
                var=ex.nc_f[vn][ni:nf]

            else:
                var=ex.nc_f[vn][ni:nf]*var_to[k][j]
                #print(ex.nc_f[vn].units,var_to[k][j],'xxxxxxxx')

            date= ex.date[ni:nf]

            #to make the plot with the variables defined
            fig,ax=temporal_plot(fig,ax,date,var,k=j,exp_label=exp_label[k][j],color=color[j])

            exname=exname+'_'+ex.name

            j+=1

        #to defined the plot characteristics 
        fig,ax=plot_temporal_axis(fig,ax,ex,lim=lim[k],plot_def=plot_def[k])

        plt.savefig('%s_%s_%s.pdf'%(file_temporal,exname,vn),bbox_inches='tight', format='pdf', dpi=1000)


        k+=1

    #plt.show()
    if show:
       plt.show()

    #for ex in exp:
    #  exname=''

    #  j=0
    #  for vn in ex.var_to_plot:

    #      #To plot
    #      if k==0:
    #          f1  = plt.figure(j)
    #          ax1 = plt.axes()
    #          fig.append(f1)
    #          ax.append(ax1)

    #          print('xx')

    #      print('For '+ex.name+' ploting '+vn)

    #      ni,nf= down.data_n(ex.datei,ex.datef,ex.data[:])

    #      ##Extract the variables to plot
    #      if var_to==0:
    #          var=ex.nc_f[vn][ni:nf]
    #      else:
    #          var=ex.nc_f[vn][ni:nf]*var_to[k][j]

    #      data= ex.data[ni:nf]

    #      #to make the plot with the variables defined



    return fig

def temporal_plot(fig,ax,data,var,k=0,exp_label=0,color=0):


    #Extract the variables to plot
    if color==0:    
        line,col =color_hours(k)
    else:
        line=[1,0]
        col=color[k]

    plt.plot(data,var,label='%s'%(exp_label),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')

    return fig,ax


def plot_temporal_axis(fig,ax,ex,alt,lim,plot_def,date0):


    #plot_def
    #[ [X,Y], ['a)',dt.datetime(2014,3,5,0),120],[False,'upper left'],[0.35,0]]
    
    lmin=lim[0]
    lmax=lim[1]
    #interval=int(ex.date.shape[0]/4)
    interval=lim[2]

    locatormax = mdates.HourLocator(interval=interval)
    locatormin = mdates.HourLocator(interval=int(interval/2))

    majorFormatter = mpl.dates.DateFormatter('%H')
    ax.xaxis.set_major_formatter(majorFormatter)

    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )


    #d1=dt.datetime(plot_def[1][1][0],plot_def[1][1][1],plot_def[1][1][2],plot_def[1][1][3])
    date_format = '%Y-%m-%dT%H:%M'
    #d1=dt.datetime.strptime(plot_def[1][1], date_format)
    d1 = np.datetime64(plot_def[1][1]) 
    #d1=dt.datetime(plot_def[1][1],plot_def[1][1],plot_def[1][2],plot_def[1][3])

    plt.xlabel(r'%s'%(plot_def[0][0])) 
    plt.ylabel(r'%s'%(plot_def[0][1])) 

    #lim1 = np.datetime64(lim[0]) 
    #lim2 = np.datetime64(lim[1]) 
    # Converte especificando o formato exato

    lim1=pd.to_datetime(lim[0], format=date_format)
    lim2=pd.to_datetime(lim[1], format=date_format)

    #lim1 = lim1.strftime(date_format)
    #lim2 = lim2.strftime(date_format)

    lim1 = down.data_to_reference(lim1,date0)
    lim2 = down.data_to_reference(lim2,date0)

    plt.axis( [lim1,lim2,alt[0],alt[1]])

    ax.text(d1,plot_def[1][2], r'%s'%(plot_def[1][0]), fontsize=8, color='black')

    if plot_def[2][0]:
        ax.legend(frameon=False,loc=plot_def[2][1])


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

def temporal_cases(exp,days,exp_label,exp_label2,exp_label_cape,lim):

    #First day of the experiment 
    k=0

    #size=0.6
    #fig,ax =fown.figure_sam(0.4)

    tke_all =[]
    mmc_all =[]
    data_all=[]
    cape_all=[]
    cin_all =[]
    rho_all =[]


    for ex in exp:

        #All experiment have the same time, the first day of 2014 
        idi     = dt.datetime(days[k][0],days[k][1],days[k][2], days[k][3]) 
        idf     = dt.datetime(days[k][4],days[k][5],days[k][6], days[k][7]) 

        size= ex.date.shape[0]

        di,df= down.data_n(idi,idf,ex.date)


        #cin and cape from other program
        data_f,cape_f,cin_f=read_cape_cin(exp_label_cape[k])
        #day0=to control de first day of the begins of
        #the experiment. day0=0, first day 1
        day0=0
        data_c = down.data_to_reference(data_f,day0,days[0][6])

        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        data = down.data_all(ex.data,k)

        tam = df-di 

        cape          =   np.zeros(tam)
        cin           =   np.zeros(tam)
        bowen         =   np.zeros(tam)

        rho           =   np.zeros(tam)
        tkeint        =   np.zeros(tam)
        tkeint_pbl    =   np.zeros(tam)
        tkeint_cloud  =   np.zeros(tam)
        tkeint_cloud2 =   np.zeros(tam)

        mtke          =   np.zeros(tam)
        itke          =   np.zeros(tam)
        mmc           =   np.zeros(tam)

        indexant=0
        maxl    =100
        j       =0

        for i in range(di,df):

            cape[j] =cape_f[i] 
            cin[j]  =cin_f[i] 

            bowen[j]=ex.SHF[i]/(ex.LHF[i]+1.0e-5)

            indexmin  =   np.argmin(ex.TVFLUX[i][0:maxl]) 

            mmc[j]    =   np.mean(ex.MCUP[i][indexmin-5:indexmin+5]) 
            mini      =   ex.TVFLUX[i][indexmin] 

            itke[j]   =   np.mean(ex.TKE[i][indexmin-2:indexmin]) 
            imc  =   np.argmax(ex.MCUP[i][0:maxl]) 
            #mmc[j]    =   np.mean(ex.MCUP[i][indexmin-6:indexmin+6]) 
            mmc[j]    =   ex.MCUP[i][imc] 
            tkeint_pbl[j]   = 1.0/(ex.z[indexmin]-ex.z[0])  *integrate.simps(ex.TKE[i][0:indexmin],ex.z[0:indexmin])

            rho[j]          = ex.RHO[i][indexmin] 

            ###if(mini>=0.0):
            ###    #indexmin        = indexant
            ###    tkeint_pbl[j]   = ex.TVFLUX[i][indexmin] 
            ###    rho[j]          = ex.RHO[i][indexmin] 
            ###else:
            ###    rho[j]          = 1.0/(ex.z[indexmin]-ex.z[0])  *integrate.simps(ex.RHO[i][0:indexmin],ex.z[0:indexmin])
            ###    tkeint_pbl[j]   = 1.0/(ex.z[indexmin]-ex.z[0])  *integrate.simps(ex.TKE[i][0:indexmin],ex.z[0:indexmin])


            j=j+1


        massflux1  = 0.8*rho*np.sqrt(1.0*tkeint_pbl)*np.exp(-(0.08*cin/tkeint_pbl))
        #massflux2  = 0.06*(0.28*np.sqrt(tkeint_pbl)+0.64)*np.exp(-(1.0*cin/tkeint_pbl))
        #massflux1  = 0.06*(0.28*np.sqrt(itke)+0.64)*np.exp(-(1.0*np.sqrt(cin)/itke))
        fig = plt.figure()
        ax  = plt.axes()
        plt.plot( data[di:df], massflux1,color='blue' )
        plt.plot( data[di:df], mmc,color='green' )
        #plt.plot( data[di:df], massflux2,color='red' )
        #plt.plot( data[di:df], cin,color='red' )

        plt.show()

        exit()
        
        #plt.plot(data[di:df]       ,mmc           ,label='%s'%(exp_label2[k]),color='blue',linewidth=1.0,alpha=1.0,marker='')
        #plt.plot(data[di:df]       ,itke           ,label='%s'%(exp_label2[k]),color='blue',linewidth=1.0,alpha=1.0,marker='')
        #plt.plot(data[di:df]       ,tkeint_pbl    ,label='%s'%(exp_label2[k]),color='red',linewidth=1.0,alpha=1.0,marker='')
        #plt.plot(data[di:df]       ,rho          ,label='%s'%(exp_label2[k]),color='m',linewidth=1.0,alpha=1.0,marker='')
        #plt.plot(data[di:df]       ,cin          ,label='%s'%(exp_label2[k]),color='orange',linewidth=1.0,alpha=1.0,marker='')
        #plt.show()

        
        tke_all.append(itke[:]) 
        #tke_all.append(tkeint_pbl[:]) 
        mmc_all.append(mmc[:]) 
        data_all.append(data[di:df]) 
        cape_all.append(cape[:]) 
        cin_all.append(cin[:]) 
        rho_all.append(rho[:]) 

        #massflux1      = 0.4*rho*np.sqrt(tkeint_pbl)*np.exp(-(cin)/tkeint_pbl)
        #massflux2      = 0.4*rho*np.sqrt(tkeint_pbl)*np.exp(-(cin+1)/tkeint_pbl)
        #massflux3      = 0.4*rho*np.sqrt(tkeint_pbl)*np.exp(-(1)/tkeint_pbl)


        #fig = plt.figure()
        #ax  = plt.axes()

        #plt.plot(  massflux1, mmc ,'s' ,color='red')
        #fig = plt.figure()
        #ax  = plt.axes()
        #plt.plot(  massflux2, mmc,  's' ,color='green')
        #fig = plt.figure()
        #ax  = plt.axes()
        #plt.plot( massflux3,mmc,    's' ,color='green')

        #plt.plot( data_all[0][:], tke_all[0][:],color='green')
        #plt.plot( data_all[0][:], cin_all[0][:],color='blue' )

        plt.show() 

        k+=1

    #ax=mean(ax,lhf_all,ex.data,size)

    #il     = dt.datetime(2014, 1 ,1, 17) 
    #ax.text(il,350 , r'%s'%('b)'), fontsize=9, color='black')
    #plt.show()

    #
    #locatormax = mdates.DayLocator(interval=10)
    #locatormin = mdates.DayLocator(interval=1)
    #ax.xaxis.set_minor_locator(locatormin)
    #ax.xaxis.set_major_locator(locatormax )

    #ax.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
    #
    idi     = dt.datetime(2014,1,1, 0) 
    idf     = dt.datetime(2014,1,31,23) 
    #plt.axis( [idi,idf,0 ,400])
    #
    plt.ylabel(r' Latent Heat FLux $\mathrm{ [W m^{-2}]}$') 
    plt.xlabel(r'Days') 

    #ax.legend(frameon=False)
    #plt.show()

    tke     =   np.concatenate(tke_all,axis=0)
    umf     =   np.concatenate(mmc_all,axis=0)
    cape    =   np.concatenate(cape_all,axis=0)
    cin     =   np.concatenate(cin_all,axis=0)
    rho     =   np.concatenate(rho_all,axis=0)

    print(rho)
    print(cin)
    print(tke)

    massflux1  = tke#0.4*rho*np.sqrt(tke)*np.exp(-(cin)/tke)
    massflux2  = cin#0.4*rho*np.sqrt(tke)*np.exp(-(cin+1)/tke)
    #massflux3  = 0.4*rho*np.sqrt(tke)*np.exp(-(cin)/tke)
    massflux3  = 0.06*(0.28*np.sqrt(tke)+0.64)*np.exp(-(1*cin)/tke)

    fig = plt.figure()
    ax  = plt.axes()
    #plt.plot(  umf, np.sqrt(tke)*np.exp(-cin/tke),  '*' )
    #plt.plot( umf, massflux3,   's' ,color='green')
    plt.plot( data_all[0][:], massflux3 ,color='green')

    #corr3, st3 = pearsonr(umf,massflux3 )


    #corr1, st1 = spearmanr(massflux1, umf)
    #corr2, st2 = spearmanr(massflux2, umf)
    #corr3, st3 = spearmanr(massflux3, umf)

    #print corr1,corr2,corr3

    #corr1, st1 = kendalltau(massflux1, umf)
    #corr2, st2 = kendalltau(massflux2, umf)
    #corr3, st3 = kendalltau(massflux3, umf)

    #print corr1,corr2,corr3
    ##massflux2      = 0.28*np.sqrt(tke)+0.64



    #sb.jointplot(x = umf, y = massflux1,
    #          kind = "kde")
    #sb.jointplot(x = umf, y = massflux2,
    #          kind = "kde")


    #plt.axis( [0,0.6,0 ,.6])

    
    #fig.set_size_inches(4.5, 2)
    #plt.savefig('%stemporal_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)
    plt.show()


    return fig

def maxmassflux(exp,days,exp_label,exp_label2,lim):

####################################
    k=0

    fig,ax =fown.figure_sam(0.4)
   
    mass_all=[] 

    #All experiment have the same time, the first day of 2021 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    for ex in exp:

        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        #print ex.data[0]
        #day0=to control de first day of the begins of
        #the experiment. day0=0, first day 1
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        if exp_label2[k]=='BOMEX':

            data= data + dt.timedelta(hours=8)


        size= ex.data.shape[0]

        tam = ex.MCUP.shape[0]

        maxmc=[]

        for i in range(0,tam):

            mmc       = np.max(ex.MCUP[i][:]) 

            maxmc.append(mmc)

        line,col =color_hours(k)

        plt.plot( data[0:size]     ,maxmc[0:size]      ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        mass_all.append(maxmc)

        k=k+1

    ax  =   mean(ax,mass_all,data,size)

    il  = dt.datetime(2014, 1 ,1, 17) 
    ax.text(il,0.098 , r'%s'%('d)'), fontsize=9, color='black')
    
    #Ticks of the axisss
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)
    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )

    plt.axis( [idi,idf,lim[0], lim[1]])
    
    plt.xlabel(r'Hours LT (UTC-4)') 
    plt.ylabel(r'Maximum uMF $\mathrm{[kg m^{-2} s^{-1}]}$') 
    
    ax.legend(frameon=False)
    
    #fig.set_size_inches(4.5, 2)
    plt.savefig('%smax_massflux_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()
    #exit()

def basewupdraft(exp,days,exp_label,exp_label2,lim):

####################################
    k=0


    fig,ax =fown.figure_sam(0.4)
   
    mass_all=[] 

    #All experiment have the same time, the first day of 2014 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])


    for ex in exp:

        var=ex.WSUP
        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        #print ex.data[0]

        #the experiment. day0=0, first day 1
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        if exp_label2[k]=='BOMEX':
            data= data + dt.timedelta(hours=8)

        size= ex.data.shape[0]

        tam = var.shape[0]

        maxmc=[]
        maxl=30

        for i in range(0,tam):

            index1  =  np.argmin(ex.TVFLUX[i][0:maxl]) 

            for j in range(1,8):

                index2=index1+j
    
                if ex.TVFLUX[i][index2]>0 and index1>6:
    
                    indexmin=index2 

                    break

                else: 
                    indexmin=index1
    

            mmc       =   (var[i][indexmin]) 
            #mmc       =   1/5.0*(var[i][indexmin+1]+var[i][indexmin-1]+var[i][indexmin+2]+var[i][indexmin-2]+var[i][indexmin]) 

            maxmc.append(mmc)

        line,col =color_hours(k)

        step=2
        ax.plot( data[0:size:step]     ,maxmc[0:size:step]      ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')

        mass_all.append(maxmc)

        k=k+1

    ax=mean(ax,mass_all,data,size)

    il     = dt.datetime(2014, 1 ,1, 17) 
    ax.text(il,0.098 , r'%s'%('d)'), fontsize=9, color='black')
    
    #Ticks of the axisss
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)
    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    
    plt.axis( [idi,idf,lim[0], lim[1]])

    
    plt.xlabel(r'Hours LT (UTC-4)') 
    plt.ylabel(r'Base Wu $\mathrm{[m s^{-1}]}$') 
    
    ax.legend(frameon=False)
    
    #fig.set_size_inches(4.5, 2)

    plt.savefig('%sbase_wupdraft_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()
    #exit()

def pbl_cbase_h(exp,days,exp_label,exp_label2,lim):

####################################
    k=0


    fig,ax =fown.figure_sam(0.4)

    mass_all=[] 

    #All experiment have the same time, the first day of 2014 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    for ex in exp:

        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        #print ex.data[0]

        #the experiment. day0=0, first day 1
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        if exp_label2[k]=='BOMEX':
            data= data + dt.timedelta(hours=8)

        size= ex.data.shape[0]

        tam = ex.MCUP.shape[0]

        maxmc=[]
        pblh =[]
        cbase=[]
        ctop =[]


        maxl=30

        index1=0
        index2=0
        index3=0


        for i in range(0,tam):

            index1  =  np.argmin(ex.TVFLUX[i][0:maxl]) 

            for j in range(1,6):

                index2=index1+j
    
                if ex.TVFLUX[i][index2]>0 and index1>4:
    
                    indexmin=index2 

                    break

                else: 
                    indexmin=index1

            for i1 in range(1,70):

                index3=index2+i1

                if ex.QC[i][index3]<0.0001 :

                    indexmax=index3 

                    break
                #else: 
                #    indexmax=index2
    
            pblh.append(ex.z[index1]/1000.0)
            cbase.append(ex.z[indexmin]/1000.0)
            ctop.append(ex.z[indexmax]/1000.0)


        line,col =color_hours(k)



        step=1
        if(exp_label2[k]=='Large'):

            ax.plot( data[0:size:step] , pblh[0:size:step]  ,color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='*')

        ax.plot( data[0:size:step]     , cbase[0:size:step] ,color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')

        ax.plot( data[0:size:step]     , ctop[0:size:step]  ,color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')

        mass_all.append(maxmc)

        k=k+1

    ax=mean(ax,mass_all,data,size)

    il     = dt.datetime(2014, 1 ,1, 17) 
    ax.text(il,0.098 , r'%s'%('d)'), fontsize=9, color='black')
    
    #Ticks of the axisss
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)

    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )


    loc=mpl.ticker.MultipleLocator(0.5)

    ax.yaxis.set_major_locator(loc)
    #ax.yaxis.set_minor_locator(locatormin)
    
    plt.axis( [idi,idf,lim[0], lim[1]])

    
    plt.xlabel(r'Hours LT (UTC-4)') 
    plt.ylabel(r'h $\mathrm{[km]}$') 
    
    ax.legend(frameon=False)
    

    plt.savefig('%spbl_cloud_base_h_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()
    #exit()

def basemassflux(exp,days,exp_label,exp_label2,lim):

####################################
    k=0


    fig,ax =fown.figure_sam(0.4)

    mass_all=[] 

    #All experiment have the same time, the first day of 2014 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    for ex in exp:

        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        #print ex.data[0]

        #the experiment. day0=0, first day 1
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        if exp_label2[k]=='BOMEX':
            data= data + dt.timedelta(hours=8)

        size= ex.data.shape[0]

        tam = ex.MCUP.shape[0]

        maxmc=[]
        pblh =[]
        cbase=[]

        maxl=30

        for i in range(0,tam):

            index1  =  np.argmin(ex.TVFLUX[i][0:maxl]) 

            for j in range(1,9):

                index2=index1+j
    
                if ex.TVFLUX[i][index2]>0 and index1>6:
    
                    indexmin=index2 
                    #print(index1,ex.TVFLUX[i][index1])
                    #print(index2,ex.TVFLUX[i][index2])
                    break
                else: 
                    indexmin=index1
    
            #print(index1,ex.TVFLUX[i][index1])
            #print(index2,ex.TVFLUX[i][index2])
            #print(indexmin,ex.TVFLUX[i][indexmin])
            #exit()


            #mmc       =   (ex.MCUP[i][indexmin]) 

            mmc       =   1/5.0*(ex.MCUP[i][indexmin+1]+ex.MCUP[i][indexmin-1]+ex.MCUP[i][indexmin+2]+ex.MCUP[i][indexmin-2]+ex.MCUP[i][indexmin]) 
            #mmc       =   1/3.0*(ex.MCUP[i][indexmin+1]+ex.MCUP[i][indexmin-1]+ex.MCUP[i][indexmin]) 

            maxmc.append(mmc)

            pblh.append(ex.z[index1])
            cbase.append(ex.z[indexmin])


        line,col =color_hours(k)


        step=2

        ax.plot( data[0:size:step]     ,maxmc[0:size:step]      ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')

        mass_all.append(maxmc)

        k=k+1

    ax=mean(ax,mass_all,data,size)

    il     = dt.datetime(2014, 1 ,1, 17) 
    ax.text(il,0.098 , r'%s'%('d)'), fontsize=9, color='black')
    
    #Ticks of the axisss
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)
    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    
    plt.axis( [idi,idf,lim[0], lim[1]])

    plt.xlabel(r'Hours LT (UTC-4)') 
    plt.ylabel(r'Base uMF $\mathrm{[kg m^{-2} s^{-1}]}$') 
    
    ax.legend(frameon=False)
    
    #fig.set_size_inches(4.5, 2)

    plt.savefig('%sbase_massflux_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()
    #exit()

def read_cape_cin(exp_label):

    # Your filename
    nc_file    = 'cape_cin_%s.nc'%exp_label  
    # Dataset is the class behavior to open the file
    # and create an instance of the ncCDF4 class
    nc_v = Dataset(nc_file, 'r')    
    cape =  nc_v.variables['cape'][:,0,0]
    cin  =  nc_v.variables['cin' ][:,0,0]
    time =  nc_v.variables['time']

    tu = "days  since 2014-01-01T00:00:00 +04:00:00"
    tc = "gregorian"

    data_cin = num2pydate(time[:],units=tu,calendar=tc) 

    return data_cin,cape,cin

def massflux_scatter(exp,days,exp_label,exp_label_cape,exp_label2,lim):

####################################
    k=0


    fig,ax =fown.figure_sam(0.4)
   
    tke_all_pbl  =[] 

    mass_all=[] 

    #All experiment have the same time, the first day of 2014 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    for ex in exp:


        #Read the cin and cape nc files  calculated in cape.py
        #data_cin,cape,cin=read_cape_cin(exp_label_cape[k])
        #data_c = down.data_to_reference(data_cin)

        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        di,df= down.data_n(idi,idf,data)


        size= ex.data.shape[0]
        tam = df-di 

        cape          =   np.zeros(tam)
        cin           =   np.zeros(tam)
        bowen         =   np.zeros(tam)

        rho           =   np.zeros(tam)
        tkeint        =   np.zeros(tam)
        tkeint_pbl    =   np.zeros(tam)
        tkeint_cloud  =   np.zeros(tam)
        tkeint_cloud2 =   np.zeros(tam)

        mtke          =   np.zeros(tam)
        itke          =   np.zeros(tam)
        mmc           =   np.zeros(tam)

        indexant=0
        levi    =80

        j=0

        for i in range(di,df):

            cape[j]=ex.CAPE[i] 
            cin[j] =ex.CIN[i] 

            bowen[j]=ex.SHF[i]/(ex.LHF[i]+1.0e-5)

            indexmin  =   np.argmin(ex.TVFLUX[i][0:100]) 

            mtke[j]   =   np.max(ex.TKE[i][20:150]) 
            itke[j]   =   ex.TKE[i][indexmin]
            rho[j]    =   ex.RHO[i][indexmin]

            mmc[j]    =   np.max(ex.MCUP[i][0:150]) 

            mini      =   np.min(ex.TVFLUX[i][0:100]) 
            
            if (cin[j]==0):

                cin[j]=1.0

            # to prevent to chosse a index that not exist
            # went the flux in to small, zero
            if(mini>-0.001 and mini<0.001):

                indexmin=indexant

            tkeint_pbl[j]   = 1.0/(ex.z[indexmin]-ex.z[0])  *integrate.simps(ex.TKE[i][0:indexmin],ex.z[0:indexmin])

            indexant=indexmin

            j=j+1


        #line,col =color_hours(k)

        #massflux      =0.3*0.4*rho*np.sqrt(tkeint)      *np.exp(-cin[di:df]/tkeint)
        massflux_pbl  =0.4*rho*np.sqrt(tkeint_pbl)*np.exp(-(cin-1)/tkeint_pbl)
        #massflux_cloud=0.4*0.4*rho*np.sqrt(tkeint_cloud)*np.exp(-cin[di:df]/tkeint_cloud)

        #massflux      =0.4*rho*np.sqrt(itke)  *np.exp(-1.0/(4.0*tkeint))
        #massflux_pbl  =0.4*rho*np.sqrt(itke)  *np.exp(-1.0/tkeint_pbl)
        #massflux_cloud=0.4*rho*np.sqrt(itke)  *np.exp(-1.0/(9.0*tkeint_cloud))


        #line=[1,0]
        line,col =color_hours(k)


        maxx   =   np.argmax(mmc) 
        fin    =   len(cape) 


        #variables= [cape,cin,tkeint_pbl,bowen]
        variables= [massflux_pbl]
        degress= 2

        #fig = plt.figure()
        #ax  = plt.axes()
        #l2= ax.plot(mmc , massflux_pbl   ,linewidth=1.4)
        #plt.show()


        print(exp_label[k]) 
        for var in variables:

            fig = plt.figure()
            ax  = plt.axes()

            model1=np.poly1d(np.polyfit(var[0:maxx],mmc[0:maxx],degress))
            model2=np.poly1d(np.polyfit(var[maxx+1:fin],mmc[maxx+1:fin],degress))
            polyline1 = np.linspace(var[0], var[maxx], 40)
            polyline2 = np.linspace(var[maxx+1], var[fin-1], 40)
            l1= ax.plot( polyline1 ,model1(polyline1)              ,label='%s'%(exp_label2[k]),color='blue'  ,linewidth=1.4)
            l2= ax.plot( polyline2 ,model2(polyline2)              ,label='%s'%(exp_label2[k]),color='blue'  ,linewidth=1.4)


            r1=polifit(var[0:maxx],mmc[0:maxx],degress)
            r2=polifit(var[maxx+1:fin],mmc[maxx+1:fin],degress)

            r=(r1+r2)/2.0

            print(r1,r2)
            print(r)

            l1= ax.plot( var[0:maxx] ,mmc[0:maxx]                  ,label='%s'%(exp_label2[k]),color='red'  ,linewidth=1.4)
            l1= ax.plot( var[maxx+1:fin] ,mmc[maxx+1:fin]          ,label='%s'%(exp_label2[k]),color='red'  ,linewidth=1.4)

            plt.show()

        #fig2 = plt.figure()
        #ax2  = plt.axes()
        #l2= ax2.plot( mmc     ,var  ,label='%s'%(exp_label2[k]),color='green',linewidth=1.4)

        #fig3 = plt.figure()
        #ax3  = plt.axes()
        #l3= ax3.plot( mmc     ,var  ,label='%s'%(exp_label2[k]),color='blue' ,linewidth=1.4)

        #fig4 = plt.figure()
        #ax4  = plt.axes()
        #l4= ax4.plot( mmc     ,var  ,label='%s'%(exp_label2[k]),color='blue' ,linewidth=1.4)



        #ax.axis( [0,0.3,0,0.3])
        #ax2.axis( [0,0.3,0,0.3])
        #ax3.axis( [0,0.3,0,0.3])
        #ax4.axis( [0,0.3,0,0.3])

        k=k+1

    
    # plt.show()


def massflux_correlation(exp,days,exp_label,exp_label2,lim):

####################################
    k=0

    fig,ax =fown.figure_sam(0.4)

    for ex in exp:

####################################
        #All experiment have the same time, the first day of 2021 
        idi1     = dt.datetime(days[k][6], 1 ,1, days[k][0] ) 
        idf1     = dt.datetime(days[k][6], 1 ,1, 14,00)

        idi2     = dt.datetime(days[k][6], 1 ,1, 14,00) 
        idf2     = dt.datetime(days[k][6], 1 ,1, days[k][1])

        mflux1,cor1=integration_var(idi1,idf1,ex,exp_label,exp_label2,lim)
        mflux2,cor2=integration_var(idi2,idf2,ex,exp_label,exp_label2,lim)

        #massflux    = np.concatenate(mflux1, mflux2)
        cor=(cor1+cor2)/2.0


        line,col =color_hours(k)

        line=[1,0]
        l1= ax.plot( ex.data    ,massflux[1]       ,label='%s'%(exp_label2[k]),color=col,linewidth=1.4,alpha=1.0,dashes=line,marker='')

        #line=[1,0]
        #l1= ax.plot( data[di:df]     ,massflux2       ,label='%s'%(exp_label2[k]),color=col,linewidth=1.4,alpha=1.0,dashes=line,marker='')

        #line=[1,1]
        #l1=ax.plot( data[di:df]      ,mmf         ,label='',color=col,linewidth=1.0,alpha=0.8,dashes=line,marker='')

        plt.show()

    return cor

def integration_var(idi,idf,ex,exp_label,exp_label2,lim):
                             
   
    #To make one reference time for al experiment 
    #Where the hour and seconds are really important
    #print ex.data[0]

    data    = down.data_to_reference(ex.data)

    di,df   = down.data_n(idi,idf,data)

    size    = data.shape[0]
    tam     = df-di 

    rho          =   np.zeros(tam)
    tkeint_pbl   =   np.zeros(tam)
    mmf          =   np.zeros(tam)
    mtke         =   np.zeros(tam)
    itke         =   np.zeros(tam)

    indexant=0

    cape=ex.CAPE[:] 
    cin =ex.CIN[:] 


    j=0
    for i in range(di,df):

        #to searh the minimum buoyancy flux until 2000 m
        indexmin  =   np.argmin(ex.TVFLUX[i][0:40]) 
        mini      =   np.min(ex.TVFLUX[i][0:40]) 

        #to maximum mass flux until 2000 m, base
        mmf[j]    =   np.max(ex.MCUP[i][0:100]) 

        #maximum tke
        mtke[j]   =   np.max(ex.TKE[i][20:150]) 

        # tke at the base
        itke[j]   =   ex.TKE[i][indexmin]

        rho[j]    =   ex.RHO[i][indexmin]

        # to prevent to chosse a index that not exist
        # went the flux in to small, zero
        if(mini>-0.001 and mini<0.001):

            indexmin=indexant

        indexant=indexmin

        #mean of tke at the pbl
        tkeint_pbl[j]   = 1.0/(ex.z[indexmin]-ex.z[0])  *integrate.simps(ex.TKE[i][0:indexmin],ex.z[0:indexmin])

        j+=1


    massflux1      = 0.4*rho*np.sqrt(tkeint_pbl)*np.exp(-(cin[di:df]+1)/tkeint_pbl)

    massflux2      = 0.4*rho*np.sqrt(mtke)*np.exp(-(cin[di:df]+1)/mtke)

    massflux3      = 0.4*rho*np.sqrt(itke)*np.exp(-(cin[di:df]+1)/itke)

    massflux4      = 0.4*rho*np.sqrt(tkeint_pbl)*np.exp(-(cin[di:df])/tkeint_pbl)

    corr1, st1 = pearsonr(massflux1, mmf)
    corr2, st2 = pearsonr(massflux2, mmf)
    corr3, st2 = pearsonr(massflux3, mmf)
    corr4, st2 = pearsonr(massflux4, mmf)
    corr5, st5 = pearsonr(ex.MCUP[di:df,indexmin], ex.CLD[di:df,indexmin])

    #fig = plt.figure()
    ###New axis
    #ax  = plt.axes()
    #plt.plot(ex.MCUP[di:df,indexmin], ex.CLD[di:df,indexmin])

    #plt.show()

    corr=[ corr1,corr2,corr3,corr4,corr5]

    massflux=[ massflux1, massflux2, massflux3, massflux4]


    return massflux,corr 



def massflux_int(exp,days,exp_label,exp_label_cape,exp_label2,lim):

####################################
    k=0


    fig,ax =fown.figure_sam(0.4)
    tke_all_pbl  =[] 

    #All experiment have the same time, the first day of 2014 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    for ex in exp:


        #Read the cin and cape nc files  calculated in cape.py
        #data_cin,cape,cin=read_cape_cin(exp_label_cape[k])
        #data_c = down.data_to_reference(data_cin)

        cape=ex.CAPE[:] 
        cin =ex.CIN[:] 

        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        #print ex.data[0]

        day0=0
        data   = down.data_to_reference(ex.data,day0,days[0][6])

        size= ex.data.shape[0]

        tam = ex.TKE.shape[0]

        maxmc=[]

        rho           =   np.zeros(tam)
        tkeint_pbl    =   np.zeros(tam)

        mtke          =   np.zeros(tam)
        itke          =   np.zeros(tam)

        indexant=0

        levi=80#tam


        for i in range(0,tam):

            indexmin  =   np.argmin(ex.TVFLUX[i][0:100]) 

            mini      =   np.min(ex.TVFLUX[i][0:100]) 
            mmc       =   np.max(ex.MCUP[i][0:150]) 

            #mtke[i]   =   np.max(ex.TKE[i][20:150]) 
            mtke[i]   =   np.max(ex.TKE[i][20:150]) 
            itke[i]   =   ex.TKE[i][indexmin]

            rho[i]    =   ex.RHO[i][indexmin]

            #if(cin[i]<1.00):

            #    cin[i]=1.00

            # to prevent to chosse a index that not exist
            # went the flux in to small, zero
            if(mini>-0.001 and mini<0.001):

                indexmin=indexant

            indexant=indexmin
            maxmc.append(mmc)

            tkeint_pbl[i]   = 1.0/(ex.z[indexmin]-ex.z[0])  *integrate.simps(ex.TKE[i][0:indexmin],ex.z[0:indexmin])


        line,col =color_hours(k)

        massflux_pbl  = 1.0*rho*1.0/(np.sqrt(tkeint_pbl*3.14*2.0))*np.exp(-(1.0)**2.0/(2.0*tkeint_pbl**2.0))   
        #massflux_pbl  = 0.4*rho*np.sqrt(tkeint_pbl)*np.exp(-(cin+1.5)/tkeint_pbl)   

        line=[1,0]
        l1= ax.plot( data     ,massflux_pbl       ,label='%s'%(exp_label2[k]),color=col,linewidth=1.4,alpha=1.0,dashes=line,marker='')


        line=[2,1]
        l1=ax.plot( data      ,maxmc         ,label='',color=col,linewidth=1.0,alpha=0.8,dashes=line,marker='')

        k=k+1

    
    lines1 =  fig.gca().get_lines()

    lshape= len(lines1)

    #legend1 = ax.legend([lines1[i] for i in range(1,lshape+1,2)],['LES_%s'%(lines1[i].get_label()) for i in range(0,lshape,2)], loc=2,frameon=False)

    #fig.gca().add_artist(legend1)

    #Ticks of the axisss
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)

    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    ax.axis( [idi,idf,lim[0], lim[1]])

    di     = dt.datetime(2014, 1 ,1, 9) 
    #ax.text(di,0.12,r'uMf=$0.4\rho\sqrt{\overline{tke}}e^{-(cin+1)/overline{tke}}$')
    ax.text(di,0.11,r'$uMf=0.4\rho\sqrt{\overline{TKE}}e^{-(cin+1)/\overline{TKE}}$',fontsize=10)

    #plt.title(r'$\mathrm{uMf=0.4\rho\sqrt{e}e^{-(cin+1)/e}}$')

    ax.set_xlabel(r'Hours LT (UTC-4)') 
    ax.set_ylabel(r'Massflux $\mathrm{[kg m^{-2} s^{-1}]}$') 

    ax.legend(frameon=False,loc='center left')

    plt.show()

    fig.savefig('%smassflux_tke_cin_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.close(fig)

    plt.show()

def tke_int(exp,days,exp_label,exp_label2,lim):

####################################
    k=0


    fig1,ax1 =fown.figure_sam(0.4)
    fig2,ax2 =fown.figure_sam(0.4)
    fig3,ax3 =fown.figure_sam(0.4)
   
    tke_all=[] 
    tke_all_pbl=[] 
    tke_all_cloud=[] 

    #All experiment have the same time, the first day of 2021 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    for ex in exp:

        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        #print ex.data[0]
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        ni,nf    =down.data_n(idi,idf,ex.data) 

        if exp_label2[k]=='BOMEX':
            data= data + dt.timedelta(hours=8)

        size= ex.data.shape[0]

        tam = ex.TKE.shape[0]

        tkeint        =   np.zeros(tam)
        tkeint_pbl    =   np.zeros(tam)
        tkeint_cloud  =   np.zeros(tam)
        tkeint_cloud2 =   np.zeros(tam)

        indexant=0
        for i in range(0,tam):

            indexmin        = np.argmin(ex.TVFLUX[i][0:90]) 
            mini            = np.min(ex.TVFLUX[i][0:90]) 

            if(mini>-0.001 and mini<0.001):

                indexmin=indexant

            #Way to calculate the cloud top with tlflux
            #work!
            #index           = np.argmin(ex.TLFLUX[i][:])
            #TL=ex.TLFLUX[i][:]

            #for j in range(0,len(ex.z)):

            #    if j <= index:

            #        TL[j]=-10.0 

            #indexmax       = np.where(TL>-0.001) 

            #if(indexmax[0][0]>indexmin):

            #    tkeint_cloud2[i]= integrate.simps(ex.TKE[i][indexmin:indexmax[0][0]],ex.z[indexmin:indexmax[0][0]])
            #else:
            #    tkeint_cloud2[i]= 0  
            indexant=indexmin

            
            tkeint[i]       = integrate.simps(ex.RHO[i][:]*ex.TKE[i][:],ex.z[:])

            tkeint_pbl[i]   = integrate.simps(ex.RHO[i][0:indexmin]*ex.TKE[i][0:indexmin],ex.z[0:indexmin])

        tkeint_cloud=tkeint-tkeint_pbl

        tke_all.append(tkeint[ni:nf])
        tke_all_pbl.append(tkeint_pbl[ni:nf])
        tke_all_cloud.append(tkeint_cloud[ni:nf])


        line,col =color_hours(k)

        ax1.plot( data[0:size] ,tkeint[0:size]      ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        ax2.plot( data[0:size] ,tkeint_pbl[0:size]  ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        ax3.plot( data[0:size] ,tkeint_cloud[0:size],label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')


    	#plt.plot( data[0:size]
        #,tkeint_cloud2[0:size],label='%s_cloud2'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='*')
        #plt.show()

        k=k+1

    ax1=mean(ax1,tke_all      ,data,size)
    ax2=mean(ax2,tke_all_pbl  ,data,size)
    ax3=mean(ax3,tke_all_cloud,data,size)

    #Ticks of the axisss
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)

    ax1.xaxis.set_minor_locator(locatormin)
    ax1.xaxis.set_major_locator(locatormax )

    ax2.xaxis.set_minor_locator(locatormin)
    ax2.xaxis.set_major_locator(locatormax )

    ax3.xaxis.set_minor_locator(locatormin)
    ax3.xaxis.set_major_locator(locatormax )
    
    ax1.axis( [idi,idf,lim[0][0], lim[0][1]])
    ax2.axis( [idi,idf,lim[1][0], lim[1][1]])
    ax3.axis( [idi,idf,lim[2][0], lim[2][1]])
    
    ax1.set_xlabel(r'Hours LT (UTC-4)') 
    ax1.set_ylabel(r'Integrate TKE $\mathrm{[kg m^{-1} s^{-2}]}$') 

    ax2.set_xlabel(r'Hours LT (UTC-4)') 
    ax2.set_ylabel(r'Integrate TKE PBL $\mathrm{[kg m^{-1} s^{-2}]}$') 
    il     = dt.datetime(2014, 1 ,1, 17) 
    ax2.text(il,900 , r'%s'%('e)'), fontsize=9, color='black')
    
    ax3.set_xlabel(r'Hours LT') 
    ax3.set_ylabel(r'Integrate TKE CLOUD $ \mathrm{[kg m^{-1} s^{-2}]}$') 
    
    ax1.legend(frameon=False)
    ax2.legend(frameon=False)
    ax3.legend(frameon=False)
    

    fig1.savefig('%sint_tke_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    fig2.savefig('%sint_tke_pbl_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    fig3.savefig('%sint_tke_cloud_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)


    plt.show()
    #exit()

def int_cloud(exp,days,exp_label,exp_label2,lim):

####################################
    #First day of the experiment 
    k=0

    fig,ax =fown.figure_sam(0.4)

    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    total_cloud_all=[] 

    for ex in exp:

        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        ni,nf    =down.data_n(idi,idf,ex.data) 
            
        size= ex.data.shape[0]
        
        total_cloud_all.append(ex.CLDLOW[ni:nf]*100) 
        
        line,col =color_hours(k)
        
        plt.plot( data[0:size]       ,ex.CLDLOW[0:size]*100    ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        
        k=k+1

    ax=mean(ax,total_cloud_all,data,size)

    #Ticks of the axisss
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)
    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    plt.axis( [idi,idf,lim[0], lim[1]])
    
    plt.xlabel(r'Hours LT (UTC-4)') 
    plt.ylabel(r'Total Cloud Fraction [%]') 

    
    il     = dt.datetime(2014, 1 ,1, 17) 
    ax.text(il,22 , r'%s'%('a)'), fontsize=9, color='black')
    
    ax.legend(frameon=False)
    
    plt.savefig('%stotal_cloud_all_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    return fig



def lwp(exp,days,exp_label,exp_label2,lim):
    ###############################################

    #First day of the experiment 
    k=0

    #Figure
    fig,ax =fown.figure_sam(0.4)

    #All experiment have the same time, the first day of 2021 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    lwp_all=[] 

    for ex in exp:

        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        size= ex.data.shape[0]

        if exp_label2[k]=='BOMEX':
            data= data + dt.timedelta(hours=8)

        ni,nf    =down.data_n(idi,idf,ex.data) 

        line,col =color_hours(k)
        plt.plot( data[0:size]       ,ex.LWP[0:size]    ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')

        lwp_all.append(ex.LWP[ni:nf]) 

        k=k+1

    ax=mean(ax,lwp_all,data,size)

    #Ticks of the axisss
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)
    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    
    plt.axis( [idi,idf,lim[0], lim[1]])
    #plt.xlabel(r'Date begins 01-09-2014') 
    
    plt.ylabel(r'Liquid Water Path [gm$^{-2}]$') 
    plt.xlabel(r'Hours LT (UTC-4)') 

    
    ax.legend(frameon=False)

    il     = dt.datetime(2014, 1 ,1, 17) 
    ax.text(il,30 , r'%s'%('f)'), fontsize=9, color='black')
    
    #fig.set_size_inches(8, 5)
    #fig.set_size_inches(4.5, 2)

    plt.savefig('%slwp_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    return fig
    ###############################################

def bowen(exp,days,exp_label,exp_label2,lim):

    #First day of the experiment 
    k=0

    #All experiment have the same time, the first day of 2021 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])


    fig,ax =fown.figure_sam(0.4)

    bowen_all=[]

    for ex in exp:

        size= ex.data.shape[0]
        
        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        #the experiment. day0=0, first day 1
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        ni,nf    =down.data_n(idi,idf,ex.data) 
        
        if exp_label2[k]=='BOMEX':
            data= data + dt.timedelta(hours=8)
        
        line,col =color_hours(k)
        
        plt.plot(data[0:size]       ,ex.SHF[0:size]/(ex.LHF[0:size]+0.00001)    ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        bowen_all.append(ex.SHF[ni:nf]/(ex.LHF[ni:nf]+0.00001)) 
        
        k=k+1

    ax=mean(ax,bowen_all,data,size)
    
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)
    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    
    plt.axis( [idi,idf,lim[0], lim[1]])
    
    plt.ylabel(r' Bowen ratio') 
    plt.xlabel(r'Hours LT (UTC-4)') 
    
    ax.legend(frameon=False)

    il     = dt.datetime(2014, 1 ,1, 17) 
    ax.text(il,0.3 , r'%s'%('c)'), fontsize=9, color='black')
    
    #fig.set_size_inches(4.5, 2)
    plt.savefig('%sbowen_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    return fig

def lhf(exp,days,exp_label,exp_label2,lim):

    #First day of the experiment 
    k=0

    #All experiment have the same time, the first day of 2014 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])


    fig,ax =fown.figure_sam(0.4)

    lhf_all=[]

    for ex in exp:

        size= ex.data.shape[0]
        
        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])


        ni,nf    =down.data_n(idi,idf,ex.data) 
        
        if exp_label2[k]=='BOMEX':
            data= data + dt.timedelta(hours=8)
        
        line,col =color_hours(k)
        
        plt.plot(data[0:size]       ,ex.LHF[0:size]    ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        lhf_all.append(ex.LHF[ni:nf]) 
        
        k=k+1

    ax=mean(ax,lhf_all,data,size)

    il     = dt.datetime(2014, 1 ,1, 17) 
    ax.text(il,350 , r'%s'%('b)'), fontsize=9, color='black')
    
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)
    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    
    plt.axis( [idi,idf,lim[0], lim[1]])
    
    plt.ylabel(r' Latent Heat FLux $\mathrm{ [W m^{-2}]}$') 
    plt.xlabel(r'Hours LT (UTC-4)') 
    
    ax.legend(frameon=False)

    
    #fig.set_size_inches(4.5, 2)
    plt.savefig('%slhf_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    return fig

def shf(exp,days,exp_label,exp_label2,lim):

    #First day of the experiment 
    k=0

    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    #First day of the experiment 
    k=0

    fig,ax =fown.figure_sam(0.4)

    shf_all=[]

    for ex in exp:

        size= ex.data.shape[0]

        ni,nf    =down.data_n(idi,idf,ex.data) 
        
        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])
        
        if exp_label2[k]=='BOMEX':
            data= data + dt.timedelta(hours=8)
        
        line,col =color_hours(k)
        
        plt.plot(data[0:size]       ,ex.SHF[0:size]    ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        shf_all.append(ex.SHF[ni:nf]) 
        
        k=k+1

    ax=mean(ax,shf_all,data,size)

    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)
    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    
    plt.axis( [idi,idf,lim[0], lim[1]])
    
    plt.ylabel(r' Sensible Heat FLux $\mathrm{ [W m^{-2}]}$') 
    plt.xlabel(r'Hours LT (UTC-4)') 

    il     = dt.datetime(2014, 1 ,1, 17) 
    ax.text(il,100 , r'%s'%('a)'), fontsize=9, color='black')
    
    ax.legend(frameon=False)
    
    #fig.set_size_inches(4.5, 2)
    plt.savefig('%sshf_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    return fig

def prec(exp,days,exp_label,exp_label2,lim):
    ###############################################

    #First day of the experiment 
    k=0

    #All experiment have the same time, the first day of 2014 
    idi     = dt.datetime(days[0][6], 1 ,1, days[0][0]) 
    idf     = dt.datetime(days[0][6], 1 ,1, days[0][1])

    #First day of the experiment 
    k=0

    fig,ax =fown.figure_sam(0.4)

    prec_all=[] 

    for ex in exp:
        
        #if(k==0):
        #    ax.plot([],[],color='white',label='Large     ')
        #if(k==2):
        #    ax.plot([],[],color='white',label='Medium     ')
        #if(k==4):
        #    ax.plot([],[],color='white',label='Small      ')
        
        size= ex.data.shape[0]
        
        #To make one reference time for al experiment 
        #Where the hour and seconds are really important
        #day0=to control de first day of the begins of
        #the experiment. day0=0, first day 1
        day0=0
        data = down.data_to_reference(ex.data,day0,days[0][6])

        ni,nf    =down.data_n(idi,idf,ex.data) 
        
        if exp_label2[k]=='BOMEX':
            data= data + dt.timedelta(hours=8)
        
        line,col =color_hours(k)
        
        #mmh-1
        plt.plot( data[0:size]       ,ex.PREC[0:size]*1.0/24.0    ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        
        ax.axhline(0.5, color='r')
        
        prec_all.append(ex.PREC[ni:nf]*1.0/24.0) 
        
        #mmday-1
        #plt.plot( data[0:size]       ,ex.PREC[0:size]    ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        #ax.axhline(y=5,color='r')
        
        k=k+1

    #to plot the mean 
    ax= mean(ax,prec_all,data,size) 
    
    #Ticks of the axisss
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)

    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    
    #plt.axis( [idi,idf,0.00, 10.0])
    plt.xlabel(r'Hours LT (UTC-4)') 
    plt.ylabel(r'Precipitation $\mathrm{ [mmh^{-1}]}$') 
    #plt.axis( [idi,idf,0.00, 0.1])
    plt.axis( [idi,idf,lim[0], lim[1]])
    ax.legend(frameon=False, )

    #plt.axis( [idi,idf,0.00, 0.15])
    #plt.ylabel(r'Precipitation $\mathrm{ [mmday^{-1}]}$') 
    
    #fig.set_size_inches(8, 5)
    #fig.set_size_inches(4.5, 2)

    plt.savefig('%sprec_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    return fig

def mean(ax,var_all,data,size):

    mean_prec   =   np.mean(var_all,axis=0)

    #ax.plot( data[0:size]       ,mean_prec[0:size]   ,color='black',linewidth=1.0,alpha=1.0,dashes=[1,0],label='Average',marker='')

    #cis  =   (mean_prec[0:size]*0.90, mean_prec[0:size]*1.10)

    #ax.fill_between(data[0:size],cis[0],cis[1],alpha=0.25,color='black')# **kw)

    return ax
        

def color_hours1(hour): 
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
          color='red'
    elif  hour==3:
          #line=[3, 1]
          line=[1,0]
          color='g'
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



def color_hours_diff(hour):

    line=[1,0]
    color='k'

    if    hour==0:
          line=[1,0]
          color='blue'
    if    hour==1:
          line=[1,0]
          color='black'
    if    hour==2:
          line=[1,0]
          color='orange'
    elif  hour==3:
          line=[1,0]
          color='g'
    elif  hour==4:
          line=[2, 1]
          color='blue'
    elif  hour==5:
          line=[2,1]
          color='black'
    elif  hour==6:
          line=[2,1]
          color='orange'
    elif  hour==7:
          line=[2,1]
          color='g'
    elif  hour==8:
          line=[2,1,5,3]
          color='tab:purple'
    elif  hour==9:
          line=[4,2,1,2]
          color='y'
    elif  hour==10:
          line=[1,2,4,2]
          color='c'

    return line,color


