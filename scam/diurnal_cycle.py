import  numpy               as np

import  datetime            as dt

import  cftime              #as cf

import  matplotlib.pyplot   as plt

import  matplotlib          as mpl

from    matplotlib.ticker   import MultipleLocator,AutoMinorLocator, FormatStrFormatter

import  matplotlib.ticker  as ticker

import nc_time_axis

import importlib

import subprocess, sys

import xarray as xr

import  scam.data_own            as down

import  scam.figure_own_xr       as fown

import  scam.campain_data        as cd

import  scam.plotparameters      as pp

import  scam.forcing_file_common as ffc

import  scam.default_values as df

import  scam.plotparameters      as pp

import  scam.forcing_file_common as ffc

#to work with date in plots 
import  matplotlib.dates as mdates

#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/scam/', shell = True, executable="/bin/bash")

#used the user parameter to plot(plotparameter.py) if para:
#pars=__import__('source.Parameters_default',globals())
pars=importlib.import_module('.Parameters_default','scam',)

def diurnal_cycle_scam(
                        exp,variables,date,
                        name=[],explabel1=[],explabel2=[],explabel3=[],
                        date0=None,plotpara=None,save=None,
                        alt=[],lim=[],var_to=[],color=[],line=[],plot_def=[],show=[],
                        diurnal=[],lev=None,
                        obs=None,date_obs=None,var_obs=None,var_to_obs=None,
                        obs2=None,date_obs2=None,var_obs2=None,var_to_obs2=None, 
                        ):

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

    agora = dt.datetime.now()
    # Formata e imprime
    data_formatada = agora.strftime(date_format)

    datenow=dt.datetime.strptime(data_formatada, date_format)

    j=0
    for var in variables:


        print("___________________")
        print("%s"%(var))
        print("___________________")

        plot_defu=df.default_plot(plot_def,j)

        size_wg = plot_defu[5][0]
        size_hf = plot_defu[5][1]
        cm_plus = plot_defu[5][2]

        if plotpara:
            tama,figsize= pp.plotsize(plotpara.width,plotpara.height, plotpara.cmm,'temporal')
            tama= plotpara.tama 
            plotpara.parameters["figure.figsize"]=figsize
            mpl.rcParams.update(plotpara.parameters)
        else:
            tama,figsize=pp.plotsize(size_wg,size_hf,cm_plus,'temporal')

        #To plot 
        fig  = plt.figure()
        ax   = plt.axes()

        k=0
        for ex in exp:

            limu,altu,var_tou,coloru,explabel1u,explabel2u,plot_defu,showu=df.default_values_1d_new(ex,var,lim,alt,var_to,color,explabel1,explabel2,plot_def,show,k,j)

            print("___________________")
            print("__%s__"%(ex.name))
            print("___________________")


            datei=dt.datetime.strptime(date[k][0], date_format)
            datef=dt.datetime.strptime(date[k][1], date_format)

            time1 = cftime.DatetimeNoLeap(

            datei.year, datei.month, datei.day, datei.hour
            )

            time2 = cftime.DatetimeNoLeap(
                datef.year, datef.month, datef.day, datef.hour
            )


            ni,nf=down.data_n(time1,time2,ex.time.values) 

            tovar= ex.sel(time=slice(ex.time[ni],ex.time[nf]))

            #if name:
            name    =   str(ex.name.values)#+'_'+dates[0]

            print("_scam__%s__"%(name))

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

            # Calculate mean diurnal cycle
            diurnal_obs = data_obs.groupby("time.hour").mean(dim="time")

            try:
                plt.plot(diurnal_obs,diurnal_obs.data[:,0,0],label='%s'%('Radar'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])
            except:                  
                plt.plot(diurnal_obs,diurnal_obs.data[:],label='%s'%('Radar'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])

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

            # Calculate mean diurnal cycle
            diurnal_obs2 = data_obs2.groupby("time.hour").mean(dim="time")

            try:
                plt.plot(diurnal_obs2,diurnal_obs2.data[:,0,0],label='%s'%('TRRM'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])
            except:                  
                plt.plot(diurnal_obs2,diurnal_obs2.data[:],label='%s'%('TRRM'),color='black',linewidth=1.5,alpha=1.0)#,dashes=line[k])
        ###########################


        fig,ax=plot_temporal_axis(fig,ax,ex,altu,limu,plot_defu,date0,data.time)

        exit()


        label="%s_%s"%(name,var)

        label=label+"_%s"%(var)

        if save:
                try: 

                    label=save[1]+"_%s"%(var)
                    plt.savefig('%s/diurnal_cycle_%s.pdf'%(pars.out_fig,label),bbox_inches='tight', format='pdf', dpi=200)
                except:
                    plt.savefig('%s/diurnal_cycle%s.pdf'%(pars.out_fig,label),bbox_inches='tight', format='pdf', dpi=200)

        j+=1

    if showu:
        plt.show()

    return fig


def plot_temporal_axis(fig,ax,ex,alt,lim,plot_def,date0,time):

    #majorFormatter = mpl.dates.DateFormatter(lim[3])
    #print(ex.time)
    #exit()

    #date_form = nc_time_axis.CFTimeFormatter(lim[3],'noleap') 
    #ax.xaxis.set_major_formatter(date_form)
    #ax.xaxis.set_major_locator(locatormax)

    #the first day of simulation if 2026-01-01
    t0_num = mdates.date2num(dt.datetime(2026, 1, 1))

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

def diurnal_hour(data,leg_loc,plotpara):

    size_wg = leg_loc[5][0]
    size_hf = leg_loc[5][1]
    cm_plus = leg_loc[5][2]

    #tama=pp.plotsize(size_wg,size_hf,cm_plus,'diurnal')

    if plotpara:
        tama,figsize= pp.plotsize(plotpara.width,plotpara.height, plotpara.cmm,'temporal')
        tama= plotpara.tama 
        plotpara.parameters["figure.figsize"]=figsize
        mpl.rcParams.update(plotpara.parameters)
    else:
        tama,figsize=pp.plotsize(size_wg,size_hf,cm_plus,'temporal')


    #To plot 
    fig  = plt.figure()
    ax   = plt.axes()

    # Calculate mean diurnal cycle
    diurnal = data.groupby("time.hour").mean(dim="time")

    #print(diurnal.data)

    #diurnal.plot(ax=ax, marker="o")

    return


def xxxxxdiurnal_cycle_scam(exp,di,df,variables,exp2=[],variables2=[],exp3=[],variables3=[],era5=[],vars_era5=[],explabel1=[],explabel2=[],lev=[],lim=[],var21=[],var22=[],var23=[],v2era5=[],color=[],leg_loc=[],diurnal=[],show=[],step_era5=False): 

    lim_copy = copy.deepcopy(lim)

    #Date to referece
    year   =2024
    month_0=1
    day_0  =1

    #date_format = '%Y%m%d%H'
    date_format = '%Y%m%d%H%M'
    di=dt.datetime.strptime(di, date_format)
    df=dt.datetime.strptime(df, date_format)

    j=0
    for var in variables:


        size_wg = leg_loc[j][5][0]
        size_hf = leg_loc[j][5][1]

        pp.plotsize(size_wg,size_hf, 0.0,'temporal')

        #To plot 
        fig     = plt.figure()
        ax      = plt.axes()

        print("___________________")
        print("______%s_____"%(var))
        print("___________________")


        if lim:

            lim_copy[j][0]=dt.datetime.strptime(lim_copy[j][0], date_format)
            lim_copy[j][1]=dt.datetime.strptime(lim_copy[j][1], date_format)


        i=0

        for ex in exp: 

            name    =   str(ex[0].name.values)
            print("__%s__"%(name))

            tall=[]
            hours=[]
            #To reference data change if change the day
            d0=-1
            day1_0=day_0

            xx=[]
            yy=[]


            var_all=[]

            k=0
            for e in ex:

                tomean = e[var]

                hours.append(tomean.Time.values)

                vmean        =   tomean.mean(dim='n_face') 

                var1plot=vmean*var21[j]

                var_all.append(vmean)

                k+=1

            mean,hours   =   diurnal_main(var_all)

            plt.plot(hours,mean,label='%s'%(explabel1[j][i]),color=color[j][i],linewidth=1.0,alpha=1.0)#,dashes=line)

            i+=1

        if exp2:
    
            #i=0
            var_all=[]
            for ex2 in exp2: 

                n0,n1   =   down.data_n(di,df,ex2.ltime.values.astype('datetime64[s]'))

                var2    =   variables2[j]

                try:
                    #var2plot=ex2[var2][n0:n1,0].values
                    var2plot=ex2[var2][n0:n1,0,0]#.values
                except:
                    var2plot=ex2[var2][n0:n1]#.values


                var2plot=   var2plot*var22[j]

                var_all.append(var2plot)
                
                mean,hours   =   diurnal_main(var_all)

                plt.plot(hours,mean,label='%s'%(explabel1[j][i]),color=color[j][i],linewidth=1.0,alpha=1.0,marker='')#,dashes=line)

                i+=1

        if exp3:

            #i=0
            var_all=[]
            for ex3 in exp3: 

                n0,n1   =   down.data_n(di,df,ex3.ltime.values.astype('datetime64[s]'))

                var3     =   variables3[j]

                try:
                    var3plot=ex3[var3][n0:n1,0,0]#.values
                except:
                    var3plot=ex3[var3][n0:n1].values

                var3plot =   var3plot*var23[j]

                var_all.append(var3plot)

                mean,hours   =   diurnal_main(var_all)

                plt.plot(hours,mean,label='%s'%(explabel1[j][i]),color=color[j][i],linewidth=1.0,alpha=1.0,marker='')#,dashes=line)

                i+=1

        if era5:

            print("era5")

            for e5 in era5: 


                if step_era5:

                    fig,ax=era5_experiment_step(fig,ax,e5,vars_era5[j],explabel1[j][i],v2era5[j],color[j][i],date=[di,df],diurnal=True)

                else:

                    fig,ax=era5_experiment(fig,ax,e5,vars_era5[j],explabel1[j][i],v2era5[j],color[j][i],date=[di,df],diurnal=True)
                    
            i+=1

        ax=label_plots(ax,leg_loc[j],'','')

        label="%s"%(explabel2[j]+'_'+var)

        fig.savefig('%s/diurnal_cicle_%s.pdf'%(pars.out_fig,label),bbox_inches='tight',dpi=200, format='pdf')

        j+=1

    if show[0]=='True':

        plt.show()

    plt.close('all')

    return 

def diurnal_main(var): 


    #number of levels
    nl      =1
    #number of hours
    nh      =24
    
    hi=0
    ch=1

    #Hour array
    #+ch to reach the final hour in the loop
    hour    = np.zeros(nh)

    #Sum variable to the mean 
    varsum  = np.zeros([nh])
    
    meanvar = np.zeros([nh])
    
    #Number of  time thar variable was sum 
    cont    = np.zeros(nh)

    #number of process used to read the files 
    nprocess=len(var)


    for k in range(0,nprocess):
        
        #Lengh of the time array to search
        try:
            ndtp    = len(var[k].Time) 
            time='Time'
        except:
            ndtp    = len(var[k].time) 
            time='time'
        
        for i in range(0,ndtp):
        
            for j in range(0,nh,ch):
    
                if int(var[k][i][time].dt.hour)==j+hi: 
    
                    hour[j]     =   j+hi
    
                    varsum[j] =   varsum[j]+var[k][i]
    
                    cont[j]     =   cont[j]+1
    
        k+=1


    for j in range(0,nh,ch):
        
        meanvar[j] = varsum[j]/cont[j]


    return meanvar,hour

def era5_experiment(fig,ax,exp,variable,explabel,var2,color,date=[],diurnal=False):
    
    #as the pytime is no a dimension is no possibeol to 
    #use, because the sel not limit with this pytime, only 
    #with time. Then is bbetter to work with time and use the utc
    # to limit.
    di=date[0] 
    df=date[1] 

    print(exp)

    if date:
        tomean = exp.sel(time=slice(di,df))

    #exit()

    #tomean['pytime']=pd.to_datetime(tomean.time)#-dt.timedelta(hours=4)
    #print(tomean.pytime)

    vlat    =   tomean[variable].mean(dim='latitude') 
    vmean   =   vlat.mean(dim='longitude') 

    hours=[]
    tplot=[]
    k=0
    #for d in tomean.pytime: 
    for d in range (0,len(tomean.time)): 
    
        #day    = tomean.pytime[d].dt
        day    = tomean.ltime[d].dt

        #print(tomean.pytime[d].values,tomean.time[k].values)

        hours.append(day)

        tplot.append(vmean[d]*var2)
    
        k+=1


    if diurnal:

        mean,hours   =   diurnal_main_2(tplot,hours)

        plt.plot(hours,mean ,label='%s'%(explabel),color=color,linewidth=1.0,alpha=1.0)#,dashes=line)

    else:

        plt.plot(hours,tplot ,label='%s'%(explabel),color=color,linewidth=1.0,alpha=1.0)#,dashes=line)
    #plt.plot(hours,vmean.values,linewidth=1.0,alpha=1.0)#,dashes=line)

    return fig,ax
