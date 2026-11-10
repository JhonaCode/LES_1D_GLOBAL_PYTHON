#Function to plot the cape and cin, 
#also make a skew plot 

import  metpy.calc as mpy

from    metpy.plots import add_metpy_logo, SkewT

from matplotlib.ticker import FixedLocator,NullLocator

from    metpy.units import units

# Python standard library datetime  module
import  datetime as dt  

import  numpy as np

import  matplotlib.pyplot as plt

#to work with date in plots
import  matplotlib.dates as mdates

import  matplotlib as mpl
  
import  sam_python.data_own            as down

import  sam_python.figure_own          as fown

#import  sam_python.files_direction     as fd

import  sam_python.campain_data        as cd

import  sam_python.plotparameters      as pp

# Python library to work with Netcdf4 
from    netCDF4         import Dataset

# To save the time coordinate in specific format 
from    netCDF4         import num2date, date2num

#integration 
import scipy.integrate as integrate

import importlib

import subprocess, sys

from   datetime import datetime


#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/sam_python/', shell = True, executable="/bin/bash")

#used the user parameter to plot(plotparameter.py) if para:
#pars=__import__('source.Parameters_default',globals())
pars=importlib.import_module('.Parameters_default','sam_python',)

today = dt.datetime.today()

def cape_sonde(day):

    files   =[]
    data    =[]
    sondavar=[]
    pressure=[]
    temp    =[]
    dwp     =[]
    
    cape    =[]
    cin     =[]
    
    cape2   =[]
    cin2    =[]

#

    for i in range(0,len(day)): 
    

        files.append("%s/maosondewnpnM1.b1.201409%s.cdf"%(sondafile,day[i]))

        sondavar.append(sondavarfile.ncload(files[i]))

        data.append(sondavar[i].data_p[0].tz_localize(tz = 'Etc/GMT-4')) 
    
        pres        =   units.Quantity(sondavar[i].pres[:],'hPa')
        pressure.append(pres)
    
        temperature =   units.Quantity(sondavar[i].tdry[:],'celsius')
        temp.append(temperature)
    
        dp          =   units.Quantity(sondavar[i].dp[:]  ,'celsius')
        dwp.append(dp)
    
        tp          =   mpy.parcel_profile(pres, temperature[0], dp[0]) 
    
        alt         =   units.Quantity(sondavar[i].alt[:],'m')
    
    
        k=0
        tol=5
        for h in alt:
            if h.magnitude>20000-tol and h.magnitude<20000+tol:
                altind=k
            k+=1
    
        #plt.plot(temperature,alt,'k-',tp,alt,'r-')
    
        #plt.show()
    
    
        #cap,ci      =   mpy.cape_cin(pres[1:1500], temperature[1:1500], dp[1:1500], tp[1:1500]) 
        #cap,ci      =   mpy.mixed_layer_cape_cin(pres[0:2000], temperature[0:2000], dp[0:2000]) 
        cap,ci      =   mpy.most_unstable_cape_cin(pres, temperature, dp) 
        cape.append(cap.magnitude)
        cin.append(ci.magnitude)
    
    
        cap2,ci2      =   mpy.cape_cin(pres[1:altind], temperature[1:altind], dp[1:altind], tp[1:altind]) 
        cape2.append(cap2.magnitude)
        cin2.append(ci2.magnitude)

    return  cape,cin,data


def cape_own(exp,hours,days,exp_label):


    k=0

    for ex in exp: 
    

        #Inicial hour
        hi=hours[k][0]    
        #Final hour
        hf=hours[k][1] 

        idi     = dt.datetime(2014, days[k][2] ,days[k][0], hi) 
        idf     = dt.datetime(2014, days[k][3] ,days[k][1], hf)

        ni,nf   = down.data_n(idi,idf,ex.data[:])

        #a presao tem que ser bidimensional para poder fazer os calculos 
        #sem os loops...
        pressure       		=   units.Quantity(ex.p   ,'mbar')
        temperature    		=   units.Quantity(ex.TABS,'kelvin')

        #Water Vapor QV
        #Specific humidity for water vapor
        specific_humidity_v	=   units.Quantity(ex.QV  ,'g/kg')
        relative_humidity       =   units.Quantity(ex.RELH[:]/100.0  ,'')

        #TOTAl Water QT
        #TOTAl Water Specific humidity qt=qv+ql 
        specific_humidity_t	=   units.Quantity(ex.QT  ,'g/kg')

        alt            		=   units.Quantity(ex.z   ,'m')
        v_wind      		=   units.Quantity(ex.U   ,'m/seconds')
        u_wind      		=   units.Quantity(ex.V   ,'m/seconds')

        #Deep point temperature
        dw   	    =   mpy.dewpoint_from_specific_humidity( pressure[:], temperature[:,:],specific_humidity_v[:,:])

        mxr         =   mpy.mixing_ratio_from_specific_humidity(specific_humidity_v[:,:])

        tv          =   mpy.virtual_temperature(temperature[:,:],mxr[:])

        #Caculated properties
        #Parcel temperature
        tp=np.zeros((ex.data.shape[0],ex.z.shape[0]))


        #Calculated the parcel properties from the initial condition 
        #it is no recomended, cin goes to zero 

        for i in range(0,ex.data.shape[0]): 

            tp[i,:]     =   mpy.parcel_profile(pressure[:], temperature[i,0], dw[i,0]) 


        #Calculated the parcel properties from the 200:400 meters mean (Fecher-Bertenthon) 

        #for i in range(0,ex.data.shape[0]): 

        #    t_200 = np.mean(temperature[i,0:4])
        #    dw_200= np.mean(dw[i,0:4])
        #    tp[i,:]     =   mpy.parcel_profile(pressure[:], t_200, dw_200) 

        
        tpu  	=   units.Quantity(tp   ,'kelvin')

        #mx=mixing ratio equal than the envioroment 
        tvp     =   mpy.virtual_temperature(tpu        ,mxr ) 


        tvd  =tv.magnitude
        tvpd =tvp.magnitude

        #Virtual potencial temperature
        thetav =np.zeros((ex.data.shape[0],ex.z.shape[0]))
        thetavp=np.zeros((ex.data.shape[0],ex.z.shape[0]))

        for i in range(0,ex.data.shape[0]): 

            thetav  =   mpy.virtual_potential_temperature(pressure[:],temperature[i,:], mxr[:])
            thetavp =   mpy.virtual_potential_temperature(pressure[:],tpu[i,:]        , mxr[:])

        
        lfc =np.zeros(ex.data.shape[0])
        el  =np.zeros(ex.data.shape[0])
        lcl =np.zeros(ex.data.shape[0])
        l0  =np.zeros(ex.data.shape[0])
        l1  =np.zeros(ex.data.shape[0])
        l2  =np.zeros(ex.data.shape[0])
        cin =np.zeros(ex.data.shape[0])
        cin_uw =np.zeros(ex.data.shape[0])
        cin_flecher =np.zeros(ex.data.shape[0])
        cape=np.zeros(ex.data.shape[0])

        for i in range(0,ex.data.shape[0]): 

            lfc_m = mpy.lfc(pressure,temperature[i,:],dw[i,:])
            lfc[i]= lfc_m[0].magnitude
            
            el_m  = mpy.el(pressure , temperature[i,:],dw[i,:])
            el[i] = el_m[0].magnitude
            
            #Calculing lifting condensation level 
            lcl_m = mpy.lcl(pressure[0], temperature[i,0], dw[i,0],max_iters=50,eps=1e-5)
            #lcl_m = mpy.lcl(np.mean(pressure[0:4]), np.mean(temperature[i,0:4]), np.mean(dw[i,0:4]),max_iters=50,eps=1e-5)
            lcl[i]= lcl_m[0].magnitude

            #level of the end of pbl 
            l0         =np.argmin(ex.TVFLUX[i][:]) 

            #level lf lfc, el
            l1   ,l2   =down.pressure_n(lfc[i],el[i],ex.p[:],ex)

            #level lcl, el
            l3   ,l4   =down.pressure_n(lcl[i],el[i],ex.p[:],ex)

            inte_cape  =(tvpd[i][l1:l2]-tvd[i][l1:l2])/(tvd[i][l1:l2])
            cape[i]    = 9.81*integrate.simps(inte_cape,ex.z[l1:l2])

            #Uw washingon CIN, from lcl from lfc
            if l0<l1:
                inte_cin   =(tvpd[i][l0:l1]-tvd[i][l0:l1])/(tvd[i][l0:l1])
                cin_uw[i]     = -9.81*integrate.simps(inte_cin,ex.z[l0:l1])
            else:
                cin_uw[i]     = -0.001 

            #cin own 
            inte_cin   =(tvpd[i][0:l1]-tvd[i][0:l1])/(tvd[i][0:l1])
            cin[i]     = -9.81*integrate.simps(inte_cin,ex.z[0:l1])

            #CIN Flecher, from 200=300 to cloud base at lifting condensation level# 
            inte_cin   =(tvpd[i][0:l3]-tvd[i][0:l3])/(tvd[i][0:l3])
            cin_flecher[i]     = -9.81*integrate.simps(inte_cin,ex.z[0:l3])

            ##fig = plt.figure()
            ######New axis
            ##ax  = plt.axes()
            ###plt.plot(ex.data,cape,'g',label='own cape')
            ###plt.plot(tvpd[i,:] ,ex.z,'r',label='parcel ')
            ###plt.plot(tv[i,:]   ,ex.z,'b', label='envirioment')

            ##plt.plot(thetav[i,:]   ,ex.z,'r', label='envirioment')
            ##plt.plot(thetavp[i,:]  ,ex.z, 'b', label='parcel')

            ##ax.legend(frameon=False)

            ##plt.show()
            
        
        #cin and cape calculate from metpy
        ci =np.zeros((tovar.data.shape[0]))
        cap=np.zeros((tovar.data.shape[0]))

        for i in range(0,tovar.data.shape[0]): 
        
            #capii,cinii  =   mpy.most_unstable_cape_cin(pressure[:], temperature[i,:], dw[i,:]) 
            capii,cinii =   mpy.cape_cin(pressure[:], temperature[i,:], dw[i,:],tpu[i,:]) 
        
            cap[i]  =-1.0*capii.magnitude
            ci[i]   =-1.0*cinii.magnitude

        

        #to save cape and cin in from metpy netcdffile
        cape_cin_netcdf(cap,ci,ex,exp_label[k]) 

        label="%s_fecher"%(exp_label[k])
        cape_cin_netcdf(cap,cin_flecher,ex,label) 

        label="%s_uw"%(exp_label[k])
        cape_cin_netcdf(cap,ci,ex,label) 

        fig = plt.figure()
        ####New axis
        ax  = plt.axes()
        #plt.plot(ex.data,cape,'g',label='own cape')
        plt.plot(ex.data,cin ,'r',label='CIN own ')

        #plt.plot(ex.data,cap,'b',label='cape')
        plt.plot(ex.data,ci ,'m',label=' CIN met_py')

        #plt.plot(ex.data,cap,'b',label='cape')
        plt.plot(ex.data,cin_flecher ,'orange',label=' CIN Flecher')

        plt.plot(ex.data,cin_uw ,'g',label=' CIN UW')

        #plt.plot(ex.data,ex.CAPE,'orange',label=' SAM cape')
        plt.plot(ex.data,-1.0*ex.CIN[:],'b',label='SAM CIN')

        #plt.axis( [ 350.0, 450,0,7000])
        #plt.ylabel(r'Parcel $\mathrm{ [Jkg^{-1}]}$') 
        ax.legend(frameon=False)
        ##ax.set_title('CAPE')

        plt.show()
        #exit()

        k=k+1

    return cape,cin




def cape_sam_i(exp,hours,days,exp_label):


    k=0

    for ex in exp: 
    

        #Inicial hour
        hi=hours[k][0]    
        #Final hour
        hf=hours[k][1] 

        idi     = dt.datetime(2014, days[k][2] ,days[k][0], hi) 
        idf     = dt.datetime(2014, days[k][3] ,days[k][1], hf)


        print("Data", idi, ' to ', idf) 

        ni,nf= down.data_n(idi,idf,ex.data[:])

        pressure       		=   units.Quantity(ex.p   ,'mbar')
        temperature    		=   units.Quantity(ex.TABS,'kelvin')

        #water vapor QV
        #Specific humidity for water vapor
        specific_humidity_v	=   units.Quantity(ex.QV  ,'g/kg')
        relative_humidity       =   units.Quantity(ex.RELH[:]/100.0  ,'')

        #TOTAl Water QT
        #TOTAl Water Specific humidity qt=qv+ql 
        specific_humidit_t	=   units.Quantity(ex.QT  ,'g/kg')

        alt            		=   units.Quantity(ex.z   ,'m')
        v_wind      		=   units.Quantity(ex.U   ,'m/seconds')
        u_wind      		=   units.Quantity(ex.V   ,'m/seconds')


        i=80

        #Deep point temperature
        dws  	    =   mpy.dewpoint_from_specific_humidity( pressure[:], temperature[i,:],specific_humidity_v[i,:])
        dwr  	    =   mpy.dewpoint_from_relative_humidity(temperature[i,:],relative_humidity[i,:])

        #fig = plt.figure()
        #####New axis
        #ax  = plt.axes()

        #plt.plot(dws,ex.z[:],'g')
        #plt.plot(dwr,ex.z[:],'r')
        #plt.show()


        #Caculated properties
        #Parcel temperature
        q           =   mpy.specific_humidity_from_dewpoint(pressure[:],dws)
        mxr         = mpy.mixing_ratio_from_specific_humidity(specific_humidity_v[i,:])


        #fig = plt.figure()
        ####New axis
        #ax  = plt.axes()
        #plt.plot(q[:],ex.z[:],'g')
        #plt.plot(specific_humidity_v[100,:],ex.z[:],'r')
        #plt.plot(mxr,ex.z,'b')
        #plt.show()
        #exit()

        tp      =   mpy.parcel_profile(pressure[:], temperature[i,0], dws[0])
        tpu  	=   units.Quantity(tp   ,'K')
        tv      =   mpy.virtual_temperature(temperature[i,:],mxr)

        #mx=mxr of air 
        tvp     =   mpy.virtual_temperature(tp[:]        ,mxr ) 

        fig = plt.figure()
        #####New axis
        ax  = plt.axes()

        plt.plot(tv[:],ex.z[:],'g')
        plt.plot(tvp[:],ex.z[:],'r')

        thetav          =   mpy.virtual_potential_temperature(pressure[:], temperature[i,:],mxr) 
        thetavp         =   mpy.virtual_potential_temperature(pressure[:], tpu,mxr) 

        ####New axis
        fig = plt.figure(2)
        ax  = plt.axes()

        plt.plot(thetav,ex.z,'r', label='Enviroment')
        plt.plot(thetavp,ex.z,'g',label='Parcel')

        ##plt.axis( [ 350.0, 450,0,7000])
        #plt.ylabel(r'Parcel $\mathrm{ [Jkg^{-1}]}$') 

        #plt.show()

        tvd  =tv[:].magnitude
        tvpd =tvp[:].magnitude

        lfc=mpy.lfc(pressure[:],temperature[i,:],dws)
        el =mpy.el(pressure[:], temperature[i,:], dws)
        lcl=mpy.lcl(pressure[0], temperature[i,0], dws[0],max_iters=50,eps=1e-5)

        l0        = np.argmin(ex.TVFLUX[i][:]) 

        l1,l2     = down.pressure_n(lfc[0].magnitude,el[0].magnitude,ex.p[:])

        print(l0,l1)#
        print(ex.z[l0],ex.z[l1])#

        #l0,l1=down.pressure_n(lcl[0].magnitude,lfc[0].magnitude,ex.p[:])

        inte_cape  =(tvpd[l1:l2]-tvd[l1:l2])/(tvd[l1:l2])
        inte_cin   =(tvd[l0:l1]-tvpd[l0:l1])/(tvd[l0:l1])
        #inte_cin   =(tvd[l0:l1]-tvpd[l0:l1])/(tvd[l0:l1])

        cape       = 9.81*integrate.simps(inte_cape,ex.z[l1:l2])
        cini       = 9.81*integrate.simps(inte_cin ,ex.z[l0:l1])

        cap,cin    =   mpy.most_unstable_cape_cin(pressure[:], temperature[i,:], dws) 
        cap2,cin2  =   mpy.cape_cin(pressure[:], temperature[i,:], dws,tp)

        print (cape,cap,cap2)
        print (cini,cin,cin2)

        fig = plt.figure()
        ###New axis
        ax  = plt.axes()
        plt.plot(tvp,ex.z[:],'g')
        plt.plot(tv,ex.z[:],'r')
        plt.axis( [ 350.0, 450,0,7000])
        plt.ylabel(r'Parcel $\mathrm{ [Jkg^{-1}]}$') 


        ax.legend(frameon=False)
        #ax.set_title('CAPE')

        plt.show()
        exit()

def cape_sam(exp,hours,days,exp_label):


    k=0

    for ex in exp: 
    

        #Inicial hour
        hi=hours[k][0]    
        #Final hour
        hf=hours[k][1] 

        idi     = dt.datetime(2014, days[k][2] ,days[k][0], hi) 
        idf     = dt.datetime(2014, days[k][3] ,days[k][1], hf)


        print("Data", idi, ' to ', idf) 

        ni,nf= down.data_n(idi,idf,ex.data[:])

        pressure       		=   units.Quantity(ex.p   ,'mbar')
        temperature    		=   units.Quantity(ex.TABS,'kelvin')
        specific_humidity	=   units.Quantity(ex.QV  ,'g/kg')
        alt            		=   units.Quantity(ex.z   ,'m')
        v_wind      		=   units.Quantity(ex.U   ,'m/seconds')
        u_wind      		=   units.Quantity(ex.V   ,'m/seconds')
 


        #Deep point temperature
        dw  	    =   mpy.dewpoint_from_specific_humidity(specific_humidity[:,:], temperature[:,:], pressure[:])


        #Caculated properties
        #Parcel temperature
        tp=np.zeros((ex.data.shape[0],ex.z.shape[0]))

        for i in range(ni,nf): 
            tp[i,:]      =   mpy.parcel_profile(pressure[:], temperature[i,0], dw[i,0]) 
##        tp      =   mpy.parcel_profile(pressure[:], temperature[0,:], dw[0,:]) 

        tpu  		=   units.Quantity(tp   ,'K')
        
        
        q           =   mpy.specific_humidity_from_dewpoint(dw, pressure)
        qs          =   mpy.saturation_mixing_ratio(pressure, temperature[:,:])
        
        
        hd          =   mpy.dry_static_energy(z_u[:], temperature[:,:])
        
        
        #hdp=np.zeros((ex.data.shape[0],ex.z.shape[0]))
        #hdpu   		=   units.Quantity(hdp   ,'kJ/kg')
        #for i in range(ni,nf):
        #	hdpu[i]         =   mpy.dry_static_energy(alt[:], tpu[i,:])
        
        hd          =   mpy.dry_static_energy(z_u[:], tpu[:,:])
        
        hm          =   mpy.moist_static_energy(z_u[:], temperature[:,:],q[:,:])
        hms         =   mpy.moist_static_energy(z_u[:], temperature[:,:],qs[:,:])
        
        tv          =   mpy.virtual_potential_temperature(pressure[:], temperature[:,:],0.622) 
        
        te	    =	mpy.equivalent_potential_temperature(pressure[:], temperature[:,:], dw[:,:])
        tes	    =	mpy.saturation_equivalent_potential_temperature(pressure[:], temperature[:,:])
        
        theta	    =	mpy.potential_temperature(pressure[:], temperature[:,:])
        
        
        #Parcel temperature
        
        cin=np.zeros((ex.data.shape[0],ex.z.shape[0]))
        
        cap=np.zeros((ex.data.shape[0],ex.z.shape[0]))
        
        tvp=np.zeros((ex.data.shape[0],ex.z.shape[0]))
        
        
        for i in range(ni,nf): 
            cap[i,:],cin[i,:] =   mpy.most_unstable_cape_cin(pressure[:], temperature[i,:], dw[i,:]) 
            tvp[i,:] 	      =   mpy.virtual_potential_temperature(pressure[:], tpu[i,:],0.622) 
        
        #cap,ci 	      =   mpy.most_unstable_cape_cin(pressure, temperature, dw) 
        
        
        #mpl.rcParams.update(params)
        
        ###############################################################
        #fig,ax	=	figure_sam()
        #plt.plot(ex.data[ni:nf],cap[ni:nf],'g')
        #plt.axis( [idi,idf, 00.00, 500])
        #plt.ylabel(r'MCAPE $\mathrm{ [Jkg^{-1}]}$') 
        fig = plt.figure()
        ###New axis
        ax  = plt.axes()
        plt.plot(tvp[100,:],ex.z[:],'g')
        plt.plot(tv[100,:],ex.z[:],'r')
        plt.axis( [ 350.0, 450,0,7000])
        plt.ylabel(r'Parcel $\mathrm{ [Jkg^{-1}]}$') 
        
        
        ax.legend(frameon=False)
        
        
        #ax.set_title('CAPE')
        
        plt.show()
        exit()
        
        plt.savefig('%scape_%s.pdf'%(file_fig,exp_label[k]), format='pdf', dpi=1000)
        ###############################################################
        fig,ax	=	figure_sam()
        
        plt.plot(ex.data[ni:nf],-cin[ni:nf],'g')
        #plt.plot(ex.data[ni:nf],ex.CIN[ni:nf],'g',label='sam')
        #ax.set_title('CIN')
        
        plt.ylabel(r'CIN $\mathrm{ [Jkg^{-1}]}$') 
        
        plt.axis( [idi,idf, -50, 100])
        
        ax.legend(frameon=False)
        
        plt.savefig('%scin_%s.pdf'%(file_fig,exp_label[k]), format='pdf', dpi=1000)
        
        #####################################
        
        #####################################
        
        
        fig,ax	=	figure_sam_spatial_inv()
        
        plt.axis([290,400,1040,20]) 
        
        ax.set_xlabel('[K]')
        ax.set_ylabel('p [mb]')
        
        ax.text(300, 50, r'$\theta_e$ $\_ _{.}$')
        ax.text(300, 80, r'$\theta_{es}$ _')
        ax.text(300, 110, r'$\theta$ .. ')
        
        for i in range(ni,nf,10): 
        
        	line,col=color_hours(ex.data[i].hour)
        
        	ax.plot(te[i,:],pressure[:],'-.',color=col,label='Hour=%s'%(ex.data[i].hour))
        	ax.plot(tes[i,:],pressure[:],'-',color=col)
        	ax.plot(ex.THETA[i,:],pressure[:],':',color=col)
        
        ax.legend(frameon=False)
        
        #plt.savefig('%sequivalent_potential_temperature_%s.pdf'%(file_fig,exp_label[k]), format='pdf', dpi=1000)
        
        plt.close()
        ###############################################################
        
        fig,ax	=	figure_sam_spatial_inv()
        
        plt.axis([360,430,1040,20]) 
        
        ax.text(360, 50, r'Parcel -')
        ax.text(360, 80, r'Enviroment _.')
        
        ax.set_xlabel('[K]')
        ax.set_ylabel('p [mb]')
        
        for i in range(ni,nf,10): 
        
        	line,col=color_hours(ex.data[i].hour)
        
        	ax.plot( tv[i,:],pressure,'-.',color=col,label='Hour=%s'%(ex.data[i].hour))
        	ax.plot(tvp[i,:],pressure,'-',color=col)
        
        ax.legend(frameon=False)
        #plt.savefig('%svirtual_potential_temperature_%s.pdf'%(file_fig,exp_label[k]), format='pdf', dpi=1000)
        plt.close()
        
        ########################################
        fig,ax	=	figure_sam_spatial()
        
        plt.axis([300,380,0,10]) 
        
        ax.text(310, 9   , r'Hd   -.')
        ax.text(310, 8.7 , r'Hmi  _.')
        ax.text(310, 8.4   , r'Hms  ..')
        
        
        ax.set_xlabel(r'[$\mathrm{kJkg^{-1}}$]')
        ax.set_ylabel('z [km]')
        
        for i in range(ni,nf,10): 
        
        	line,col=color_hours(ex.data[i].hour)
        
        	ax.plot(   hd[i,:],alt[:]/1000.0,'-.',color=col,label='Hour=%s'%(ex.data[i].hour))
        	ax.plot(   hm[i,:],alt[:]/1000.0,'-' ,color=col)
        	ax.plot(  hms[i,:],alt[:]/1000.0,':' ,color=col)
        
        ax.legend(frameon=False)
        #plt.savefig('%sstatic_energy_%s.pdf'%(file_fig,exp_label[k]), format='pdf', dpi=1000)
        
        
        k+=1

    return  cap,cin

def skew_T(exp,date,lim,exp_label,exp_label2,plot_def,show=True):


    k=0

    date_format = '%Y-%m-%dT%H'


    for ex in exp: 

        datei  = dt.datetime.strptime(date[k], date_format)

        time  = np.datetime64(datei) 

        time1  =   down.data_to_reference_vector(ex.time,1,1,2025)

        ex['time']=time1

        tovar = ex.sel(time=time,method='nearest')
        #becayse some experiment font in the ohter hour, aproxima 
        # por cima dessa hora
        #try:
        #    tovar = ex.sel(time=time,method='backfill')
        #except:
        #    tovar = ex.sel(time=time,method='nearest')

        print(tovar.name.values)
        print(tovar.time.values)
        #exit()
        
        pressure       		=   tovar.p*units('mbar')

        temperature    		=   tovar.TABS*units('kelvin')
        temperature2   		=   tovar.TABS*units('kelvin')+2*units('K')
        temperature3   		=   tovar.TABS*units('kelvin')-2*units('K')

        #mr=mr/md
        # you do not use QT, because vapor is only matters
        mixing_ratio	        =   tovar.QV*units('g/kg')
        specific_humidity       =   mpy.specific_humidity_from_mixing_ratio(mixing_ratio)
        #specific_humidity1       =   (mixing_ratio[:].values/1000)/((1+mixing_ratio[:].values/1000))*units('g/kg')

        z_u            		=   tovar.z*units('m')
        v_wind      		=   tovar.U*units('m/s')
        u_wind      		=   tovar.V*units('m/s')
        
        #Deep point temperature
        dw  	    =   mpy.dewpoint_from_specific_humidity( pressure[:],specific_humidity)

        tp     =   mpy.parcel_profile(pressure, temperature[0], dw[0]) 
        tp2    =   mpy.parcel_profile(pressure, temperature2[0], dw[0]) 
        tp3    =   mpy.parcel_profile(pressure, temperature3[0], dw[0]) 

        q           =   mpy.specific_humidity_from_dewpoint( pressure,dw)

        qs           =   mpy.saturation_mixing_ratio(pressure, temperature[:])

        hd           =   mpy.dry_static_energy(z_u[:], tp[:])
        
        hm           =   mpy.moist_static_energy(z_u[:], temperature[:],q[:])

        hms          =   mpy.moist_static_energy(z_u[:], temperature[:],qs[:])
        
        tv           =   mpy.virtual_potential_temperature(pressure[:], temperature[:],0.622) 
        
        te	     =	mpy.equivalent_potential_temperature(pressure[:], temperature[:], dw[:])

        tes	     =	mpy.saturation_equivalent_potential_temperature(pressure[:], temperature[:])
        
        theta	     =	mpy.potential_temperature(pressure[:], temperature[:])

        theta2	     =	mpy.potential_temperature(pressure[:], temperature[:]+2*units('K'))

        theta3	     =	mpy.potential_temperature(pressure[:], temperature[:]-2*units('K'))

        theta_adiab  =	mpy.potential_temperature(pressure[:], tp )

        theta_adiab2 =	mpy.potential_temperature(pressure[:], tp2)

        theta_adiab3 =	mpy.potential_temperature(pressure[:], tp3)

        #"""
        #ax1.plot(theta[:,40],theta.z,color='red')
        #ax1.plot(theta2[:,40],theta.z,color='red')
        #ax1.plot(theta_adiab [40,:],tovar.z[:],color='blue') 
        #ax1.plot(theta_adiab2[40,:],tovar.z[:],color='blue') 
        #ax1.axis( [295,320,0,4000])
        #plt.show()

        #Ticks of the axisss

        size_wg = plot_def[k][2][0]
        size_hf = plot_def[k][2][1]
        cmm     = plot_def[k][2][2]

        tama= pp.plotsize(size_wg,size_hf, cmm,'diurnal')

        fig  = plt.figure()
        #ax   = plt.axes()


        #skew=SkewT(fig,rotation=30)
        skew=SkewT(fig,rotation=10,aspect=180)
        

        #fig.subplots_adjust(left=0.15, bottom=0.0, right=0.85, top=1.10)
        #skew.ax.set_aspect(0.5)

        skew.plot(pressure,temperature[:].metpy.convert_units('degC'),'r',label='T')  
        #skew.plot(pressure,temperature2[:].metpy.convert_units('degC'),'magenta',label='T=T+2')
        #skew.plot(pressure,temperature3[:].metpy.convert_units('degC'),'navy',label='T=T-2')

        #skew.plot(pressure,theta[:].metpy.convert_units('degC'),'r')
        #skew.plot(pressure,theta2[:].metpy.convert_units('degC'),'b')

        skew.plot(pressure,dw[:],'g', label='dp T')

        # Plot LCL temperature as black dot
        #skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')
        
        # Plot the parcel profile as a black line
        skew.plot(pressure, ( tp[:].metpy.convert_units('degC')), 'black', linewidth=1,linestyle='--',label='parcel T')

        #skew.plot(pressure, (tp2[:].metpy.convert_units('degC')), 'magenta', linewidth=1,linestyle='--',label='parcel T=T+2')

        #skew.plot(pressure, (tp3[:].metpy.convert_units('degC')), 'navy', linewidth=1,linestyle='--',label='parcel T=T-2')
        
        # Shade areas of CAPE and CIN
        #skew.shade_cin( pressure,  temperature[0,:],  (tpu[0,:]))#, dw[0,:])
        #skew.shade_cape(pressure,  temperature[0,:],  (tpu[0,:]))

        # Plot a zero degree isotherm
        skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)


        # Shade areas of CAPE and CIN
        skew.shade_cin(pressure , temperature.metpy.convert_units('degC'), tp.metpy.convert_units('degC'), dw)
        skew.shade_cape(pressure, temperature.metpy.convert_units('degC'), tp.metpy.convert_units('degC'))

        #skew.shade_cin(pressure , temperature2.metpy.convert_units('degC'), tp2.metpy.convert_units('degC'))
        #skew.shade_cape(pressure, temperature2.metpy.convert_units('degC'), tp2.metpy.convert_units('degC'))




        # Add the relevant special lines
        #skew.plot_dry_adiabats()

        skew.plot_moist_adiabats()
        skew.plot_mixing_lines()

        #p_levels = np.array([1000, 925, 850, 700, 500])#, 400])#,200, 150])
        p_levels = np.array([1000, 925, 850, 700, 600,550,500,450,400,300,200])#,200, 150])

        skew.ax.set_xlim(lim[k][0],lim[k][1])
        skew.ax.set_ylim(lim[k][2],lim[k][3])

        skew.ax.yaxis.set_major_locator(FixedLocator(p_levels))
        #skew.ax.set_yticks(p_levels)

        plt.text(plot_def[k][0][1],plot_def[k][0][2],f'{exp_label[k]} {plot_def[k][0][0]}',fontsize=tama)

        #skew.ax.set_ylabel('Pressure (hpa)')
        #skew.ax.set_xlabel('Temperature ($^\\circ$C)')
        skew.ax.set_ylabel('P [hpa]')
        skew.ax.set_xlabel('T [$^\\circ$C]')

        #p_levels = np.array([1000, 925, 850, 700, 500, 400])#,200, 150])
        p_levels = np.array([1000, 925, 850, 700, 600,550,500,450,400,300,200])#,200, 150])

        # sort by pressure
        idx = np.argsort(pressure.values)
        pressure_vals = pressure.values[idx]
        z_vals = z_u.values[idx]
        
        # forward transform
        def p_to_z(p):
            return np.interp(p, pressure_vals, z_vals)
        
        # sort by height for inverse
        idx_z = np.argsort(z_vals)
        z_sorted = z_vals[idx_z]
        p_sorted_from_z = pressure_vals[idx_z]
        
        # inverse transform (FIXED)
        def z_to_p(z):
            return np.interp(z, z_sorted, p_sorted_from_z)

        z_levels=p_to_z(p_levels)

        #to test the interpolation, only accep in increasing way 
        #print(z_values)
        #print(z_to_p(z_values))

        # --- secondary axis ---
        secax = skew.ax.secondary_yaxis('right', functions=(p_to_z, z_to_p))
        #secax.set_ylabel('Height (km)')
        secax.set_ylabel('z (km)')

        #idx = np.argsort(pressure.values)
        #z_levels = np.interp(
        #    p_levels,
        #    pressure.values[idx],
        #    z_u.values[idx]
        #)

        #secax.set_yticks(z_levels)
        secax.yaxis.set_major_locator(FixedLocator(z_levels))
        secax.set_yticklabels([f"{z/1000:.1f}" for z in z_levels])

        # remove all minor ticks
        secax.yaxis.set_minor_locator(NullLocator())

        #legend(loc='upper right')
        plt.legend(frameon=False,loc='upper right')

        #plt.show()
        #exit()


        hour=tovar.time.dt.hour.values
        name=f"{ex.name.values}_{hour}h"
    
        if tovar.time.dt.minute>50:
            hour=tovar.time.dt.hour.values+1
            name=f"{ex.name.values}_{hour}h"

            #print(name)
        #if tovar.time.dt.minute<10:
        #    hour=tovar.time.dt.hour.values
        #    name=f"{ex.name.values}_{hour}h"
       # print(name)
        #    exit()

        fig.savefig('%s/skewT_%s.pdf'%(pars.out_fig,name),bbox_inches='tight', format='pdf', dpi=200)

        k+=1

    if show:
        plt.show()

    return  

def cape_sam_all(exp,hours,date,alt,exp_label,exp_label2,plot_def,color,line,date0=None):

    if date0==None:
        date0=[]


    #date_format = '%Y-%m-%dT%H:%M'
    date_format = '%Y-%m-%dT%H'

    agora = datetime.now()
    # Formata e imprime
    data_formatada = agora.strftime(date_format)
    datenow=dt.datetime.strptime(data_formatada, date_format)
    
    #Ticks of the axisss
    ###############################################################
    size_wg = plot_def[0][3][0]
    size_hf = plot_def[0][3][1]
    cmm     = plot_def[0][3][2]

    tama= pp.plotsize(size_wg,size_hf, cmm,'temporal')


    fig1  = plt.figure()
    ax1   = plt.axes()

    size_wg = plot_def[1][3][0]
    size_hf = plot_def[1][3][1]
    cmm     = plot_def[1][3][2]

    fig2  = plt.figure()
    ax2   = plt.axes()

    cape_all=[]
    cin_all=[]


    k=0
    for ex in exp: 

        datei=dt.datetime.strptime(date[k][0], date_format)
        datef=dt.datetime.strptime(date[k][1], date_format)

        
        time1 = np.datetime64(date[k][0]) 
        time2 = np.datetime64(date[k][1])

        #print(date[k][0],date[k][1])
        #print(datei,datef)
        #print(time1,time2)
    
        ni,nf   = down.data_n(time1,time2,ex.time.values) 

        tovar1  = ex.sel(time=slice(ex.time[ni],ex.time[nf-1]))

        li, lf  = down.level_n(0,15000,ex.z.values)

        tovar   = tovar1.sel(z=slice(ex.z[li],ex.z[lf-1]))


        time11  = tovar.time


        #time22  = down.data_to_reference_vector(time11,1,1,2026)
        if date0:  
            date0 = date0
        else:
            date0 =[1,1,datenow.year]

        time22   = down.data_to_reference_vector(time11,date0)

        pressure       		=   tovar.p*units('mbar')

        temperature    		=   tovar.TABS*units('kelvin')

        #t
        #sam work with mixing ratio!!!
        #specific_humidity	=   tovar.QV*units('g/kg')
        mr_u        =   tovar.QT*units('g/kg')
        #convert to specific humidity from mixing ratio
        specific_humidity  =   mr_u/(1.0 + mr_u) 


        z_u            		=   tovar.z*units('m')
        #v_wind      		=   tovar.U*units('m/s')
        #u_wind      		=   tovar.V*units('m/s')
        
        #Deep point temperature
        dw  	    =   mpy.dewpoint_from_specific_humidity( pressure[:], temperature[:,:],specific_humidity[:,:])

        #Caculated properties
        #Parcel temperature
        tp =np.zeros((tovar.time.shape[0],tovar.z.shape[0]))

        for i in range(0,tovar.time.shape[0]): 

            tp[i,:]      =   mpy.parcel_profile(pressure[:], temperature[i,0], dw[i,0]) 

        tpu  =   tp   * units('K')

        q           =   mpy.specific_humidity_from_dewpoint( pressure,dw)

        qs          =   mpy.saturation_mixing_ratio(pressure, temperature[:,:])
        

        hd          =   mpy.dry_static_energy(z_u[:], tpu[:,:])
        
        hm          =   mpy.moist_static_energy(z_u[:], temperature[:,:],q[:,:])

        hms         =   mpy.moist_static_energy(z_u[:], temperature[:,:],qs[:,:])
        
        tv          =   mpy.virtual_potential_temperature(pressure[:], temperature[:,:],0.622) 
        
        te	        =	mpy.equivalent_potential_temperature(pressure[:], temperature[:,:], dw[:,:])

        tes	        =	mpy.saturation_equivalent_potential_temperature(pressure[:], temperature[:,:])
        
        theta	    =	mpy.potential_temperature(pressure[:], temperature[:,:])

        theta_adiab =	mpy.potential_temperature(pressure[:], tpu )

        cin=np.zeros((tovar.time.shape[0]))

        cap=np.zeros((tovar.time.shape[0]))

        t_inversion         = np.zeros((tovar.time.shape[0],tovar.z.shape[0]))#*units('K')
        t_inversion[:,:]    = temperature[:,:].values 

        for i in range(0,tovar.time.shape[0]): 

            c1=0
            c2=0

            for j in range(0,tovar.z.shape[0]):

                if tovar.z[j].values>5000.0 and c1==0:
                
                    y1  =   tovar.z[j].values
                    x1  =   temperature[i,j].values
                    c1+=1 
                
                if tovar.z[j].values>=5500.0:
                
                    if c2==0:
                        y2  =   tovar.z[j].values
                        x2  =   temperature[i,j].values
                
                        mi=(x2-x1)/(y2-y1)
                
                        c2+=1 
                
                    #line equation, y-y0=m(x-x0)
                    #theta_inversion[k,i] = x2 + (2.0)*mi*(z_u[k,i].magnitude-y2)
                    #temperature[i,j] = (x2 + (2.0)*mi*(tovar.z[j].values-y2))*units('kelvin')
                    t_inversion[i,j] = (x2 + -(1.0)*mi*(tovar.z[j].values-y2))#*units('kelvin')

        """
        #to calculate the new cape with the inversioni 
        fig = plt.figure()
        ax  = plt.axes()

        ax.plot(temperature[i,:], tovar.z,color='red' ,ls='--')
        ax.plot(t_inversion[i,:],tovar.z,color='blue' ,ls='--')

        #plt.show()
        #exit()

        fig2 = plt.figure()
        ax2  = plt.axes()
        ax.invert_yaxis()
        ax2.invert_yaxis()
        """

        for i in range(0,tovar.time.shape[0]): 
        
            #capii,cinii =   mpy.most_unstable_cape_cin(pressure[:], temperature[i,:], dw[i,:]) 
            #capii,cinii =   mpy.cape_cin(pressure[:], temperature[i,:], dw[i,:],tpu[i,:],which_el='bottom') 
            capii,cinii =   mpy.cape_cin(pressure[:], t_inversion[i,:]*units('K'), dw[i,:],tpu[i,:]) 

        
            cap[i]=capii.magnitude
            cin[i]=cinii.magnitude

            """
            print(cap[i], tovar.time[i].values)

            if cap[i]==0:

                print(cap[i-1], tovar.time[i-1].values)
                print('xx',capii,cinii) 

                ax.plot(temperature[i-1,:], pressure[:],color='red')
                ax.plot(tpu[i-1,:],         pressure[:],color='black')
                ax2.plot(dw[i-1,:],         pressure[:],color='green')

                ax.plot(temperature[i,:], pressure[:],color='red' ,ls='--')
                ax.plot(tpu[i,:],         pressure[:],color='black',ls='--')
                ax2.plot(dw[i,:],          pressure[:],color='green',ls='--')

                plt.show()
            """

        ###############################################################
        
        ax1.plot(time22       ,cap   ,label='%s'%(exp_label2[k]),color=color[k],linewidth=1.5,alpha=1.0,dashes=line[k],marker='')

        #ax1.plot( tovar.time[0:110]        ,tovar.CAPE[0:110]   ,label='%s'%(exp_label2[k]),color='red',linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        ax2.plot( time22      ,-cin  ,label='%s'%(exp_label2[k]),color=color[k],linewidth=1.5,alpha=1.0,dashes=line[k],marker='')
        #ax2.plot( tovar.time[0:110]       ,tovar.CIN[0:110]   ,label='%s'%(exp_label2[k]),color='red',linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        #####################################
        
        
        cape_all.append(cap)
        cin_all.append(cin)
        
        k+=1


    #ax1.legend(frameon=False,loc='lower right')
    ax2.legend(frameon=False,loc='upper right')

    ax1.set_xlabel( plot_def[0][0][0]) 
    ax1.set_ylabel( plot_def[0][0][1]) 

    ax2.set_xlabel( plot_def[1][0][0]) 
    ax2.set_ylabel( plot_def[1][0][1]) 
    
    d11=dt.datetime.strptime(hours[0][0], date_format)
    d12=dt.datetime.strptime(hours[0][1], date_format)
    d21=dt.datetime.strptime(hours[1][0], date_format)
    d22=dt.datetime.strptime(hours[1][1], date_format)
    ax1.set_xlim(d11, d12)
    ax2.set_xlim(d21, d22)

    ax1.set_ylim(alt[0][0], alt[0][1])
    ax2.set_ylim(alt[1][0], alt[1][1])

    majorFormatter = mpl.dates.DateFormatter('%H')
    ax1.xaxis.set_major_formatter(majorFormatter)
    ax2.xaxis.set_major_formatter(majorFormatter)
    
    locatormax = mdates.HourLocator(interval=alt[0][2])
    locatormin = mdates.HourLocator(interval=int(alt[0][2]/2))

    ax1.xaxis.set_minor_locator(locatormin)
    ax2.xaxis.set_minor_locator(locatormin)

    ax1.xaxis.set_major_locator(locatormax )
    ax2.xaxis.set_major_locator(locatormax )
    
    ax1.grid(axis='x',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )
    ax1.grid(axis='y',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )
    ax2.grid(axis='x',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )
    ax2.grid(axis='y',color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0]  )


    #average!!!
    #mean_cape=np.mean(cape_all,axis=0)
    #mean_cin =np.mean(cin_all,axis=0)

    #ax1.plot( data[0:110]       ,mean_cape[0:110]   ,color='black',linewidth=1.0,alpha=1.0,dashes=[1,0],marker='',label='Average')
    #ax2.plot( data[0:110]       ,-mean_cin[0:110]   ,color='black',linewidth=1.0,alpha=1.0,dashes=[1,0],marker='',label='Average')

    #cis1 =   (mean_cape[0:110]*0.90, mean_cape[0:110]*1.10)
    #cis2 =   (mean_cin[0:110]*0.90  , mean_cin[0:110]*1.10)

    #ax1.fill_between(data[0:110],cis1[0]  ,cis1[1],alpha=0.25,color='black')# **kw)
    #ax2.fill_between(data[0:110],-cis2[0],-cis2[1],alpha=0.25,color='black')# **kw)

    #il     = dt.datetime(2022, 1 ,1, 7) 
    #ax1.text(il,580 , r'%s'%('b)'), fontsize=9, color='black')
    #il     = dt.datetime(2022, 1 ,1, 7) 
    #ax2.text(il,105 , r'%s'%('c)'), fontsize=9, color='black')


    fig1.savefig('%s/cape_%s.pdf'%(pars.out_fig,exp_label[0]),bbox_inches='tight', format='pdf', dpi=200)
    fig2.savefig('%s/cin_%s.pdf' %(pars.out_fig,exp_label[0]),bbox_inches='tight', format='pdf', dpi=200)

    plt.show()

    return  cap,cin

def cape_sam_all_old(exp,hours,date,alt,exp_label,exp_label2,plot_def):


    #parameters={
    #        'font.size' : 6,
    #        'legend.fontsize': 'medium',
    #        'axes.labelsize' : 'medium',
    #        'xtick.labelsize': 'medium',
    #        'ytick.labelsize': 'medium',
    #        }
    #mpl.rcParams.update(params_temp)
	

    k=0

    """
    #Inicial hour
    hi=hours[k][0]    
    #Final hour
    hf=hours[k][1] 

    idi     = dt.datetime(2022, days[k][2] ,days[k][0], hi) 
    idf     = dt.datetime(2022, days[k][3] ,days[k][1], hf)

    print(idi,idf)
    """

    date_format = '%Y-%m-%dT%H'
    
    #Ticks of the axisss
    ###############################################################
    size_wg = plot_def[0][3][0]
    size_hf = plot_def[0][3][1]
    cmm     = plot_def[0][3][2]

    tama= pp.plotsize(size_wg,size_hf, cmm,'temporal')

    fig1  = plt.figure()
    ax1   = plt.axes()

    size_wg = plot_def[1][3][0]
    size_hf = plot_def[1][3][1]
    cmm     = plot_def[1][3][2]

    fig2  = plt.figure()
    ax2   = plt.axes()

    cape_all=[]
    cin_all=[]


    for ex in exp: 

        datei=dt.datetime.strptime(date[k][0], date_format)
        datef=dt.datetime.strptime(date[k][1], date_format)
        
        time1 = np.datetime64(date[k][0]) 
        time2 = np.datetime64(date[k][1])
    
        ni,nf   = down.data_n(time1,time2,ex.time.values) 
        tovar   = ex.sel(time=slice(ex.time[ni],ex.time[nf-1]))

        time11  = tovar.time
        time22  = down.data_to_reference_vector(time11,1,1,2026)

        pressure       		=   tovar.p*units('mbar')
        temperature    		=   tovar.TABS*units('kelvin')
        specific_humidity	=   tovar.QV*units('g/kg')
        z_u            		=   tovar.z*units('m')
        v_wind      		=   tovar.U*units('m/s')
        u_wind      		=   tovar.V*units('m/s')
        
        #Deep point temperature
        dw  	    =   mpy.dewpoint_from_specific_humidity( pressure[:], temperature[:,:],specific_humidity[:,:])

        #Caculated properties
        #Parcel temperature
        tp =np.zeros((tovar.time.shape[0],ex.z.shape[0]))
        tp2=np.zeros((tovar.time.shape[0],ex.z.shape[0]))
        tp3=np.zeros((tovar.time.shape[0],ex.z.shape[0]))

        for i in range(0,tovar.time.shape[0]): 

            tp[i,:]      =   mpy.parcel_profile(pressure[:], temperature[i,0], dw[i,0]) 

            tp2[i,:]     =   mpy.parcel_profile(pressure[:], temperature[i,0]+2*units('K'), dw[i,0]) 

            tp3[i,:]     =   mpy.parcel_profile(pressure[:], temperature[i,0]-2*units('K'), dw[i,0]) 

        #tp     =   mpy.parcel_profile(pressure[:], temperature[:,0], dw[:,0]) 
        #exit()


        tpu  =   tp   * units('K')
        tpu2 =   tp2  * units('K')
        tpu3 =   tp3  * units('K')

        q           =   mpy.specific_humidity_from_dewpoint( pressure,dw)

        qs          =   mpy.saturation_mixing_ratio(pressure, temperature[:,:])
        
        #hd          =   mpy.dry_static_energy(alt[:], temperature[:,:])
        #hdp=np.zeros((ex.data.shape[0],ex.z.shape[0]))
        #hdpu   		=   units.Quantity(hdp   ,'kJ/kg')
        #for i in range(ni,nf):
        #	hdpu[i]         =   mpy.dry_static_energy(alt[:], tpu[i,:])
        

        hd          =   mpy.dry_static_energy(z_u[:], tpu[:,:])
        
        hm          =   mpy.moist_static_energy(z_u[:], temperature[:,:],q[:,:])

        hms         =   mpy.moist_static_energy(z_u[:], temperature[:,:],qs[:,:])
        
        tv          =   mpy.virtual_potential_temperature(pressure[:], temperature[:,:],0.622) 

        tv2         =   mpy.virtual_potential_temperature(pressure[:], temperature[:,:]+2*units('K'),0.622) 

        tv3         =   mpy.virtual_potential_temperature(pressure[:], temperature[:,:]-2*units('K'),0.622) 
        
        te	        =	mpy.equivalent_potential_temperature(pressure[:], temperature[:,:], dw[:,:])

        tes	        =	mpy.saturation_equivalent_potential_temperature(pressure[:], temperature[:,:])
        
        theta	    =	mpy.potential_temperature(pressure[:], temperature[:,:])

        theta2	    =	mpy.potential_temperature(pressure[:], temperature[:,:]+2*units('K'))

        theta3	    =	mpy.potential_temperature(pressure[:], temperature[:,:]-2*units('K'))


        theta_adiab  =	mpy.potential_temperature(pressure[:], tpu )

        theta_adiab2 =	mpy.potential_temperature(pressure[:], tpu2)

        theta_adiab3 =	mpy.potential_temperature(pressure[:], tpu3)

        #jprint(tv.shape)

        #jexit()
        datei  = dt.datetime.strptime('2026-01-01T06', date_format)

        time  = np.datetime64(datei) 

        time1  =   down.data_to_reference_vector(ex.time,1,1,2026)

        ex['time']=time1

        timex = ex.sel(time=time,method='nearest').time.values

        idt=ex.get_index('time').get_loc(timex)

        #print(idt)

        """
        fig  = plt.figure()
        plt.plot(theta[:,idt],theta.z,color='black')
        plt.plot(theta2[:,idt],theta.z,color='red')
        plt.plot(theta3[:,idt],theta.z,color='blue')
        plt.plot(theta_adiab[idt,:],tovar.z[:],color='black') 
        plt.plot(theta_adiab2[idt,:],tovar.z[:],color='red') 
        plt.plot(theta_adiab3[idt,:],tovar.z[:],color='blue') 
        plt.axis( [295,320,0,4000])

        fig  = plt.figure()

        plt.plot(tv[:,idt]  ,tovar.z,color='black')
        #plt.plot(tv2[:,idt] ,tovar.z,color='red')
        #plt.plot(tv3 [:,idt],tovar.z[:],color='blue') 
        #ax.axis( [295,320,0,4000])
        #plt.show()
        #exit()

        fig  = plt.figure()

        skew=SkewT(fig,rotation=30)
        skew.plot(pressure,temperature[0,:].metpy.convert_units('degC'),'r')
        skew.plot(pressure,dw[0,:],'g')

        # Plot LCL temperature as black dot
        #skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')
        
        # Plot the parcel profile as a black line
        skew.plot(pressure, (tpu[0,:]), 'k', linewidth=2)
        
        # Shade areas of CAPE and CIN
        #skew.shade_cin( pressure,  temperature[0,:],  (tpu[0,:]))#, dw[0,:])
        #skew.shade_cape(pressure,  temperature[0,:],  (tpu[0,:]))

        # Plot a zero degree isotherm
        skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)
        
        # Add the relevant special lines
        skew.plot_dry_adiabats()
        skew.plot_moist_adiabats()
        skew.plot_mixing_lines()

        plt.ylim(alt[0][0], alt[0][1])


        plt.show()

        """
        #exit()
        
        #Parcel temperature
        
        cin=np.zeros((tovar.time.shape[0]))
        cap=np.zeros((tovar.time.shape[0]))
        
        #tvp=np.zeros((ex.data.shape[0],ex.z.shape[0]))
        
        #capii,cinii =   mpy.most_unstable_cape_cin(pressure[:], temperature[0,:], dw[0,:]) 
        
        #print capii,cinii
        
        for i in range(0,tovar.time.shape[0]): 
        
            #capii,cinii =   mpy.most_unstable_cape_cin(pressure[:], temperature[i,:], dw[i,:]) 
            capii,cinii =   mpy.cape_cin(pressure[:], temperature[i,:], dw[i,:],tpu[i,:]) 
        
            cap[i]=capii.magnitude
            cin[i]=cinii.magnitude
            #tvp[i,:] 	      =   mpy.virtual_potential_temperature(pressure[:], tpu[i,:],0.622) 
        
        #cap,ci 	      =   mpy.most_unstable_cape_cin(pressure, temperature, dw) 
        #print cap.shape
        
        ###############################################################

        #print(alt[0])
        #exit()
        
        ax1.set_ylabel(r'CAPE $\mathrm{ [Jkg^{-1}]}$') 
        ax2.set_ylabel( r'CIN $\mathrm{ [Jkg^{-1}]}$') 

        ax1.set_xlabel('Hours LT') 
        ax2.set_xlabel('Hours LT') 
        #print(time1,time2, alt[0][0], alt[0][1])

        #exit()
        
        #ax1.axis( [time1,time2, alt[0][0], alt[0][1]])
        #ax2.axis( [time1,time2, alt[1][0], alt[1][1]])
        
        locatormax = mdates.HourLocator(interval=2)
        locatormin = mdates.HourLocator(interval=1)

        ax1.xaxis.set_minor_locator(locatormin)
        ax2.xaxis.set_minor_locator(locatormin)

        ax1.xaxis.set_major_locator(locatormax )
        ax2.xaxis.set_major_locator(locatormax )
        
        
        line,col =color_hours(k)

        ax1.plot(time22[0:110]       ,cap[0:110]   ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')

        #ax1.plot( tovar.time[0:110]        ,tovar.CAPE[0:110]   ,label='%s'%(exp_label2[k]),color='red',linewidth=1.0,alpha=1.0,dashes=line,marker='')

        
        ax2.plot( time22[0:110]       ,-cin[0:110]        ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        #ax2.plot( tovar.time[0:110]       ,tovar.CIN[0:110]   ,label='%s'%(exp_label2[k]),color='red',linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        #####################################
        
        
        cape_all.append(cap[0:110])
        cin_all.append(cin[0:110])

        #plt.show()
        print(k ,'k')
        
        k+=1


    #average!!!
    #mean_cape=np.mean(cape_all,axis=0)
    #mean_cin =np.mean(cin_all,axis=0)

    #ax1.plot( data[0:110]       ,mean_cape[0:110]   ,color='black',linewidth=1.0,alpha=1.0,dashes=[1,0],marker='',label='Average')
    #ax2.plot( data[0:110]       ,-mean_cin[0:110]   ,color='black',linewidth=1.0,alpha=1.0,dashes=[1,0],marker='',label='Average')

    #cis1 =   (mean_cape[0:110]*0.90, mean_cape[0:110]*1.10)
    #cis2 =   (mean_cin[0:110]*0.90  , mean_cin[0:110]*1.10)

    #ax1.fill_between(data[0:110],cis1[0]  ,cis1[1],alpha=0.25,color='black')# **kw)
    #ax2.fill_between(data[0:110],-cis2[0],-cis2[1],alpha=0.25,color='black')# **kw)

    #il     = dt.datetime(2022, 1 ,1, 7) 
    #ax1.text(il,580 , r'%s'%('b)'), fontsize=9, color='black')
    #il     = dt.datetime(2022, 1 ,1, 7) 
    #ax2.text(il,105 , r'%s'%('c)'), fontsize=9, color='black')

    ax1.legend(frameon=False,loc='lower right')
    ax2.legend(frameon=False,loc='upper right')

    #fig1.savefig('%scape_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)
    #fig2.savefig('%scin_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    return  cap,cin

def cape_cin_cal(exp,hours,days,exp_label,exp_label2):


    k=0

    #Inicial hour
    hi=hours[k][0]    
    #Final hour
    hf=hours[k][1] 

    idi     = dt.datetime(2021, days[k][2] ,days[k][0], hi) 
    idf     = dt.datetime(2021, days[k][3] ,days[k][1], hf)

    #Ticks of the axisss

    ###############################################################
    fig1,ax1	=	figure_sam(0.5)
    fig2,ax2	=	figure_sam(0.5)

    ax1.axis( [idi,idf, 00.00, 650])
    
    ax1.legend(frameon=False)
    ax2.legend(frameon=False)
    
    ax1.set_ylabel(r'CAPE $\mathrm{ [Jkg^{-1}]}$') 
    ax2.set_ylabel(r'CIN $\mathrm{ [Jkg^{-1}]}$') 

    ax1.set_xlabel('Hours LT') 
    ax2.set_xlabel('Hours LT') 
    
    ax2.axis( [idi,idf, -5, 120])
    
    locatormax = mdates.HourLocator(interval=2)
    locatormin = mdates.HourLocator(interval=1)

    ax1.xaxis.set_minor_locator(locatormin)
    ax2.xaxis.set_minor_locator(locatormin)

    ax1.xaxis.set_major_locator(locatormax )
    ax2.xaxis.set_major_locator(locatormax )

    cape_all=[]
    cin_all =[]

 

    for ex in exp: 
    

        data = down.data_to_reference(ex.data)
        
        #print(ex.time[:])
        #exit()
        
        pressure       		=   units.Quantity(ex.p   ,'mbar')
        temperature    		=   units.Quantity(ex.TABS,'kelvin')
        specific_humidity	=   units.Quantity(ex.QV  ,'g/kg')
        alt            		=   units.Quantity(ex.z   ,'m')
        v_wind      		=   units.Quantity(ex.U   ,'m/seconds')
        u_wind      		=   units.Quantity(ex.V   ,'m/seconds')
        
        #Deep point temperature
        dw  	    =   mpy.dewpoint_from_specific_humidity(specific_humidity[:,:], temperature[:,:], pressure[:])
        
        cin=np.zeros((ex.data.shape[0]))
        cap=np.zeros((ex.data.shape[0]))
        
        for i in range(0,ex.data.shape[0]): 
        
            capii,cinii =   mpy.most_unstable_cape_cin(pressure[:], temperature[i,:], dw[i,:]) 
        
            cap[i]=capii.magnitude
            cin[i]=cinii.magnitude
        
        ###############################################################
        
        line,col =color_hours(k)
        
        ax1.plot( data       , cap   ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        ax2.plot( data       ,-cin   ,label='%s'%(exp_label2[k]),color=col,linewidth=1.0,alpha=1.0,dashes=line,marker='')
        
        #####################################
        
        
        cape_all.append(cap)
        cin_all.append( cin)
        
        #to save cape and cin in netcdffile
        cape_cin_netcdf(cap,cin,ex,exp_label[k]) 
        k+=1


    mean_cape=np.mean(cape_all,axis=0)
    mean_cin =np.mean(cin_all,axis=0)

    #ax1.plot( data       ,mean_cape   ,color='black',linewidth=1.0,alpha=1.0,dashes=[1,0],marker='',label='Average')
    #ax2.plot( data       ,-mean_cin   ,color='black',linewidth=1.0,alpha=1.0,dashes=[1,0],marker='',label='Average')


    #cis1 =   (mean_cape*0.90, mean_cape*1.10)
    #cis2 =   (mean_cin*0.90 , mean_cin*1.10)

    #ax1.fill_between(data, cis1[0] ,cis1[1],alpha=0.25,color='black')# **kw)
    #ax2.fill_between(data,-cis2[0],-cis2[1],alpha=0.25,color='black')# **kw)

    ax1.legend(frameon=False)
    ax2.legend(frameon=False,loc='upper right')

    #fig1.savefig('%scape_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)

    #fig2.savefig('%scin_%s.pdf'%(file_temp,exp_label[0]),bbox_inches='tight', format='pdf', dpi=1000)


    plt.show()

    return  cap,cin

def cape_cin_netcdf(cape,cin,ex,explabel):

    ## Writing NetCDF files to scam 
    #
    ## Open a new NetCDF file to write the data to. For format, you can choose from
    ## 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    
    nc_out              = Dataset('cape_cin_%s.nc'%(explabel), 'w', format='NETCDF4')
    nc_out.description  = " cape and cin calculate until deserved level"
    
    
    nc_out.history = "Created " + today.strftime("%d/%m/%y")
    nc_out.author = "Jhonatan A. A manco"
    
    
    time_nc = nc_out.createVariable('bdate', 'i4',())
    nc_out.variables['bdate'][:] =  20140101 
    
    # we can create the new dimension
    ## Even though we know the size, we are going to set the size to unknown
    nc_out.createDimension('lon', 1)
    nc_out.createDimension('lat', 1)
    
    dtime =len(ex.time)
    dlev=len(ex.p)
    nc_out.createDimension('lev',dlev )
    nc_out.createDimension('time', dtime)

    ##########################################
    #time_nc = nc_out.createVariable('time', 'f4',('time',))
    #
    ### Assign the dimension data to the new NetCDF file.
    #nc_out.variables['time'][:] = time[:]
    
    
    tsec_nc = nc_out.createVariable('time', 'f4',('time',))
    tsec_nc.setncatts({'long_name': u"Time in days since \
                        2014-01-01T00:00:00 +00:00:00 ",\
                        'units': u"s",\
                        'statistic': u'none'})
    
    
    nc_out.variables['time'][:] = ex.time[:]

    ##############################
    
    lon_nc = nc_out.createVariable('lon', 'f4', ('lon'))
    lon_nc.setncatts({'long_name': u"Longitude",\
                        'units': u"degrees",\
                        'var_desc': u"Longitude of ARM SITE MANACAPURU AMAZONAS",\
                        'statistic': u'none'})
    
    nc_out.variables['lon'][:] = -60.00
    
    ##############################
    
    lat_nc = nc_out.createVariable('lat', 'f4', ('lat'))
    lat_nc.setncatts({'long_name': u"Latitude",\
                        'units': u"degrees",\
                        'var_desc': u"latidude of ARM SITE MANACAPURU AMAZONAS",\
                        'statistic': u'none'})
    
    nc_out.variables['lat'][:] = -3.15

    ############################
    cape_nc = nc_out.createVariable('cape', 'f4', ('time','lat','lon'))
    cape_nc.setncatts({'long_name': u"Surface sensible heat flux",\
                        'units': u"Jkg^{-1}", 'level_desc': u'Surface',\
                        'var_desc': u"CAPE",\
                        'statistic': u'none\nM'})
    
    
    cape_3d=np.zeros([cape.shape[0],1,1])
    
    cape_3d[:,0,0]=cape[:]
    
    nc_out.variables['cape'][:] = cape_3d[:,0,0]

    ############################

    cin_nc = nc_out.createVariable('cin', 'f4', ('time','lat','lon'))
    cin_nc.setncatts({'long_name': u"Surface sensible heat flux",\
                        'units': u"Jkg^{-1}", 'level_desc': u'Surface',\
                        'var_desc': u"CIN",\
                        'statistic': u'none\nM'})
    
    
    cin_3d=np.zeros([cin.shape[0],1,1])
    
    cin_3d[:,0,0]=cin[:]
    
    nc_out.variables['cin'][:] = cin_3d[:,0,0]


    nc_out.close()  # close the new file
    print('Files were created' )
    print('cape_%s'%(explabel) )
    print('%s.nc'%(explabel) )
    
    
    return 



def color_hours1(hour):

    line=[1,0]
    color='k'

    if hour==0:
        line=[1,0]
        color='blue'
    elif  hour==1:
        line=[1,0]
        color='orange'
    elif hour==2:
        line=[1,0]
        color='m'
    elif  hour==3:
        line=[1,0]
        color='r'
    elif  hour==4:
        line=[4, 1]
        color='green'
    elif  hour==5:
        line=[1,1]
        color='tab:orange'
    elif  hour==6:
        line=[1,2,1,2]
        color='m'
    elif  hour==7:
        line=[2,1,1,3]
        color='tab:brown'
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

def color_hours(hour):

    line=[1,0]
    color='k'

    if hour==0:
        line=[1,0]
        color='blue'
    elif  hour==1:
        line=[1,0]
        color='orange'
    elif hour==2:
        line=[1,0]
        color='r'
    elif  hour==3:
        line=[1,0]
        color='g'
    elif  hour==4:
        line=[4, 1]
        color='green'
    elif  hour==5:
        line=[1,1]
        color='tab:orange'
    elif  hour==6:
        line=[1,2,1,2]
        color='m'
    elif  hour==7:
        line=[2,1,1,3]
        color='tab:brown'
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
