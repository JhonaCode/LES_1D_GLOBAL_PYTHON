import  numpy as np

import  cftime

import matplotlib.patches as mpatches

import  matplotlib          as mpl

import  matplotlib.pyplot   as plt

import matplotlib.ticker as ticker

# Python standard library datetime  module
import  datetime as dt  

#To work with date in plots 
import  matplotlib.dates as mdates

import  importlib

import  subprocess, sys

import  xarray as xr

import  pandas as pd

import  seaborn as sns

#import  campain_data  as cd
import  scam.data_own       as down

import  scam.figure_own_xr  as fown

import  scam.default_values as df

import  scam.forcing_file_common as ffc

#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/scam/', shell = True, executable="/bin/bash")

#used the user parameter to plot(plotparameter.py) if para:
#pars=__import__('source.Parameters_default',globals())
pars=importlib.import_module('.Parameters_default','scam',)


def two_dimensional_xr(ex,variables,date,name=[],explabel1=[],explabel2=[],alt=[],contour=[],var_to=[],color=[],leg_loc=[],show=[]):

    print("___________________")
    print("__%s__"%(ex.name))
    print("___________________")

    #date_format = '%Y%m%d%H%M%S'

    date_format = '%Y-%m-%dT%H'
    datei=dt.datetime.strptime(date[0], date_format)
    datef=dt.datetime.strptime(date[1], date_format)

    time1 = np.datetime64(date[0]) 
    time2 = np.datetime64(date[1])

    ni,nf=down.data_n(time1,time2,ex.time.values) 


    tovar= ex.sel(time=slice(ex.time[ni],ex.time[nf]))

    #if name:
    name    =   str(ex.name.values)#+'_'+dates[0]

    print("_les__%s__"%(name))

    j=0
    for var in variables:

    
        print("___________________")
        print("%s"%(var))
        print("___________________")

        #Its no necessary to calculate de height
        z=ex.z.values

        hours=[datei,datef]

        contour,alt,var_to,color,explabel1,explabel2,leg_loc,show=df.default_values_sam_2d_kj(ex,var,z,contour,alt,var_to,color,explabel1,explabel2,leg_loc,show,0,j)

        data=tovar[var][:,:]*var_to[j]


        fig_label='scam_'+name+'_'+var

        figs,axis  = fown.d2_plot_im_diff(data,z,alt[j],contour[j],color[j],[fig_label,explabel1[j],explabel2[j]],leg_loc[j],hours=hours)

        if show[j]:

            plt.show()

        j+=1

        plt.close('all')

    return 

def two_dimensional_exps_xr(exp,variables,date,name=[],explabel1=[],explabel2=[],key=[],alt=[],contour=[],var_to=[],color=[],leg_loc=[],show=[],temporal=None,save=True):

    

    k=0
    for ex in exp:

        print("___________________")
        print("__%s__"%(ex.name))
        print("___________________")

        #date_format = '%Y%m%d%H%M%S'
        date_format = '%Y-%m-%dT%H'
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

        print(ni,nf)
        j=0
        for var in variables:

        
            print("___________________")
            print("%s"%(var))
            print("___________________")


            if(j==0):
                #Pressure in Pa and T in K
                tmean=ex.T.mean(dim='time')
                pressure=ex.lev[::-1]
                z_sfc=0.0
                z=ffc.get_height_from_pres(tmean[::-1], pressure, z_sfc)

            hours=[time1,time2]

            contour,alt,var_to,color,exl1,exl2,leg_locu,show=df.default_values_sam_2d_kj(ex,var,z,contour,alt,var_to,color,explabel1,explabel2,leg_loc,show,k,j)
            
            #inverted to plot in z  no in lev
            data=tovar[var][:,::-1]*var_to[j]

            fig_label='scam_'+name+'_'+var

            figs,axis  = fown.d2_plot_im_diff(data,z,alt[j],contour[j],color[j],[fig_label,exl1,exl2],leg_locu,hours=hours)

            if temporal:

                figs,axis,axis2=fown.temporal(figs,axis,tovar,temporal[1::])

            #print(leg_locu[5][0])
            if(leg_locu[5][0]):

                #figs,axis=fown.base_top_cloud(figs,axis,ex,['gray','orange','magenta'])
                figs,axis=fown.base_top_cloud(figs,axis,ex,['gray','gray','gray'],leg_locu[5][1])


            #print(pars.out_fig,fig_label)
            #exit()

            if save:

                if not key:


                    figs.savefig('%s/vertical_2d_%s.pdf'%(pars.out_fig,fig_label),bbox_inches='tight',dpi=200, format='pdf')
                    print(key)
                    print('%s/vertical_2d_%s.pdf'%(pars.out_fig,fig_label))

                    #plt.show()
                    #exit()

                else:
                    figs.savefig('%s/vertical_2d_%s_%s.pdf'%(pars.out_fig,fig_label,key),bbox_inches='tight',dpi=200, format='pdf')
                    print('else',key)
                    print('%s/vertical_2d_%s_%s.pdf'%(pars.out_fig,fig_label,key))



            j+=1

        k+=1

    if show[0]:

        plt.show()
    
    plt.close('all')

    return 
