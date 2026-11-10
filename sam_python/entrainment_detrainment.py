import  numpy       as     np

#Python standard library datetime  module
import  datetime    as dt

import  matplotlib          as mpl

import  matplotlib.pyplot   as plt

#from    files_direction import file_fig 

#metpy package 
from    metpy.units import units

from    metpy.constants import *

import  sam_python.data_own    as down

import  sam_python.figure_own  as fown

import  sam_python.diurnal  as diu

import  sam_python.default_values as df

import importlib

import subprocess, sys

import xarray as xr

#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/sam_python/', shell = True, executable="/bin/bash")

#used the user parameter to plot(plotparameter.py) if para:
#pars=__import__('source.Parameters_default',globals())
pars=importlib.import_module('.Parameters_default','sam_python',)

#def diurnal_entrainment_detrainment_sam(exp,explabel=[],explabel2=[],alt=[],lim=[],var_to=[],color=[],xlabel=[],ylabel=[],leg_loc=[],diurnal=[],show=True,fractional=False): 
#
#
#    k=0
#
#    for ex in exp:
#
#        print("___________________")
#        print("__%s__"%(ex.name))
#        print("Entrainment & Detrainment")
#        print("___________________")
#
#        E,D=entrainment_detrainment(ex)
#
#        #to test the function
#        #E=[ex.MCUP[:],ex.MCUP[:]]
#        #D=[ex.MCUP[:],ex.MCUP[:]]
#
#        #Its no necessary to calculate de height
#        z=ex.z
#
#        name=ex.name
#
#        date=ex.date
#
#        variables=[E[0],E[1],D[0],D[1]]
#
#        lim,alt,var_to,color,explabel1,explabel2,leg_loc,diurnal,show=df.default_values(exp,variables,lim,alt,var_to,color,explabel,explabel2,leg_loc,diurnal,show,k)
#
#        j=0 
#        data=E[0]*var_to[k][j]
#        ch=diurnal[k][j][0]
#
#        fig1,ax1 = diu.main_plot_diurnal_new(ex,data,ch,date,z,alt[k][j],lim[k][j],color[k][j],name+'_entrainment',xlabel[k][j],ylabel[k][j],explabel1[k][j],explabel2[k][j],leg_loc[k][j],diurnal[k][j])
#
#
#        j=1
#        data=D[0]*var_to[k][j]
#        ch=diurnal[k][j][0]
#
#        fig2,ax2 = diu.main_plot_diurnal_new(ex,data,ch,date,z,alt[k][j],lim[k][j],color[k][j],name+'_detrainment',xlabel[k][j],ylabel[k][j],explabel1[k][j],explabel2[k][j],leg_loc[k][j],diurnal[k][j])
#
#
#        if fractional:
#
#            j=2 
#            data=E[1]*var_to[k][j]
#            ch=diurnal[k][j][0]
#            fig3,ax3 = diu.main_plot_diurnal_new(ex,data,ch,date,z,alt[k][j],lim[k][j],color[k][j],name+'_fractional_entrainment',xlabel[k][j],ylabel[k][j],explabel1[k][j],explabel2[k][j],leg_loc[k][j],diurnal[k][j])
#
#            j=3 
#            data=D[1]*var_to[k][j]
#            ch=diurnal[k][j][0]
#            fig4,ax4 = diu.main_plot_diurnal_new(ex,data,ch,date,z,alt[k][j],lim[k][j],color[k][j],name+'_fractional_detrainment',xlabel[k][j],ylabel[k][j],explabel1[k][j],explabel2[k][j],leg_loc[k][j],diurnal[k][j])
#
#
#
#        k+=1
#
#
#    if show:
#
#        plt.show()
#
#    plt.close('all')
#
#    return 

def diurnal_entrainment_xr(exp,variables,date,name=[],explabel1=[],explabel2=[],alt=[],lim=[],var_to=[],color=[],leg_loc=[],diurnal=[],show=[],load=[]): 

    k=0
    for ex in exp:

        print("___________________")
        print("__%s__"%(ex.name))
        print("___________________")

        #date_format = '%Y%m%d%H%M%S'
        date_format = '%Y-%m-%dT%H'
        datei=dt.datetime.strptime(date[k][0], date_format)
        datef=dt.datetime.strptime(date[k][1], date_format)

        time1 = np.datetime64(date[k][0]) 
        time2 = np.datetime64(date[k][1])

        ni,nf=down.data_n(time1,time2,ex.time.values) 

        tovar= ex.sel(time=slice(ex.time[ni],ex.time[nf]))

        #if name:
        name    =   str(ex.name.values)#+'_'+dates[0]

        print("_les__%s__"%(name))


        #to test the function
        #E=[tovar.MCUP[:].values,tovar.MCUP[:].values]
        #D=[tovar.MCUP[:].values,tovar.MCUP[:].values]

        #Its no necessary to calculate de height
        z=tovar.z.values

        if load:

            ED = xr.open_dataset('Entrainment_Detrainmnet_%s.nc'%(name), engine='netcdf4')

        else:

            E,D=entrainment_detrainment(tovar)

            ED=xr.Dataset(
            {
                "Ent": (["time","z"], E[0]),
                "FracE": (["time","z"], E[1]),
                "Det": (["time","z"], D[0]),
                "FracD": (["time","z"], D[1]),
                "name":'entrainment_detrainment'
            },
            coords={
                "time": tovar.time.values,
                "z": z,
            },
            )

            ED.to_netcdf('Entrainment_Detrainmnet_%s.nc'%(name))
        

        #variables=['Ent','FracE','Det','FracD']

        j=0
        for var in variables:

            limu,altu,var_tou,coloru,explabel1u,explabel2u,leg_locu,diurnalu,showu,lineu=df.default_values_sam_diurnal(ED,var,z,lim,alt,var_to,color,explabel1,explabel2,leg_loc,diurnal,show,k,j)

            print("___________________")
            print("%s"%(var))
            print("___________________")

            data=ED[var][:,:]*var_tou

            hours=[datei,datef]

            name2='les_'+var+'_'+name

            
            #lines per hour
            ch=diurnalu[0]

            try:
                #hour to plot
                htp=diurnalu[2]
            except:
                htp=[]

            figs,axis = diu.main_plot_diurnal_new(data,ch,htp,hours,z,altu,limu,coloru,name2,[explabel1u,explabel2u],leg_locu,diurnalu[1])

            j+=1

        k+=1

    if show:

        plt.show()

    plt.close('all')

    return 



def entrainment_detrainment(ex):
        
#Fuction to calcate Detraiment and Entraiment.
#core=True_ cor variables  False= Updraft variable .

    #idi     = dt.datetime(days[k][7],days[k][4],days[k][2],days[k][0]) 
    #idf     = dt.datetime(days[k][6],days[k][5],days[k][3],days[k][1])

    #ni,nf= down.data_n(idi,idf,ex.date[:])

    #MFCOR "Mass flux in core averaged over the whole domain" 
    wm      =   ex.COR[:,:]*ex.WCOR[:,:]+(1.0-ex.COR[:,:])*ex.WENV[:,:]
    wu      =   ex.SUP[:,:]*ex.WSUP[:,:]+(1.0-ex.SUP[:,:])*ex.WENV[:,:]

    #Mass flux calculation
    #Core
    mcor    =   ex.COR[:,:]*ex.RHO[:,:]*(ex.WCOR[:,:]-wm[:,:]) 
    #Upd
    mupd    =   ex.SUP[:,:]*ex.RHO[:,:]*(ex.WSUP[:,:]-wu[:,:]) 

    #moist potential temperature  
    #variables to calculate E e D

    var_cor  = ex.TLSUP
    flux_cor = ex.MFTLCLDA

    var_upd  = ex.TLSUP
    flux_upd = ex.MFTLSUPA

    #oveline{rho'w'Tl'}
    var_env  = ex.TLENV
    flux_env = ex.MFTLENVA

    ###var_cor  = ex.QTSUP
    ###flux_cor = ex.MFQTCLDA
    ###var_env  = ex.QTENV
    ###flux_env = ex.MFQTENVA

    i=0
    j=0

    #print(ex.time[0].total.seconds)
    delta_t     = (ex.time[i+1]-ex.time[i]).dt.total_seconds()
    delta_z     = (ex.z[j+1]-ex.z[j])

    #Entraiment core
    E =np.zeros((len(ex.time),len(ex.z)))
    #fractional Entraiment 
    E_frac=np.zeros((len(ex.time),len(ex.z)))

    #Entraiment CORE
    D=np.zeros((len(ex.time),len(ex.z)))
    #Detraiment UPDRAFT
    D_frac=np.zeros((len(ex.time),len(ex.z)))

    #core=True
    core=False

    for i in range(0,len(ex.time)-1):
        for j in range(0,len(ex.z)-1): 

            if core:
                #Varible to calculate teh derivative
                #CORE
                var_cor_diff = (var_cor[i,j+1]-var_cor[i,j])/delta_z
                #Flux variable to calculate teh derivative
                flux_cor_diff= (flux_cor[i,j+1]-flux_cor[i,j])/delta_z
                #Flux variable to calculate the time derivative
                var_cor_diff_t=(var_cor[i+1,j]-var_cor[i,j])/delta_t

                #Cloud core fraction
                a_cor_diff_t  = (ex.COR[i+1,j]-ex.COR[i,j])/delta_t

                #Entraiment CORE
                E[i,j]  = 1.0/(var_env[i,j]-var_cor[i,j])*\
                        (   mcor[i,j]*var_cor_diff   +   \
                            ex.COR[i,j]*flux_cor_diff  +   \
                            ex.RHO[i,j]*ex.COR[i,j]*var_cor_diff_t  \
                        )

                #Detraiment CORE
                D[i,j]  = E[i,j]-(mcor[i,j+1]-mcor[i,j])/delta_z \
                    -ex.RHO[i,j]*a_cor_diff_t   

            else:

                #UPDRAFT
                var_upd_diff = (var_upd[i,j+1]-var_upd[i,j])/delta_z

                #Flux variable to calculate the derivative
                flux_upd_diff= (flux_upd[i,j+1]-flux_upd[i,j])/delta_z
                #Flux variable to calculate teh derivative
                #UPDRAFT
                var_upd_diff_t=(var_upd[i+1,j]-var_upd[i,j])/delta_t

                #Cloud updraft fraction
                a_upd_diff_t      = (ex.SUP[i+1,j]-ex.SUP[i,j])/delta_t
                #Entraiment UPDRAFT

                E[i,j]  = 1.0/(var_env[i,j]-var_upd[i,j])*\
                        (   mupd[i,j]*var_upd_diff   +   \
                            ex.SUP[i,j]*flux_upd_diff  +   \
                            ex.RHO[i,j]*ex.SUP[i,j]*var_upd_diff_t  \
                        )

                #Detraiment UPDRAFT
                D[i,j]  = E[i,j]-(mupd[i,j+1]-mupd[i,j])/delta_z \
                        -ex.RHO[i,j]*a_upd_diff_t   

                #De      = (En -(ex.MCUP[i,j+1]-ex.MCUP[i,j])/delta_z \
                #        -ex.RHO[i,j]*a_upd_diff_t)  

            #ENVIONROMENT 
            #var_env_diff_t= (var_env[i+1,j]-var_env[i,j])/delta_t
            #var_env_diff  = (var_env[i,j+1]-var_env[i,j])/delta_z
            #flux_env_diff = (flux_env[i,j+1]-flux_env[i,j])/delta_z

            #Fractional entraiment rate UPDRAFT (km-1)
            E_frac[i,j]=E[i,j]*1000.0/(ex.MCUP[i,j]+1e-10)

            #Fractional detraiment rate UPDRAFT (km-1)
            D_frac[i,j]=D[i,j]*1000.0/(ex.MCUP[i,j]+1e-10)

            if (D_frac[i,j]<1 or D_frac[i,j]>20.0 or D_frac[i,j]==np.nan):
                D_frac[i,j]=0.0

            if (E_frac[i,j]<0 or E_frac[i,j]>4.0 or E_frac[i,j]==np.nan):
                E_frac[i,j]=0.0


    return [E,E_frac],[D,D_frac]

def entrainment_detrainment_old(ex):
        
    #moist potential temperature  
    var_upd  = ex.TLSUP
    flux_upd = ex.MFTLSUPA
    
    #oveline{rho'w'Tl'}
    var_env  = ex.TLENV
    flux_env = ex.MFTLENVA
    
    ###var_cor  = ex.QTSUP
    ###flux_cor = ex.MFQTCLDA
    ###var_env  = ex.QTENV
    ###flux_env = ex.MFQTENVA
    
    i=0
    j=0
    
    delta_t     = (ex.date[i+1]-ex.date[i]).total_seconds()
    delta_z     = (ex.z[j+1]-ex.z[j])
    
    #Entraiment UPDRAFT
    E_upd=np.zeros((len(ex.date),len(ex.z)))
    
    #Detraiment UPDRAFT
    D_upd=np.zeros((len(ex.date),len(ex.z)))
    
    for i in range(0,len(ex.date)-1):
    
        for j in range(0,len(ex.z)-1): 
    
            #Varible to calculate teh derivative
            #UPDRAFT
            var_upd_diff = (var_upd[i,j+1]-var_upd[i,j])/delta_z
            #ENVIONROMENT 
            var_env_diff = (var_env[i,j+1]-var_env[i,j])/delta_z
            #Flux variable to calculate teh derivative
            #UPDRAFT
            flux_upd_diff= (flux_upd[i,j+1]-flux_upd[i,j])/delta_z
            #ENVIONROMENT 
            flux_env_diff= (flux_env[i,j+1]-flux_env[i,j])/delta_z
    
            #Flux variable to calculate teh derivative
            #UPDRAFT
            var_upd_diff_t=(var_upd[i+1,j]-var_upd[i,j])/delta_t
            #ENVIONROMENT 
            var_env_diff_t=(var_env[i+1,j]-var_env[i,j])/delta_t
    
            #Cloud updraft fraction
            a_upd_diff_t      = (ex.SUP[i+1,j]-ex.SUP[i,j])/delta_t
    
            #Entraiment UPDRAFT
            E_upd[i,j]  = 1.0/(var_env[i,j]-var_upd[i,j])*\
                    (   ex.MCUP[i,j]*var_upd_diff   +   \
                        ex.SUP[i,j]*flux_upd_diff  +   \
                        ex.RHO[i,j]*ex.SUP[i,j]*var_upd_diff_t  \
                    )
    
            #Detraiment UPDRAFT
            D_upd[i,j]  = E_upd[i,j]-(ex.MCUP[i,j+1]-ex.MCUP[i,j])/delta_z \
                    -ex.RHO[i,j]*a_upd_diff_t   
    

    return E_upd,D_upd

def mass_flux_parametrization(exp,days,lim,color,explabel,show): 

    print("__________")
    print("Mass_flux parametrization")
    print("__________")

    fig =[]
    k   =0
    nfig=0

    for ex in exp:

        #Inicial hour
        hi=days[k][0]    
        #Final hour
        hf=days[k][1] 
        			#ano		#mes	#dia		#Hour
        idi     = dt.datetime(days[k][7],days[k][4],days[k][2],days[k][0]) 
        idf     = dt.datetime(days[k][6],days[k][5],days[k][3],days[k][1])
        
        ni,nf= down.data_n(idi,idf,ex.date[:])
        
        # QCFLUX = liquid water 
        # QCFLUX = liquid water flux
        # THETAL =TL= liquid water static energy =  liquid water potential temperature 
        # TLFLUX = FLux liquid water static energy =  liquid water potential temperature 
        #MFCOR "Mass flux in core averaged over the whole domain" 
        
        wm    =   ex.COR[:,:]*ex.WCOR[:,:]+(1.0-ex.COR[:,:])*ex.WENV[:,:]
        wu    =   ex.SUP[:,:]*ex.WSUP[:,:]+(1.0-ex.SUP[:,:])*ex.WENV[:,:]
        
        mass_c=   ex.COR[:,:]*ex.RHO[:,:]*(ex.WCOR[:,:]-wm[:,:]) 
        mass_u=   ex.SUP[:,:]*ex.RHO[:,:]*(ex.WSUP[:,:]-wu[:,:]) 
        
        
        #Multiply by cp*rho to w/m^2, heat equation 
        
        cpd = dry_air_spec_heat_press
        
        thetalflux_cm= cpd*ex.RHO[:,:]*mass_c*(ex.TLCOR[:,:]-ex.TLENV[:,:])
        qlflux_cm   = cpd*ex.RHO[:,:]*mass_c[:,:]*(ex.QCCOR[:,:]-ex.QCENV[:,:])
        
        thetalflux_c= cpd*ex.RHO[:,:]*ex.MC[:,:]*(ex.TLCOR[:,:]-ex.TLENV[:,:])
        qlflux_c    = cpd*ex.RHO[:,:]*ex.MC[:,:]*(ex.QCCOR[:,:]-ex.QCENV[:,:])
        
        
        thetalflux_um  = cpd*ex.RHO[:,:]*mass_u*( ex.TLSUP[:,:]-ex.TLENV[:,:])
        qlflux_um      = cpd*ex.RHO[:,:]*mass_u[:,:]  *(ex.QCSUP[:,:]-ex.QCENV[:,:])
        
        thetalflux_u  = cpd*ex.RHO[:,:]*ex.MCUP[:,:]  *(ex.TLSUP[:,:]-ex.TLENV[:,:])
        qlflux_u      = cpd*ex.RHO[:,:]*ex.MCUP[:,:]  *(ex.QCSUP[:,:]-ex.QCENV[:,:])
        
        
        #To plot 
        fn  = plt.figure(nfig)
        ax1 = plt.axes()
        #ax2 = ax.twiny() 
        
        fn=fown.splot_own_ax_label(fn,ax1,thetalflux_cm[ni:nf,:] ,ex.z[:]/1000.0,'magenta'  ,   label=r'$\mathrm{\overline{w^{\prime}\theta_l^{\prime}}^{cm}}$', shade=False)
        fn=fown.splot_own_ax_label(fn,ax1,thetalflux_um[ni:nf,:] ,ex.z[:]/1000.0,'red'      ,   label=r'$\mathrm{\overline{w^{\prime}\theta_l^{\prime}}^{um}}$', shade=False)
        fn=fown.splot_own_ax_label(fn,ax1,thetalflux_c[ni:nf,:]  ,ex.z[:]/1000.0,'blue'     ,   label=r'$\mathrm{\overline{w^{\prime}\theta_l^{\prime}}^{ca}}$', shade=False)
        fn=fown.splot_own_ax_label(fn,ax1,thetalflux_u[ni:nf,:]  ,ex.z[:]/1000.0,'green'    ,   label=r'$\mathrm{\overline{w^{\prime}\theta_l^{\prime}}^{ua}}$',shade=False)
        fn=fown.splot_own_ax_label(fn,ax1,ex.TLFLUX[ni:nf,:]     ,ex.z[:]/1000.0,'black'    ,   label=r'$\mathrm{\overline{w^{\prime}\theta_l^{\prime}}^{LES}}$',shade=False)
        
        fn2  = plt.figure(nfig+1)
        ax2 = plt.axes()
        
        fn2=fown.splot_own_ax_label(fn2,ax2,qlflux_cm[ni:nf,:]     ,ex.z[:]/1000.0,'magenta',   label=r'$\mathrm{\overline{w^{\prime}q_l^{\prime}}^{cm}}$',shade=False)
        fn2=fown.splot_own_ax_label(fn2,ax2,qlflux_um[ni:nf,:]     ,ex.z[:]/1000.0,'red'   ,    label=r'$\mathrm{\overline{w^{\prime}q_l^{\prime}}^{um}}$',shade=False)
        fn2=fown.splot_own_ax_label(fn2,ax2,qlflux_c[ni:nf,:]     ,ex.z[:]/1000.0,'blue'   ,    label=r'$\mathrm{\overline{w^{\prime}q_l^{\prime}}^{ca}}$',shade=False)
        fn2=fown.splot_own_ax_label(fn2,ax2,qlflux_u[ni:nf,:]     ,ex.z[:]/1000.0,'green'  ,    label=r'$\mathrm{\overline{w^{\prime}q_l^{\prime}}^{ua}}$',shade=False)
        fn2=fown.splot_own_ax_label(fn2,ax2,ex.QCFLUX[ni:nf,:]    ,ex.z[:]/1000.0,'black'  ,    label=r'$\mathrm{\overline{w^{\prime}q_l^{\prime}}}^{LES}$',shade=False)
        
        
        #plt.legend( frameon=False,loc='upper left')
        ax1.legend(frameon=False,loc='lower left')
        ax2.legend(frameon=False,loc='lower right')
        
        lim=[(-30,30)]
        
        #plt.axis([lim[k][0],lim[k][1],0,lmax])
        ax1.axis([lim[k][0],0,0,lmax])
        ax2.axis([0,lim[k][1],0,lmax])
        
        ax1.set_ylabel(r'z [km]') 
        ax2.set_ylabel(r'z [km]') 
        
        #plt.xlabel(r'Mass flux approximation') 
        ax1.set_xlabel(r'$\mathrm{\overline{w^{\prime}\theta_l^{\prime}}}$') 
        ax2.set_xlabel(r'$\mathrm{\overline{w^{\prime}q_l^{\prime}}}$') 
        
        fn.savefig( '%smassflux_thetal_t_%s.pdf'%(file_fig,explabel[k]), format='pdf', dpi=1000)
        fn.savefig( '%smassflux_ql_t_%s.pdf'%(file_fig,explabel[k]), format='pdf', dpi=1000)
        
        fig.append(fn)
        
        k=k+1
        
        nfig=nfig+1

    if show:
        plt.show()

    plt.close('all')


    return fig 


def diurnal_entrainment_calc(exp,days,lim_e,lim_d,color,explabel,explabel2,show): 

    print("__________")
    print("DIUNAL ENTRAINMENT_DETRAINMENT")
    print("__________")

    fig=[]
    
    k=0

    nfig=0

    for ex in exp:

        #Inicial hour
        hi=days[k][0]    
        #Final hour
        hf=days[k][1] 

        idi     = dt.datetime(days[k][7],days[k][4],days[k][2],days[k][0]) 
        idf     = dt.datetime(days[k][6],days[k][5],days[k][3],days[k][1])
        
        ni,nf= down.data_n(idi,idf,ex.date[:])

        
        #moist potential temperature  
        var_upd  = ex.TLSUP
        flux_upd = ex.MFTLSUPA
        
        #oveline{rho'w'Tl'}
        var_env  = ex.TLENV
        flux_env = ex.MFTLENVA
        
        ###var_cor  = ex.QTSUP
        ###flux_cor = ex.MFQTCLDA
        ###var_env  = ex.QTENV
        ###flux_env = ex.MFQTENVA
        
        i=0
        j=0
        
        delta_t     = (ex.date[i+1]-ex.date[i]).total_seconds()
        delta_z     = (ex.z[j+1]-ex.z[j])
        
        #Entraiment UPDRAFT
        E_upd=np.zeros((len(ex.date),len(ex.z)))
        
        #Detraiment UPDRAFT
        D_upd=np.zeros((len(ex.date),len(ex.z)))
        
        for i in range(0,len(ex.date)-1):
            for j in range(0,len(ex.z)-1): 
        
                #Varible to calculate teh derivative
                #UPDRAFT
                var_upd_diff = (var_upd[i,j+1]-var_upd[i,j])/delta_z
                #ENVIONROMENT 
                var_env_diff = (var_env[i,j+1]-var_env[i,j])/delta_z
        
                #Flux variable to calculate teh derivative
                #UPDRAFT
                flux_upd_diff= (flux_upd[i,j+1]-flux_upd[i,j])/delta_z
                #ENVIONROMENT 
                flux_env_diff= (flux_env[i,j+1]-flux_env[i,j])/delta_z
        
                #Flux variable to calculate teh derivative
                #UPDRAFT
                var_upd_diff_t=(var_upd[i+1,j]-var_upd[i,j])/delta_t
                #ENVIONROMENT 
                var_env_diff_t=(var_env[i+1,j]-var_env[i,j])/delta_t
        
                #Cloud updraft fraction
                a_upd_diff_t      = (ex.SUP[i+1,j]-ex.SUP[i,j])/delta_t
        
                #Entraiment UPDRAFT
                E_upd[i,j]  = 1.0/(var_env[i,j]-var_upd[i,j])*\
                        (   ex.MCUP[i,j]*var_upd_diff   +   \
                            ex.SUP[i,j]*flux_upd_diff  +   \
                            ex.RHO[i,j]*ex.SUP[i,j]*var_upd_diff_t  \
                        )
        
                #Detraiment UPDRAFT
                D_upd[i,j]  = E_upd[i,j]-(ex.MCUP[i,j+1]-ex.MCUP[i,j])/delta_z \
                        -ex.RHO[i,j]*a_upd_diff_t   
        
        ##interval hour
        ch      = 2
        
        meanvar_e,hour = diurnal_main(ex.date,ex.z[:]/1000.0,E_upd,idi,idf,k,hi,hf,ch)
        meanvar_d,hour = diurnal_main(ex.date,ex.z[:]/1000.0,D_upd,idi,idf,k,hi,hf,ch)
        
        #To plot 
        #@fn  = plt.figure(nfig)
        #@ax1 = plt.axes()
        #@
        #@fn2 = plt.figure(nfig+1)
        #@ax2 = plt.axes()

        #def label_plots(legend,explabel,xlabel): 
        fig1,ax1=label_plots(leg_loc,xlabel,ylabel,explabel1,explabel2)
        #def label_plots(legend,explabel,xlabel): 
        fig2,ax2=label_plots(leg_loc,xlabel,ylabel,explabel1,explabel2)
        jj=0
        
        for j in range(0,hf-hi+ch,ch):
        
            line,col =diu.color_hours(hour[j])
        
            ax1.plot(meanvar_e[j,:] ,ex.z[:]/1000.0,label='%d:00'%(hour[j]),color=col,linewidth=1.5,alpha=1.0,dashes=line)
        
            ax2.plot(meanvar_d[j,:] ,ex.z[:]/1000.0,label='%d:00'%(hour[j]),color=col,linewidth=1.5,alpha=1.0,dashes=line)
        
            jj=jj+1
        
        #fn=fown.splot_own_ax_label(fn,ax1,E_upd[ni:nf,:]     ,ex.z[:]/1000.0,'green'    ,   label=r'$\mathrm{E_{updraft}}$',shade=True)
        #fn2=fown.splot_own_ax_label(fn2,ax2,D_upd[ni:nf,:]   ,ex.z[:]/1000.0,'green'    ,   label=r'$\mathrm{D_{updraft}}$',shade=True)

        label=['mean',False]
        
        fn=fown.splot_own_ax_label(fn,ax1,E_upd[ni:nf,:]     ,ex.z[:]/1000.0,color    ,   label=label)
        fn2=fown.splot_own_ax_label(fn2,ax2,D_upd[ni:nf,:]   ,ex.z[:]/1000.0,color    ,   label=label)


         #def label_plots(legend,explabel,xlabel): 
        #fig,ax=label_plots(leg_loc,xlabel,ylabel,explabel1,explabel2)
        #ax1.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
        #ax2.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
        #
        #ax1.text(lim_e[k][0], 0.2, r' %s'%(explabel2[k]), fontsize=12, color='black')
        #ax2.text(lim_d[k][0], 0.2, r' %s'%(explabel2[k]), fontsize=12, color='black')
        #
        #if(explabel[k]=='march_10_core' or explabel[k]=='oct_05_core'):
        #       	ax1.set_ylabel(r'z [km]') 
        #       	ax2.set_ylabel(r'z [km]') 
        ##if(legen_on==True):
        #if( explabel[k]=='oct_01_core' or explabel[k]=='composite'):
        #        ax1.legend(frameon=False,loc='upper right')
        #        ax2.legend(frameon=False,loc='upper right')
        #
        #ax1.axis([lim_e[k][0],lim_e[k][1],0,lmax])
        #ax2.axis([lim_d[k][0],lim_d[k][1],0,lmax])
        
        #ax1.set_ylabel(r'z [km]') 
        #ax2.set_ylabel(r'z [km]') 
        #plt.xlabel(r'Mass flux approximation') 
        #ax1.set_xlabel(r'E') 
        #ax2.set_xlabel(r'D') 

        #plt.axis([lim[0],lim[1],alt[0],alt[1]])
        
        label="%s"%(name)


        fn.savefig( '%s/diurnal_entrainment_%s.pdf'%(file_fig,label), format='pdf',bbox_inches='tight', dpi=1000)
        fn2.savefig('%s/diurnal_detrainment_%s.pdf'%(file_fig,label), format='pdf',bbox_inches='tight', dpi=1000)
        
        k+=1
        
    if show:
        plt.show()

    plt.close('all')

    return fig 

def diurnal_fractional_entrainment_calc(exp,days,lim_e,lim_d,color,explabel,explabel2,show): 

    print("__________")
    print("DIURNAL ENTRAINMENT_DETRAINMENT")
    print("__________")

    fig=[]
    
    k=0

    nfig=0

    for ex in exp:

        #Inicial hour
        hi=days[k][0]    
        #Final hour
        hf=days[k][1] 
        
        idi     = dt.datetime(days[k][7],days[k][4],days[k][2],days[k][0]) 
        idf     = dt.datetime(days[k][6],days[k][5],days[k][3],days[k][1])
        
        ni,nf= down.data_n(idi,idf,ex.date[:])
        
        core=False
        E,D,Ef,Df   =entraiment_detrainment_cal(ex,days,core)
        
        ch      = 1
        meanvar_e,hour = diurnal_main(ex.date,ex.z[:]/1000.0,Ef,idi,idf,k,hi,hf,ch)
        meanvar_d,hour = diurnal_main(ex.date,ex.z[:]/1000.0,Df,idi,idf,k,hi,hf,ch)
        
        #To plot 
        fn  = plt.figure(nfig)
        ax1 = plt.axes()
        
        fn2 = plt.figure(nfig+1)
        ax2 = plt.axes()
        
        jj=0
        
        for j in range(0,hf-hi+ch,ch):
        
            line,col =diu.color_hours(hour[j])
        
            ax1.plot(meanvar_e[j,:] ,ex.z[:]/1000.0,label='%d:00'%(hour[j]),color=col,linewidth=1.5,alpha=1.0,dashes=line)
        
            ax2.plot(meanvar_d[j,:] ,ex.z[:]/1000.0,label='%d:00'%(hour[j]),color=col,linewidth=1.5,alpha=1.0,dashes=line)
        
            jj=jj+1
        
        
        fn=fown.splot_own_ax_label(fn  ,ax1,Ef[ni:nf,:]   ,ex.z[:]/1000.0,color[k]    ,   label=r'',shade=True)
        fn2=fown.splot_own_ax_label(fn2,ax2,Df[ni:nf,:]   ,ex.z[:]/1000.0,color[k]    ,   label=r'',shade=True)
        
        
        #ax1.legend(frameon=False,loc='upper right')
        #ax2.legend(frameon=False,loc='upper right')
        
        ax1.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
        ax2.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
        
        ax1.text(lim_e[k][0], 0.2, r' %s'%(explabel2[k]), fontsize=12, color='black')
        ax2.text(lim_d[k][0], 0.2, r' %s'%(explabel2[k]), fontsize=12, color='black')
        
        ax1.axis([lim_e[k][0],lim_e[k][1],0,lmax])
        ax2.axis([lim_d[k][0],lim_d[k][1],0,lmax])
        
        #ax1.set_ylabel(r'z [km]') 
        #ax2.set_ylabel(r'z [km]') 
        
        if(explabel[k]=='march_10_core' or explabel[k]=='oct_05_core'):
               	ax1.set_ylabel(r'z [km]') 
               	ax2.set_ylabel(r'z [km]') 
        
        if( explabel[k]=='oct_01_core' or explabel[k]=='composite'):
                ax1.legend(frameon=False,loc='upper right')
                ax2.legend(frameon=False,loc='upper right')
        
        ax1.axis([lim_e[k][0],lim_e[k][1],0,lmax])
        ax2.axis([lim_d[k][0],lim_d[k][1],0,lmax])
        
        fn.savefig( '%sdiurnalfrac_entrainment_%s.pdf'%(file_fig,explabel[k]), format='pdf',bbox_inches='tight', dpi=1000)
        fn2.savefig('%sdiurnalfrac_detrainment_%s.pdf'%(file_fig,explabel[k]), format='pdf',bbox_inches='tight', dpi=1000)
        
        fig.append(fn)
        
        k=k+1
        
        nfig=nfig+1+1
        
        if show:
            plt.show()


    plt.close('all')

    return fig 

def entraiment_detrainment_cal(ex,days,core): 
#Fuction to calcate Detraiment and Entraiment.
#core=True_ cor variables  False= Updraft variable .

    #idi     = dt.datetime(days[k][7],days[k][4],days[k][2],days[k][0]) 
    #idf     = dt.datetime(days[k][6],days[k][5],days[k][3],days[k][1])

    #ni,nf= down.data_n(idi,idf,ex.date[:])

    #MFCOR "Mass flux in core averaged over the whole domain" 
    wm      =   ex.COR[:,:]*ex.WCOR[:,:]+(1.0-ex.COR[:,:])*ex.WENV[:,:]
    wu      =   ex.SUP[:,:]*ex.WSUP[:,:]+(1.0-ex.SUP[:,:])*ex.WENV[:,:]

    #Mass flux calculation
    #Core
    mcor    =   ex.COR[:,:]*ex.RHO[:,:]*(ex.WCOR[:,:]-wm[:,:]) 
    #Upd
    mupd    =   ex.SUP[:,:]*ex.RHO[:,:]*(ex.WSUP[:,:]-wu[:,:]) 

    #moist potential temperature  
    #variables to calculate E e D

    var_cor  = ex.TLSUP
    flux_cor = ex.MFTLCLDA

    var_upd  = ex.TLSUP
    flux_upd = ex.MFTLSUPA

    #oveline{rho'w'Tl'}
    var_env  = ex.TLENV
    flux_env = ex.MFTLENVA

    ###var_cor  = ex.QTSUP
    ###flux_cor = ex.MFQTCLDA
    ###var_env  = ex.QTENV
    ###flux_env = ex.MFQTENVA

    i=0
    j=0

    delta_t     = (ex.date[i+1]-ex.date[i]).total_seconds()
    delta_z     = (ex.z[j+1]-ex.z[j])

    #Entraiment core
    E =np.zeros((len(ex.date),len(ex.z)))
    #fractional Entraiment 
    E_frac=np.zeros((len(ex.date),len(ex.z)))

    #Entraiment CORE
    D=np.zeros((len(ex.date),len(ex.z)))
    #Detraiment UPDRAFT
    D_frac=np.zeros((len(ex.date),len(ex.z)))

    for i in range(0,len(ex.date)-1):
        for j in range(0,len(ex.z)-1): 

            if core:
                #Varible to calculate teh derivative
                #CORE
                var_cor_diff = (var_cor[i,j+1]-var_cor[i,j])/delta_z
                #Flux variable to calculate teh derivative
                flux_cor_diff= (flux_cor[i,j+1]-flux_cor[i,j])/delta_z
                #Flux variable to calculate the time derivative
                var_cor_diff_t=(var_cor[i+1,j]-var_cor[i,j])/delta_t

                #Cloud core fraction
                a_cor_diff_t  = (ex.COR[i+1,j]-ex.COR[i,j])/delta_t

                #Entraiment CORE
                E[i,j]  = 1.0/(var_env[i,j]-var_cor[i,j])*\
                        (   mcor[i,j]*var_cor_diff   +   \
                            ex.COR[i,j]*flux_cor_diff  +   \
                            ex.RHO[i,j]*ex.COR[i,j]*var_cor_diff_t  \
                        )

                #Detraiment CORE
                D[i,j]  = E[i,j]-(mcor[i,j+1]-mcor[i,j])/delta_z \
                    -ex.RHO[i,j]*a_cor_diff_t   

            else:

                #UPDRAFT
                var_upd_diff = (var_upd[i,j+1]-var_upd[i,j])/delta_z

                #Flux variable to calculate the derivative
                flux_upd_diff= (flux_upd[i,j+1]-flux_upd[i,j])/delta_z
                #Flux variable to calculate teh derivative
                #UPDRAFT
                var_upd_diff_t=(var_upd[i+1,j]-var_upd[i,j])/delta_t

                #Cloud updraft fraction
                a_upd_diff_t      = (ex.SUP[i+1,j]-ex.SUP[i,j])/delta_t
                #Entraiment UPDRAFT

                E[i,j]  = 1.0/(var_env[i,j]-var_upd[i,j])*\
                        (   mupd[i,j]*var_upd_diff   +   \
                            ex.SUP[i,j]*flux_upd_diff  +   \
                            ex.RHO[i,j]*ex.SUP[i,j]*var_upd_diff_t  \
                        )

                #Detraiment UPDRAFT
                D[i,j]  = E[i,j]-(mupd[i,j+1]-mupd[i,j])/delta_z \
                        -ex.RHO[i,j]*a_upd_diff_t   

                #De      = (En -(ex.MCUP[i,j+1]-ex.MCUP[i,j])/delta_z \
                #        -ex.RHO[i,j]*a_upd_diff_t)  

            #ENVIONROMENT 
            #var_env_diff_t= (var_env[i+1,j]-var_env[i,j])/delta_t
            #var_env_diff  = (var_env[i,j+1]-var_env[i,j])/delta_z
            #flux_env_diff = (flux_env[i,j+1]-flux_env[i,j])/delta_z

            #Fractional entraiment rate UPDRAFT (km-1)
            E_frac[i,j]=E[i,j]*1000.0/(ex.MCUP[i,j]+1e-10)

            #Fractional detraiment rate UPDRAFT (km-1)
            D_frac[i,j]=D[i,j]*1000.0/(ex.MCUP[i,j]+1e-10)

            if (D_frac[i,j]<1 or D_frac[i,j]>20.0 or D_frac[i,j]==np.nan):
                D_frac[i,j]=0.0

            if (E_frac[i,j]<0 or E_frac[i,j]>4.0 or E_frac[i,j]==np.nan):
                E_frac[i,j]=0.0

    return E,D,E_frac,D_frac 

def entrainment_calc(exp,days,lim,color,explabel,show): 

    print("__________")
    print("ENTRAINMENT_DETRAINMENT")
    print("__________")


    fig=[]
    
    k=0

    nfig=0

    for ex in exp:

        #Inicial hour
        hi=days[k][0]    
        #Final hour
        hf=days[k][1] 
        
        idi     = dt.datetime(days[k][7],days[k][4],days[k][2],days[k][0]) 
        idf     = dt.datetime(days[k][6],days[k][5],days[k][3],days[k][1])
        
        
        ni,nf= down.data_n(idi,idf,ex.date[:])
        
        #MFCOR "Mass flux in core averaged over the whole domain" 
        
        wm      =   ex.COR[:,:]*ex.WCOR[:,:]+(1.0-ex.COR[:,:])*ex.WENV[:,:]
        wu      =   ex.SUP[:,:]*ex.WSUP[:,:]+(1.0-ex.SUP[:,:])*ex.WENV[:,:]
        
        #Mass flux calculation
        #Core
        mcor    =   ex.COR[:,:]*ex.RHO[:,:]*(ex.WCOR[:,:]-wm[:,:]) 
        #Upd
        mupd    =   ex.SUP[:,:]*ex.RHO[:,:]*(ex.WSUP[:,:]-wu[:,:]) 
        
        #moist potential temperature  
        #variables to calculate E e D
        
        var_cor  = ex.TLSUP
        flux_cor = ex.MFTLCLDA
        
        var_upd  = ex.TLSUP
        flux_upd = ex.MFTLSUPA
        
        #oveline{rho'w'Tl'}
        var_env  = ex.TLENV
        flux_env = ex.MFTLENVA
        
        ###var_cor  = ex.QTSUP
        ###flux_cor = ex.MFQTCLDA
        
        ###var_env  = ex.QTENV
        ###flux_env = ex.MFQTENVA
        
        i=0
        j=0
        
        delta_t     = (ex.date[i+1]-ex.date[i]).total_seconds()
        delta_z     = (ex.z[j+1]-ex.z[j])
        
        #Entraiment core
        E_cor=np.zeros((len(ex.date),len(ex.z)))
        #Entraiment UPDRAFT
        E_upd=np.zeros((len(ex.date),len(ex.z)))
        
        #Entraiment CORE
        D_cor=np.zeros((len(ex.date),len(ex.z)))
        #Detraiment UPDRAFT
        D_upd=np.zeros((len(ex.date),len(ex.z)))
        
        D2_cor=np.zeros((len(ex.date),len(ex.z)))
        D2_upd=np.zeros((len(ex.date),len(ex.z)))
        
        for i in range(0,len(ex.date)-1):
            for j in range(0,len(ex.z)-1): 
        
        
                #Varible to calculate teh derivative
                #CORE
                var_cor_diff = (var_cor[i,j+1]-var_cor[i,j])/delta_z
                #UPDRAFT
                var_upd_diff = (var_upd[i,j+1]-var_upd[i,j])/delta_z
                #ENVIONROMENT 
                var_env_diff = (var_env[i,j+1]-var_env[i,j])/delta_z
        
                #Flux variable to calculate teh derivative
                #CORE
                flux_cor_diff= (flux_cor[i,j+1]-flux_cor[i,j])/delta_z
                #UPDRAFT
                flux_upd_diff= (flux_upd[i,j+1]-flux_upd[i,j])/delta_z
                #ENVIONROMENT 
                flux_env_diff= (flux_env[i,j+1]-flux_env[i,j])/delta_z
        
                #Flux variable to calculate teh derivative
                #CORE
                var_cor_diff_t=(var_cor[i+1,j]-var_cor[i,j])/delta_t
                #UPDRAFT
                var_upd_diff_t=(var_upd[i+1,j]-var_upd[i,j])/delta_t
                #ENVIONROMENT 
                var_env_diff_t=(var_env[i+1,j]-var_env[i,j])/delta_t
        
        
                #Cloud core fraction
                a_cor_diff_t      = (ex.COR[i+1,j]-ex.COR[i,j])/delta_t
                #Cloud updraft fraction
                a_upd_diff_t      = (ex.SUP[i+1,j]-ex.SUP[i,j])/delta_t
        
        
                #Entraiment CORE
                E_cor[i,j]  = 1.0/(var_env[i,j]-var_cor[i,j])*\
                        (   mcor[i,j]*var_cor_diff   +   \
                            ex.COR[i,j]*flux_cor_diff  +   \
        
                            ex.RHO[i,j]*ex.COR[i,j]*var_cor_diff_t  \
                        )
        
                #Entraiment UPDRAFT
                E_upd[i,j]  = 1.0/(var_env[i,j]-var_upd[i,j])*\
                        (   mupd[i,j]*var_upd_diff   +   \
                            ex.SUP[i,j]*flux_upd_diff  +   \
                            ex.RHO[i,j]*ex.SUP[i,j]*var_upd_diff_t  \
                        )
        
                #Detraiment CORE
                D_cor[i,j]  = E_cor[i,j]-(mcor[i,j+1]-mcor[i,j])/delta_z \
                        -ex.RHO[i,j]*a_cor_diff_t   
        
                #Detraiment UPDRAFT
                D_upd[i,j]  = E_upd[i,j]-(mupd[i,j+1]-mupd[i,j])/delta_z \
                        -ex.RHO[i,j]*a_upd_diff_t   
        
        
                #D2[i,j]  = E[i,j]-(mass_u[i,j+1]-ex.MCUP[i,j])/delta_z \
                #         -ex.RHO[i,j]*a_diff_t   
        
                #D2[i,j]  = 1.0/(var_env[i,j]-var_cor[i,j])*\
                #        (   mass_c[i,j]*var_env_diff        -   \
                #            (1-ex.SUP[i,j])*flux_env_diff   -   \
        
                #            ex.RHO[i,j]*(1-ex.SUP[i,j])*var_env_diff_t  \
                #        )
        
        #To plot 
        fn  = plt.figure(nfig)
        ax1 = plt.axes()
        
        fn2 = plt.figure(nfig+1)
        ax2 = plt.axes()
        #ax2 = ax.twiny() 
        
        fn=fown.splot_own_ax_label(fn,ax1,E_cor[ni:nf,:]     ,ex.z[:]/1000.0,'red'     ,   label=r'$\mathrm{E_{cor}}$',shade=False)
        fn=fown.splot_own_ax_label(fn,ax1,E_upd[ni:nf,:]     ,ex.z[:]/1000.0,'blue'    ,   label=r'$\mathrm{E_{updraft}}$',shade=False)
        
        fn2=fown.splot_own_ax_label(fn2,ax2,D_cor[ni:nf,:]   ,ex.z[:]/1000.0,'red'       ,   label=r'$\mathrm{D_{cor}}$',shade=False)
        fn2=fown.splot_own_ax_label(fn2,ax2,D_upd[ni:nf,:]   ,ex.z[:]/1000.0,'blue'      ,   label=r'$\mathrm{D_{updraft}}$',shade=False)
        
        ax1.legend(frameon=False,loc='upper right')
        ax2.legend(frameon=False,loc='upper right')
        
        ax1.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
        ax2.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
        
        
        lim=[(0,1e-4)]
        
        #plt.axis([lim[k][0],lim[k][1],0,lmax])
        ax1.axis([lim[k][0],lim[k][1],0,lmax])
        
        lim=[(0,3e-4)]
        ax2.axis([lim[k][0],lim[k][1],0,lmax])
        
        ax1.set_ylabel(r'z [km]') 
        ax2.set_ylabel(r'z [km]') 
        
        
        plt.show()
        
        #plt.xlabel(r'Mass flux approximation') 
        #ax1.set_xlabel(r'E') 
        #ax2.set_xlabel(r'D') 

        fn.savefig( '%sentrainment%s.pdf'%(file_fig,explabel[k]), format='pdf',bbox_inches='tight', dpi=1000)
        fn2.savefig('%sdetrainment%s.pdf'%(file_fig,explabel[k]), format='pdf',bbox_inches='tight', dpi=1000)

        fig.append(fn)

        k=k+1

        nfig=nfig+1

    if show:
        plt.show()

    plt.close('all')

    return fig 

def diurnal_main(data,z,var,idi,idf,k,hi,hf,ch): 

    ni,nf   = down.data_n(idi,idf,data)

    #number of levels
    nl      = z.shape[0]

    #Lengh of the time array to search
    ndtp        =   len(data) 

    #Hour array
    #+ch to reach the final hour in the loop
    hour    = np.zeros(hf-hi+ch)

    #Sum variable to the mean 
    varsum  = np.zeros([hf-hi+ch,nl])

    meanvar = np.zeros([hf-hi+ch,nl])

    #var     = np.zeros([nl])
    meanvar = np.zeros([hf-hi+ch,nl])

    #Number of  time thar variable was sum 
    cont    = np.zeros(hf-hi+ch)
    

    #nf+1 because for does arrive to n+1, but  n its necessary
    for i in range(ni,nf+1):
    
        for j in range(0,hf-hi+ch,ch):

            if int(data[i].hour)==j+hi: 

                hour[j]     =   j+hi

                varsum[j,:] =   varsum[j,:]+var[i,:]

                cont[j]     =   cont[j]+1


    for j in range(0,hf-hi+ch,ch):
        
        meanvar[j,:] = varsum[j,:]/cont[j]


    return meanvar,hour


def diurnal_function(time,variable): 


    #Number of hour
    ndh     = 24
    #Hour array
    hour    = np.zeros(ndh)
    #Sum variable to the mean 
    varsum   = np.zeros(ndh)
    #Number of  time thar variable was sum 
    cont    = np.zeros(ndh)

    
    #Lengh of the time array to search
    ndtp    = len(time) 
    
    for i in range(0,ndtp):
    
        for j in range(0,ndh):
    
            if int(time[i].hour)==j : 
    
                hour[j]=j
                varsum[j]=varsum[j]+variable[i]
                cont[j]=cont[j]+1

    
    meanvar = varsum/cont

    return meanvar,hour 

def diurnal_function_exp(time,variable): 


    #Number of hour
    ndh     = 24
#Hour array
    hour    = np.zeros(ndh)
    #Sum variable to the mean 
    varsum   = np.zeros(ndh)
    #Number of  time thar variable was sum 
    cont    = np.zeros(ndh)
    
    #Lengh of the time array to search
    ndtp    = len(time) 

    #defaul time
    timebefore=dt.datetime(2000,1,1,0,0)
    
    for i in range(0,ndtp):
    
        for j in range(0,ndh):
    
            #to fund in an hour 
            if int(time[i].hour)==j: 

                hour[j]=j

                #to found in the half of an hour on time  
                if int(time[i].minute)<30: 

                    #to no stay in the same hour 
                    if int(time[i].hour)!=timebefore.hour: 

                        varsum[j]=varsum[j]+variable[i]
                        cont[j]=cont[j]+1

                        timebefore=time[i] 

                        continue

    meanvar = varsum/cont

    return meanvar,hour 

def mean_days(exp,days,lim_fe,lim_fd,lim_e,lim_d,color,explabel,explabel2,show): 

    print("__________")
    print("ENTRAINMENT_DETRAINMENT MEAN")
    print("__________")

    fig=[]
    
    nfig=0
    k=0
    ch=1

    hi  =  days[0][0]
    hf  =  days[0][1]+1

    meanE,meanD,meanEf,meanDf,mean_E,mean_D,mean_Ef,mean_Df,datatomE,datatomD,datatomEf,datatomDf,hour= \
    diurnal_mean_days(exp,days,ch,hi,hf) 

    #To plot 
    fn  = plt.figure(nfig)
    ax1 = plt.axes()

    fn2 = plt.figure(nfig+1)
    ax2 = plt.axes()

    fn3 = plt.figure(nfig+2)
    ax3 = plt.axes()

    fn4 = plt.figure(nfig+3)
    ax4 = plt.axes()


    jj=0

    for j in range(0,hf-hi,ch):

        line,col =diu.color_hours(hour[j])

        ax1.plot(meanEf[j,:],exp[k].z[:]/1000.0,label='%d:00'%(hour[j]),color=col,linewidth=1.5,alpha=1.0,dashes=line)
        ax2.plot(meanDf[j,:],exp[k].z[:]/1000.0,label='%d:00'%(hour[j]),color=col,linewidth=1.5,alpha=1.0,dashes=line)
        ax3.plot(meanE[j,:] ,exp[k].z[:]/1000.0,label='%d:00'%(hour[j]),color=col,linewidth=1.5,alpha=1.0,dashes=line)
        ax4.plot(meanD[j,:] ,exp[k].z[:]/1000.0,label='%d:00'%(hour[j]),color=col,linewidth=1.5,alpha=1.0,dashes=line)

        jj=jj+1


    fn =    fown.splot_own_ax_label(fn ,ax1,datatomEf   ,exp[k].z[:]/1000.0,color[k]    ,   label=r'',shade=True)
    fn2=    fown.splot_own_ax_label(fn2,ax2,datatomDf   ,exp[k].z[:]/1000.0,color[k]    ,   label=r'',shade=True)
    fn3=    fown.splot_own_ax_label(fn3,ax3,datatomE    ,exp[k].z[:]/1000.0,color[k]    ,   label=r'',shade=True)
    fn4=    fown.splot_own_ax_label(fn4,ax4,datatomD    ,exp[k].z[:]/1000.0,color[k]    ,   label=r'',shade=True)

    #ax1.legend(frameon=False,loc='upper right')
    #ax2.legend(frameon=False,loc='upper right')

    ax1.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax2.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax3.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax4.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

    ax1.text(lim_fe[k][0], 0.2, r' %s'%(explabel2[k]), fontsize=12, color='black')
    ax2.text(lim_fd[k][0], 0.2, r' %s'%(explabel2[k]), fontsize=12, color='black')
    ax3.text( lim_e[k][0], 0.2, r' %s'%(explabel2[k]), fontsize=12, color='black')
    ax4.text( lim_d[k][0], 0.2, r' %s'%(explabel2[k]), fontsize=12, color='black')

    ax1.axis([lim_fe[k][0],lim_fe[k][1],0,lmax])
    ax2.axis([lim_fd[k][0],lim_fd[k][1],0,lmax])
    ax3.axis([lim_e[k][0] ,lim_e[k][1],0,lmax])
    ax4.axis([lim_d[k][0] ,lim_d[k][1],0,lmax])

    #ax1.set_ylabel(r'z [km]') 
    #ax2.set_ylabel(r'z [km]') 
    #ax1.legend(frameon=False,loc='upper right')
    #ax2.legend(frameon=False,loc='upper right')

    fn.savefig( '%sfrac_entrainment_%s.pdf'%(file_fig,explabel[k]), format='pdf',bbox_inches='tight', dpi=1000)
    fn2.savefig('%sfrac_detrainment_%s.pdf'%(file_fig,explabel[k]), format='pdf',bbox_inches='tight', dpi=1000)
    fn3.savefig('%sentrainment_%s.pdf'%(file_fig,explabel[k]), format='pdf',bbox_inches='tight', dpi=1000)
    fn4.savefig('%sdetrainment_%s.pdf'%(file_fig,explabel[k]), format='pdf',bbox_inches='tight', dpi=1000)

    if show:
        plt.show()

    plt.close('all')

    return fig 

def diurnal_mean_days(exp,days,ch,hi,hf): 


    #counter for the days and files  
    k=0

    #number of levels
    nl      =  exp[0].z[:].shape[0]
    #nl      =  100 

    #Hour array
    hour        =   np.zeros(hf-hi)

    #Sum variable to the mean 
    Esum      =   np.zeros([(hf-hi),nl])
    Dsum      =   np.zeros([(hf-hi),nl])
    Efsum     =   np.zeros([(hf-hi),nl])
    Dfsum     =   np.zeros([(hf-hi),nl])

    meanE     =   np.zeros([(hf-hi),nl])
    meanEf    =   np.zeros([(hf-hi),nl])
    meanD     =   np.zeros([(hf-hi),nl])
    meanDf    =   np.zeros([(hf-hi),nl])

    #Number of  time thar variable was sum 
    cont        =   np.zeros((hf-hi))

    for ex in exp:

        idi     = dt.datetime(days[k][7],days[k][4],days[k][2],days[k][0]) 
        idf     = dt.datetime(days[k][6],days[k][5],days[k][3],days[k][1])
        ni,nf= down.data_n(idi,idf,ex.date[:])

        #For for the hour of the days 
        #nf+1 because for does arrive to n+1, but  n its necessary

        core=False
        E,D,E_frac,D_frac=entraiment_detrainment_cal(ex,days,core)

        for i in range(ni,nf+1):
        
            for j in range(0,hf-hi,ch):

                if int(ex.date[i].hour)==j+hi: 


                    hour[j]        =   j+hi

                    Esum[j,0:nl-1] =   Esum[j,0:nl-1]+E[i,0:nl-1]
                    Dsum[j,0:nl-1] =   Dsum[j,0:nl-1]+D[i,0:nl-1]

                    Efsum[j,0:nl-1] =  Efsum[j,0:nl-1]+E_frac[i,0:nl-1]
                    Dfsum[j,0:nl-1] =  Dfsum[j,0:nl-1]+D_frac[i,0:nl-1]

                    cont[j]         =  cont[j]+1
                #---------------------

            #---------------------

        k=k+1
        #---------------------

    #General mean, for teh complete period 
    #mean = np.mean(meanvar,axis=0) 

    nh=(hf-hi)/ch


    datatomE     =   np.zeros([nh,nl])
    datatomD     =   np.zeros([nh,nl])
    datatomEf    =   np.zeros([nh,nl])
    datatomDf    =   np.zeros([nh,nl])

    mean_E       =   np.zeros(nl)
    mean_Ef      =   np.zeros(nl)
    mean_D       =   np.zeros(nl)
    mean_Df      =   np.zeros(nl)

    jj=0

    for j in range(0,hf-hi,ch):

        meanE[j,0:nl-1]  = Esum[j,0:nl-1]/cont[j]
        meanD[j,0:nl-1]  = Dsum[j,0:nl-1]/cont[j]
        meanEf[j,0:nl-1] = Efsum[j,0:nl-1]/cont[j]
        meanDf[j,0:nl-1] = Dfsum[j,0:nl-1]/cont[j]

        mean_E[0:nl-1]   = mean_E[0:nl-1] +meanE[j,0:nl-1]
        mean_D[0:nl-1]   = mean_D[0:nl-1] +meanD[j,0:nl-1]
        mean_Ef[0:nl-1]  = mean_Ef[0:nl-1]+meanEf[j,0:nl-1]
        mean_Df[0:nl-1]  = mean_Df[0:nl-1]+meanDf[j,0:nl-1]

        datatomE[j,0:nl-1]      = meanE[j,0:nl-1]
        datatomD[j,0:nl-1]      = meanD[j,0:nl-1]
        datatomEf[j,0:nl-1]     = meanEf[j,0:nl-1]
        datatomDf[j,0:nl-1]     = meanDf[j,0:nl-1]

        jj=jj+1


    mean_E  =mean_E/(jj)
    mean_D  =mean_D/(jj)
    mean_Ef =mean_Ef/(jj)
    mean_Df =mean_Df/(jj)

    return meanE,meanD,meanEf,meanDf,mean_E,mean_D,mean_Ef,mean_Df,datatomE,datatomD,datatomEf,datatomDf,hour 

#def mean_function(ch,ni,nf,hour,data,var): 
#
#        for i in range(ni,nf+1):
#        
#            for j in range(0,hf-hi,ch):
#
#                if int(data[i].hour)==j+hi: 
#
#                    #print data[i],j+hi,cont[j],k
#
#                    hour[j]     =   j+hi
#
#                    varsum[j,0:nl-1] =   varsum[j,0:nl-1]+var[i,0:nl-1]
#
#                    cont[j]     =   cont[j]+1
#                #---------------------
#
#            #---------------------
#
#        k=k+1
#        #---------------------
#    print cont
#
#    #General mean, for teh complete period 
#    #mean = np.mean(meanvar,axis=0) 
#
#    nfig=1
#
#    nh=(hf-hi)/ch
#
#    datatom     =   np.zeros([nh,nl])
#
#    mean        =   np.zeros(nl)
#
#    jj=0
#
#    for j in range(0,hf-hi,ch):
#
#        meanvar[j,0:nl-1] = varsum[j,0:nl-1]/cont[j]
#
#        mean[0:nl-1]= mean[0:nl-1]+meanvar[j,0:nl-1]
#
#        datatom[j,0:nl-1]      = meanvar[j,0:nl-1]
#
#
#        jj=jj+1
#
#
#    mean=mean/(jj)


