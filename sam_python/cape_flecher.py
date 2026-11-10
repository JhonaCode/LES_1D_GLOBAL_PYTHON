########################################################
#Program to calculate the CIN 
# and the mass flux closure 
#based on the paper: 
#Evaluating Boundary Layer-Based Mass Flux
#Closures using cloud resolving model simulation
#of deep convection.
#Flecher and Bretherton
########################################################
#Data:05/09/22
#Created by: Jhonatan A. A. Manco
########################################################
#python version: 3.8
########################################################
import  figure_own           as fown

import  metpy.calc as mpy

from    metpy.plots import add_metpy_logo, SkewT

from    metpy.units import units

# Python standard library datetime  module
import datetime as dt  

##Function to trandfform data in indices 
import data_own as down

import numpy as np

import  matplotlib.pyplot as plt

#to work with date in plots
import matplotlib.dates as mdates

from   	plotparameters 		import 	*

import  matplotlib as mpl

from  figure_own import * 
  
from files_direction import *

# Python library to work with Netcdf4 
from    netCDF4         import Dataset

# To save the time coordinate in specific format 
from    netCDF4         import num2date, date2num

#integration 
import scipy.integrate as integrate


from scipy.stats import pearsonr,spearmanr,kendalltau

import seaborn as sb

#not a number
import math

today = dt.datetime.today()

def cin_flecher_cases(exp,days,exp_label,exp_label2,exp_case):


    k=0

    data=[]

    tvmin       =[]
    cb          =[]
    ct          =[]
    z0_all      =[]


    cin         =[]
    tke         =[]
    tke_cloud   =[]
    tke_all     =[]
    mfi         =[]
    eq1_all         =[]
    eq2_all         =[]
    eq3_all         =[]

    cin_iop1        =[]
    tke_iop1        =[]
    tke_cloud_iop1  =[]
    tke_all_iop1    =[]
    mfi_iop1        =[]
    eq1_iop1        =[]
    eq2_iop1        =[]
    eq3_iop1        =[]
    data_iop1       =[]

    cin_amz        =[]
    tke_amz        =[]
    tke_cloud_amz  =[]
    tke_all_amz    =[]
    mfi_amz        =[]
    eq1_amz        =[]
    eq2_amz        =[]
    eq3_amz        =[]
    data_amz       =[]


    cin_iop2        =[]
    tke_iop2        =[]
    tke_cloud_iop2  =[]
    tke_all_iop2    =[]
    mfi_iop2        =[]
    eq1_iop2        =[]
    eq2_iop2        =[]
    eq3_iop2        =[]
    data_iop2       =[]

    cin_lall        =[]
    tke_lall        =[]
    tke_cloud_lall  =[]
    tke_all_lall    =[]
    mfi_lall        =[]
    eq1_lall        =[]
    eq2_lall        =[]
    eq3_lall        =[]
    data_lall       =[]

    cin_lrn        =[]
    tke_lrn        =[]
    tke_cloud_lrn  =[]
    tke_all_lrn     =[]
    mfi_lrn        =[]
    eq1_lrn        =[]
    eq2_lrn        =[]
    eq3_lrn        =[]
    data_lrn       =[]

    cin_lnr        =[]
    tke_lnr        =[]
    tke_cloud_lnr  =[]
    tke_all_lnr     =[]
    mfi_lnr        =[]
    eq1_lnr        =[]
    eq2_lnr        =[]
    eq3_lnr        =[]
    data_lnr       =[]

    cin_m        =[]
    tke_m        =[]
    tke_cloud_m  =[]
    tke_all_m     =[]
    mfi_m        =[]
    eq1_m        =[]
    eq2_m        =[]
    eq3_m        =[]
    data_m        =[]

    cin_s        =[]
    tke_s        =[]
    tke_cloud_s  =[]
    tke_all_s  =[]
    tke_nr_s     =[]
    mfi_s        =[]
    eq1_s        =[]
    eq2_s        =[]
    eq3_s        =[]
    data_s       =[]


    color   =[]
    marker  =[]
    alpha   =[]
    psize   =[]

    for ex in exp: 
    

        idi     = dt.datetime(days[k][0], days[k][1] ,days[k][2], days[k][3]) 
        idf     = dt.datetime(days[k][4], days[k][5] ,days[k][6], days[k][7])

        ni,nf= down.data_n(idi,idf,ex.data[:])

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
        specific_humidit_t	=   units.Quantity(ex.QT  ,'g/kg')

        alt            		=   units.Quantity(ex.z   ,'m')
        v_wind      		=   units.Quantity(ex.U   ,'m/seconds')
        u_wind      		=   units.Quantity(ex.V   ,'m/seconds')

        #Deep point temperature
        dw   	    =   mpy.dewpoint_from_specific_humidity( pressure[:], temperature[:,:],specific_humidity_v[:,:])

        mxr         =   mpy.mixing_ratio_from_specific_humidity(specific_humidity_v[:,:])
        tv          =   mpy.virtual_temperature(temperature[:,:],mxr[:])


        theta=np.zeros((ex.data.shape[0],ex.z.shape[0]))



        #funcionando arm e kwajex
        #z1,z2=down.level_n(200,500,ex.z)
        #z3   =len(pressure)
        #z0,z4=down.level_n(300,600,ex.z)

        #funcionando goamazon shallow
        z1,z2=down.level_n(200,450,ex.z)
        z3   =len(pressure)
        z0,z4=down.level_n(320,600,ex.z)


        #t1   =   ex.data.shape[0]        
        t1   =   nf-ni        

        mean_theta  =   np.zeros(t1)
        mean_temp   =   np.zeros(t1)
        mean_mxr    =   np.zeros(t1)
        mean_spec   =   np.zeros(t1)

        tp =np.zeros((t1,z3-z0))
        tv =np.zeros((t1,z3-z0))
        tvp=np.zeros((t1,z3-z0))

        cin_flecher =   np.zeros(t1)
        tke_pbl     =   np.zeros(t1)
        mtke_cloud  =   np.zeros(t1)
        mtke_all    =   np.zeros(t1)
        mf          =   np.zeros(t1)

        #for i in range(0,ex.data.shape[0]): 
        jj=0

        for i in range(ni,nf,1): 

            mean_mxr[jj]   =   np.mean(mxr[i,z1:z2].magnitude)*(units('g/kg')) 
            
            #standar deviation
            qv_s          =   np.std(specific_humidity_v[i,z1:z2].magnitude,axis=0)
            
            mean_spec[jj]  =   (np.mean(specific_humidity_v[i,z1:z2].magnitude)+qv_s)*(units('g/kg')) 
            
            
            temp          =   np.mean(temperature[i,z1:z2])
            dwp           =   mpy.dewpoint_from_specific_humidity( pressure[z1],temp,mean_spec[jj])#.magnitude
            
            
            #calculate before cin
            tp[jj,:]      =   mpy.parcel_profile(pressure[z0:z3], temp, dwp) 
            tvp           =   mpy.virtual_temperature(tp[jj,:]*units('kelvin') ,mxr[i,z0:z3] ) 
            tv            =   mpy.virtual_temperature(temperature[i,z0:z3],mxr[i,z0:z3] ) 
            
            thetav        =   mpy.virtual_potential_temperature(pressure[z0:z3], temperature[i,z0:z3],mxr[i,z0:z3]) 
            thetavp       =   mpy.virtual_potential_temperature(pressure[z0:z3], tp[jj,:]*units('kelvin'),mxr[i,z0:z3]) 
            
            
            lcl_m         =   mpy.lcl(pressure[z0], temp, dwp,max_iters=50,eps=1e-5)
            
            lcl           =   lcl_m[0]
            
            lfc_c         =   mpy.lfc(pressure[z0:z3],temperature[i,z0:z3],dw[i,z0:z3],which='top')
            lfc        =   lfc_c[0].magnitude
            
            #l1            =   mpy.pressure_to_height_std(lcl).to('m').magnitude
            #print(l1)
            #print(ex.z[:],ex.p[:])
            #l1=int(np.mean([l11-1,l11,l11+1]))
            
            
            l1   ,l2      =   down.pressure_n(lcl.magnitude,lfc,pressure[:].magnitude,ex)
            
            #if l1<=z0:
            #    l1+=2

            zn0       =   ex.z[z0:l1+1]
            l3       =   len(zn0)
            
            zn2       =   ex.z[z0:l2+1]
            l4       =   len(zn2)
            
            ipblh    =   np.argmin(ex.TVFLUX[i,1:30])
            imc      =   np.argmax(ex.MCUP[i][0:30]) 
            imc      =   ipblh+1 

            
            #if ex.MC[i,ipblh]>0.005:
            if ex.MC[i,l1]>0.005:
            #if ex.MC[i,imc]>0.005:
            #if 5>0.001:

                inte_0       =   (tvp[0:l3]  -tv[0:l3]  )/(tv[0:l3])
                inte_1       =   (tvp[0:l3+1]-tv[0:l3+1])/(tv[0:l3+1])
                inte_2       =   (tvp[0:l3-1]-tv[0:l3-1])/(tv[0:l3-1])
                #inte_3       =   (tvp[0:l3+2]-tv[0:l3+2])/(tv[0:l3+2])
                #inte_4       =   (tvp[0:l3-2]-tv[0:l3-2])/(tv[0:l3-2])

                #inte_cin=(inte_cin_0+inte_cin_1+inte_cin_2)/3.0
                #inte_cin=(inte_cin_0+inte_cin_1+inte_cin_2+inte_cin_3)/4.0
                #inte_cin       =   (thetavp[0:l3]-thetav[0:l3])/(thetav[0:l3])
                inte_cin_0=-9.81*integrate.simps(inte_0,zn0)

                zn1       =   ex.z[z0:l1+2]
                inte_cin_1=-9.81*integrate.simps(inte_1,zn1)

                zn2       =   ex.z[z0:l1]
                inte_cin_2=-9.81*integrate.simps(inte_2,zn2)

                #zn3       =   ex.z[z0:l1+3]
                #inte_cin_3=-9.81*integrate.simps(inte_3,zn3)

                #zn4       =   ex.z[z0:l1-1]
                #inte_cin_4=-9.81*integrate.simps(inte_4,zn4)

                #cin_flecher[jj]=   (inte_cin_0+inte_cin_1+inte_cin_2+inte_cin_3+inte_cin_4)/5.0
                #cin_flecher[jj]=   (inte_cin_0+inte_cin_1+inte_cin_2)/3.0
                cin_flecher[jj]=   inte_cin_0
                rho            =   ex.RHO[i,l1]

                #fig,ax =fown.figure_scatter(0.8)
                #plt.plot(thetav       ,ex.z[z0:z3],'m',label='thetav ')
                #plt.plot(thetavp      ,ex.z[z0:z3],'b',label='thetavp')
                #plt.plot(thetavp[0]   ,ex.z[z0]   ,'+',label='init parcel')
                #plt.plot(thetavp[l3-1],zn1[l3-1]   ,'o',label='lcl  parcel')
                #plt.plot(thetav[0]    ,ex.z[z0]   ,'*',label='init tv')
                #plt.plot(thetav[l3-1] ,zn1[l3-1]   ,'p',label='end tv')
                #plt.plot(thetav[l4-1] ,ex.z[l2]   ,'p',label='lfc tv')
                #plt.plot(thetavp[l4-1] ,ex.z[l2]   ,'p',label='lfc tv parcel')
                #ax.legend(frameon=False,loc='upper right')
                #plt.show()
                
                if ipblh<=z0:
                    tke_pbl[jj]   =ex.TKE[i,ipblh]   
                else: 
                    tke_pbl[jj]   =   1.0/(ex.z[ipblh]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:ipblh],ex.z[z0:ipblh])
                    #tke_pbl[jj]   =   1.0/(ex.z[l1]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:l1],ex.z[z0:l1])

                #eq1           =   0.4*(0.28*np.sqrt(tke_pbl[jj])+0.64)*np.exp(-0.5*cin_flecher[jj]/tke_pbl[jj] )
                eq1           =   0.06*(0.28*np.sqrt(tke_pbl[jj])+0.64)*np.exp(-0.0*np.abs(cin_flecher[jj])/tke_pbl[jj] )

                eq2           =   0.4*rho*(np.sqrt(tke_pbl[jj]   ))*np.exp(-0.9*cin_flecher[jj]/tke_pbl[jj] )

                kf=0.15
                #eq3           =   0.4*rho*(np.sqrt(tke_pbl[jj]   ))*np.exp(-1.0/tke_pbl[jj]   )
                eq3           =   rho*(np.sqrt(kf*tke_pbl[jj]/(2.0*math.pi)))*np.exp(-0.04/(kf*tke_pbl[jj]))

                #kf=0.10
                #eq3           =   rho*(np.sqrt(kf*tke_pbl[jj]/(2.0*math.pi)))*np.exp(-0.04/(kf*tke_pbl[jj]))
                #kf=0.10
                #eq4           =   rho*(np.sqrt(kf*tke_pbl[jj]/(2.0*math.pi)))*np.exp(-1.0*np.abs(cin_flecher[jj])/(kf*tke_pbl[jj]))

            
                #to chosse the mean point from MCUP LES simulation
                mp=1


                data.append( ex.data[i]   )
                cin.append ( cin_flecher[jj]  )
                tke.append ( tke_pbl[jj]      )
                mfi.append ( ex.MCUP[i,l1+1]  )
                eq1_all.append ( eq1  )
                eq2_all.append ( eq2  )
                eq3_all.append ( eq3  )
                #mfi.append ( np.mean(ex.MCUP[i,l1-mp:l1+mp]))
                #mfi.append ( ex.MC[i,imc])

                cb.append(ex.z[l1])
                tvmin.append(ex.z[ipblh])
                z0_all.append(ex.z[z0])

                if exp_case[k]=='shca_nr':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_amz.append(cin_flecher[jj])
                    tke_amz.append(tke_pbl[jj])
                    mfi_amz.append(ex.MCUP[i,l1+1])
                    #mfi_amz.append(np.mean(ex.MCUP[i,l1-mp:l1+mp]))
                    #mfi_amz.append(ex.MCUP[i,imc])
                    eq1_amz.append(eq1)
                    eq2_amz.append(eq2)
                    eq3_amz.append(eq3)
                    data_amz.append( ex.data[i]   )

                if exp_case[k]=='iop1':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_iop1.append(cin_flecher[jj])
                    tke_iop1.append(tke_pbl[jj])
                    mfi_iop1.append(ex.MCUP[i,l1+1])
                    #mfi_iop1.append(np.mean(ex.MCUP[i,l1-mp:l1+mp]))
                    #mfi_iop1.append(ex.MC[i,imc])
                    eq1_iop1.append(eq1)
                    eq2_iop1.append(eq2)
                    eq3_iop1.append(eq3)
                    data_iop1.append( ex.data[i]   )

                if exp_case[k]=='iop2':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_iop2.append(cin_flecher[jj])
                    tke_iop2.append(tke_pbl[jj])
                    mfi_iop2.append(ex.MCUP[i,l1+1])
                    #mfi_iop2.append(np.mean(ex.MCUP[i,l1-mp:l1+mp]))
                    #mfi_iop2.append(ex.MC[i,imc])
                    eq1_iop2.append(eq1)
                    eq2_iop2.append(eq2)
                    eq3_iop2.append(eq3)
                    data_iop2.append( ex.data[i]   )

                if exp_case[k]=='large_all':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_lall.append(cin_flecher[jj])
                    tke_lall.append(tke_pbl[jj])
                    mfi_lall.append(ex.MCUP[i,l1+1])
                    #mfi_lall.append(np.mean(ex.MCUP[i,l1-mp:l1+mp]))
                    #mfi_lall.append(ex.MC[i,imc])
                    eq1_lall.append(eq1)
                    eq2_lall.append(eq2)
                    eq3_lall.append(eq3)
                    data_lall.append( ex.data[i]   )

                if exp_case[k]=='large_rn':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_lrn.append(cin_flecher[jj])
                    tke_lrn.append(tke_pbl[jj])
                    mfi_lrn.append(ex.MCUP[i,l1+1])
                    #mfi_lrn.append(np.mean(ex.MCUP[i,l1-mp:l1+mp]))
                    #mfi_lrn.append(ex.MC[i,imc])
                    eq1_lrn.append(eq1)
                    eq2_lrn.append(eq2)
                    eq3_lrn.append(eq3)
                    data_lrn.append( ex.data[i]   )

                if exp_case[k]=='large_nr':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_lnr.append(cin_flecher[jj])
                    tke_lnr.append(tke_pbl[jj])
                    mfi_lnr.append(ex.MCUP[i,l1+1])
                    #mfi_lnr.append(np.mean(ex.MCUP[i,l1-mp:l1+mp]))
                    #mfi_lnr.append(ex.MC[i,imc])
                    eq1_lnr.append(eq1)
                    eq2_lnr.append(eq2)
                    eq3_lnr.append(eq3)
                    data_lnr.append( ex.data[i]   )

                if exp_case[k]=='medium':
                    col='yellow'
                    mark='*'
                    alp=0.5
                    ps=20
                    cin_m.append(cin_flecher[jj])
                    tke_m.append(tke_pbl[jj])
                    mfi_m.append(ex.MCUP[i,l1+1])
                    #mfi_m.append(np.mean(ex.MC[i,l1-mp:l1+mp]))
                    #mfi_m.append(ex.MC[i,imc])
                    eq1_m.append(eq1)
                    eq2_m.append(eq2)
                    eq3_m.append(eq3)
                    data_m.append( ex.data[i]   )

                if exp_case[k]=='small':
                    col='blue'
                    mark='d'
                    alp=0.5
                    ps=20
                    cin_s.append(cin_flecher[jj])
                    tke_s.append(tke_pbl[jj])
                    mfi_s.append(ex.MCUP[i,l1+1])
                    #mfi_s.append(np.mean(ex.MC[i,l1-mp:l1+mp]))
                    #mfi_s.append(ex.MC[i,imc])
                    eq1_s.append(eq1)
                    eq2_s.append(eq2)
                    eq3_s.append(eq3)
                    data_s.append( ex.data[i]   )

                if exp_case[k]=='test':
                    col='white'
                    mark='p'
                    alp=0.3
                    ps=0.1

                color.append(col)
                marker.append(mark)
                alpha.append(alp)
                psize.append(ps)


            jj+=1

        #fig,ax =fown.figure_sam(0.8)
        #plt.plot(data,z0_all,'m',label='z0')
        #plt.plot(data,cb    ,'r',label='lcl')
        #plt.plot(data,tvmin ,'k',label='tvmin')
        #ax.legend(frameon=False,loc='upper right')
        #plt.show()


        #to plot the cin and sqrt cin 
        #fig = plt.figure()
        #####New axis
        #ax  = plt.axes()
        #plt.plot(data,cin, marker='*' ,color='red',label=' CIN Flecher')
        #plt.plot(data,np.sqrt(1.0*np.array(cin)), marker='o' ,color='blue',label=' sqrt(CIN) ')
        ##plt.plot(ex.data[ni:nf],cin_flecher[:], marker='*' ,color='red',label=' CIN Flecher')
        ##plt.plot(data,cin[:], marker='*' ,color='blue',label=' CIN Flecher')
        ##plt.plot(ex.data[ni:nf],tke_pbl[:], marker='*' ,color='red',label=' CIN Flecher')
        ##plt.plot(ex.data[ni:nf],cin_flecher[:], marker='*' ,color='red',label=' CIN Flecher')
        ##plt.plot(data,0.4*np.sqrt(np.array(tke))*np.exp(-np.array(cin)/np.array(tke)), marker='*' ,color='blue',label='UW')
        ##plt.plot(data,0.06*(0.28*np.sqrt(np.array(tke))+0.64)*np.exp(-np.array(cin)/np.array(tke)), marker='*' ,color='red',label='Fletcher')
        #fig,ax =fown.figure_scatter(0.5)
        #ax.axis( [0,1.5,0,8])
        #ax.text( 0.2,7,'Sh IOP1 e IOP2')
        #ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
        #ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
        #ax.scatter(tke_1,cin_1,marker='o',facecolors='none',edgecolors='blue'  ,s=5, label='IOP1')
        #ax.scatter(tke_2,cin_2,marker='*',color='k'        ,s=5, label='IOP2')
        #ax.legend(frameon=False,loc='upper right')
        ##fig.savefig('%sscatter_cin_tke_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)
        #plt.show()


        k=k+1

    #to plot the cb and tvmin

    #fig,ax =fown.figure_sam(0.8)
    ##plt.plot(data,z0_all,'m',label='z0')
    #plt.plot(data,cb    ,'r',label='lcl')
    ##plt.plot(data,ct    ,'g',label='cloud top')
    #plt.plot(data,tvmin ,'k',label='tvmin')
    #ax.legend(frameon=False,loc='upper right')
    #plt.show()


    ###############
    #call, sall = pearsonr(tke,cin)
    #print('all',call)

    #clall, slall = pearsonr(tke_lall,cin_lall)
    #print('large all',clall)

    #cm  , sm   = pearsonr(tke_m,cin_m)
    #print('medium',cm)

    #cs  , ss   = pearsonr(tke_s,cin_s)
    #print('small',cs)


    #########################################
    #########################################
    #call, sall = pearsonr(mfi,tke)
    #print('mf tke all',call)

    #c_iop1, sall = pearsonr(mfi_1,tke_1)
    #print('mf tke iop1',c_iop1)

    #c_iop1, sall = pearsonr(mfi_2,tke_2)
    #print('mf tke iop2',c_iop2)

    #clall, slall = pearsonr(mfi_lall,tke_lall)
    #print('mf tke large all',clall)

    #clrn, slrn = pearsonr(mfi_lrn,tke_lrn)
    #print('mf tke large rain',clrn)

    #clnr, slnr = pearsonr(mfi_lnr,tke_lnr)
    #print('mf tke large not rain',clnr)

    #cm  , sm   = pearsonr(mfi_m,tke_m)
    #print('mf tke medium',cm)

    #cs  , ss   = pearsonr(mfi_s,tke_s)
    #print('mf tke small',cs)


    #fig,ax =fown.figure_scatter(0.4)
    #ax.axis( [0,1.5,0,8])
    #ax.text( 0.1,7,'c) Large ')
    #ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    #ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    #ax.scatter(tke_iop1,cin_iop1  ,marker='s',facecolors='none',edgecolors='black' ,s=4, label='IOP1')
    #ax.scatter(tke_iop2,cin_iop2  ,marker='s',facecolors='none',edgecolors='red' ,s=4, label='IOP2')
    #ax.scatter(tke_lrn,cin_lrn  ,marker='s',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    #ax.scatter(tke_lnr,cin_lnr  ,marker='o',facecolors='none',edgecolors='cyan'    ,s=4, label='Not Rain')
    #ax.scatter(tke_lall,cin_lall,marker='p',facecolors='none',edgecolors='m'    ,s=4, label='All')
    #ax.scatter(tke_m,cin_m,marker='P',facecolors='none',edgecolors='g'    ,s=4, label='medium')
    #ax.scatter(tke_s,cin_s,marker='*',facecolors='none',edgecolors='y'    ,s=4, label='small')
    #ax.legend(frameon=False,loc='upper right')
    #fig.savefig('%sscatter_cin_tke_%s.pdf'%(file_temp,exp_label2[0]),bbox_inches='tight', format='pdf', dpi=1000)

    npt=1

    ###############
    call, sall = pearsonr(tke[::npt],cin[::npt])
    print('all',call)

    camz, samz = pearsonr(tke_amz[::npt],cin_amz[::npt])
    print('amazon',camz)

    clall, slall = pearsonr(tke_lall[::npt],cin_lall[::npt])
    print('large all',clall)

    cm  , sm   = pearsonr(tke_m[::npt],cin_m[::npt])
    print('medium',cm)

    cs  , ss   = pearsonr(tke_s[::npt],cin_s[::npt])
    print('small',cs)


    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,4])
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    ax.text( 0.1,2.8,'R=%5.2f'%(call), fontsize=6)
    ax.text( 0.1,3.0,'a) ')

    ax.scatter(tke_amz ,cin_amz ,marker='s',facecolors='none',edgecolors='green'   ,s=4, label='Amazon')
    ax.scatter(tke_lall,cin_lall,marker='p',facecolors='none',edgecolors='red'    ,s=4, label='Large')
    ax.scatter(tke_m,cin_m,marker='P',facecolors='none',edgecolors='orange'    ,s=4, label='Medium')
    ax.scatter(tke_s,cin_s,marker='o',facecolors='none',edgecolors='b'    ,s=4, label='Small')
    ax.legend(frameon=False,loc='upper right')

    fig.savefig('%sscatter_cin_tke_%s.pdf'%(file_temp,exp_label2[0]),bbox_inches='tight', format='pdf', dpi=1000)

    ###############
    ###############
    call, sall = pearsonr(mfi[::npt],cin[::npt])
    print('all',call)

    camz, samz = pearsonr(mfi_amz[::npt],cin_amz[::npt])
    print('amazon',camz)

    clall, slall = pearsonr(mfi_lall[::npt],cin_lall[::npt])
    print('large all',clall)

    cm  , sm   = pearsonr(mfi_m[::npt],cin_m[::npt])
    print('medium',cm)

    cs  , ss   = pearsonr(mfi_s[::npt],cin_s[::npt])
    print('small',cs)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.15,0,4])
    #ax.text( 0.1,7,'')

    ax.set_xlabel(r'uMf [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 

    ax.text( 0.01,3.0,'b) ')
    ax.text( 0.01,2.8,'R=%5.2f'%(call), fontsize=6)

    ax.scatter(mfi_amz[::npt] ,cin_amz[::npt] ,marker='s',facecolors='none',edgecolors='green'   ,s=4, label='Amazon')
    ax.scatter(mfi_lall[::npt],cin_lall[::npt],marker='p',facecolors='none',edgecolors='red'    ,s=4, label='Large')
    ax.scatter(mfi_m[::npt],cin_m[::npt],marker='P',facecolors='none',edgecolors='orange'    ,s=4, label='Medium')
    ax.scatter(mfi_s[::npt],cin_s[::npt],marker='o',facecolors='none',edgecolors='b'    ,s=4, label='Small')
    ax.legend(frameon=False,loc='upper right')

    fig.savefig('%sscatter_mf_cin_tke_%s.pdf'%(file_temp,exp_label2[0]),bbox_inches='tight', format='pdf', dpi=1000)

    #############################
    #############################
    #############################

    call, sall = pearsonr(mfi[::npt],tke[::npt])
    print('all',call)

    camz, samz = pearsonr(mfi_amz[::npt],tke_amz[::npt])
    print('amazon',camz)

    clall, slall = pearsonr(mfi_lall[::npt],tke_lall[::npt])
    print('large all',clall)

    cm  , sm   = pearsonr(mfi_m[::npt],tke_m[::npt])
    print('medium',cm)

    cs  , ss   = pearsonr(mfi_s[::npt],tke_s[::npt])
    print('small',cs)


    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.15,0,2])
    #ax.text( 0.1,7,'')
    ax.text( 0.01,1.8,'R=%5.2f'%(call), fontsize=6)
    ax.text( 0.01,1.6,'c) ')

    ax.set_xlabel(r'uMf [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'TKE [$\mathrm{ms^{-1}}$]') 

    ax.scatter(mfi_amz[::npt] ,tke_amz[::npt] ,marker='s',facecolors='none',edgecolors='green'   ,s=4, label='Amazon')
    ax.scatter(mfi_lall[::npt],tke_lall[::npt],marker='p',facecolors='none',edgecolors='red'    ,s=4, label='Large')
    ax.scatter(mfi_m[::npt],tke_m[::npt],marker='P',facecolors='none',edgecolors='orange'    ,s=4, label='Medium')
    ax.scatter(mfi_s[::npt],tke_s[::npt],marker='o',facecolors='none',edgecolors='b'    ,s=4, label='Small')
    ax.legend(frameon=False,loc='upper right')

    fig.savefig('%sscatter_mf_tke_tke_%s.pdf'%(file_temp,exp_label2[0]),bbox_inches='tight', format='pdf', dpi=1000)



    npt=2

    ##############################################3
    ##############################################3
    ##############################################3

    call, sall = pearsonr(mfi[::npt],eq1_all[::npt])
    print('eq1 all',call)

    camz, samz = pearsonr(mfi_amz[::npt],eq1_amz[::npt])
    print('eq1 amazon',camz)

    clall, slall = pearsonr(mfi_lall[::npt],eq1_lall[::npt])
    print('eq1 large all',clall)

    cm  , sm   = pearsonr(mfi_m[::npt],eq1_m[::npt])
    print('eq1 medium',cm)

    cs  , ss   = pearsonr(mfi_s[::npt],eq1_s[::npt])
    print('eq1 small',cs)

    #fig,ax =fown.figure_scatter(0.4)
    #ax.axis( [0,0.15,0,2])
    #ax.text( 0.1,7,'')

    fig,ax =fown.figure_sam(0.4)
    #ax.axis( [0,0.1,0,4])
    #ax.text( 0.1,7,'')
    ax.text( data_amz[1],0.01,'R=%5.2f'%(call), fontsize=6)

    ax.set_xlabel(r'hour LT ') 
    ax.set_ylabel(r'uMf [$\mathrm{ms^{-1}}$]') 

    ax.scatter(data_amz[::npt] ,eq1_amz[::npt] ,marker='.',color='green',alpha=0.8  , label='Amazon')
    ax.plot(data_amz[::npt] ,mfi_amz[::npt] ,marker='',color='green' )

    ax.scatter(data_lall[::npt],eq1_lall[::npt],marker='.',color='red'   ,alpha=0.8  , label='Large')
    ax.plot(data_lall[::npt],mfi_lall[::npt],marker='',color='red'   )

    ax.scatter(data_m[::npt]   ,eq1_m[::npt]   ,marker='.',color='orange',alpha=0.8 , label='Medium')
    ax.plot(data_m[::npt]   ,mfi_m[::npt]   ,marker='',color='orange')

    ax.scatter(data_s[::npt]   ,eq1_s[::npt]   ,marker='.',color='b'     ,alpha=0.8     , label='Small')
    ax.plot(data_s[::npt]   ,mfi_s[::npt]   ,marker='',color='b'     )

    fig.savefig('%stemporal_eq1_mf_%s.pdf'%(file_temp,exp_label2[0]),bbox_inches='tight', format='pdf', dpi=1000)

    ##############################################3
    ##############################################3
    ##############################################3

    fig,ax =fown.figure_sam(0.4)

    call, sall = pearsonr(mfi,eq2_all)
    print('eq2 all',call)
    #ax.axis( [0,0.1,0,4])
    #ax.text( 0.1,7,'')
    camz, samz = pearsonr(mfi_amz,eq2_amz)
    print('eq2 amazon',camz)

    clall, slall = pearsonr(mfi_lall,eq2_lall)
    print('eq2 large all',clall)

    cm  , sm   = pearsonr(mfi_m,eq2_m)
    print('eq2 medium',cm)

    cs  , ss   = pearsonr(mfi_s,eq2_s)
    print('eq2 small',cs)

    ax.set_xlabel(r'hour LT ') 
    ax.set_ylabel(r'uMf [$\mathrm{ms^{-1}}$]') 
    ax.text( data_amz[1],0.01,'R=%5.2f'%(call), fontsize=6)

    ax.scatter(data_amz[::npt] ,eq2_amz[::npt] ,marker='.',color='green' ,alpha=0.8, label='Amazon')
    ax.plot(data_amz[::npt] ,mfi_amz[::npt] ,marker='',color='green' )

    ax.scatter(data_lall[::npt],eq2_lall[::npt],marker='.',color='red'   ,alpha=0.8, label='Large')
    ax.plot(data_lall[::npt],mfi_lall[::npt],marker='',color='red'   )

    ax.scatter(data_m[::npt]   ,eq2_m[::npt]   ,marker='.',color='orange',alpha=0.8, label='Medium')
    ax.plot(data_m[::npt]   ,mfi_m[::npt]   ,marker='',color='orange')

    ax.scatter(data_s[::npt]  ,eq2_s[::npt]   ,marker='.',color='b'    ,alpha=0.8  , label='Small')
    ax.plot(data_s[::npt]   ,mfi_s[::npt]   ,marker='',color='b'     )

    fig.savefig('%stemporal_eq2_mf_%s.pdf'%(file_temp,exp_label2[0]),bbox_inches='tight', format='pdf', dpi=1000)

    ##############################################3
    ##############################################3
    ##############################################3
    fig,ax =fown.figure_sam(0.4)
    #ax.axis( [0,0.1,0,4])
    #ax.text( 0.1,7,'')

    call, sall = pearsonr(mfi,eq3_all)
    print('eq3 all',call)

    camz, samz = pearsonr(mfi_amz,eq3_amz)
    print('eq3 amazon',camz)

    clall, slall = pearsonr(mfi_lall,eq3_lall)
    print('eq3 large all',clall)

    cm  , sm   = pearsonr(mfi_m,eq3_m)
    print('eq3 medium',cm)

    cs  , ss   = pearsonr(mfi_s,eq3_s)
    print('eq3 small',cs)

    ax.set_xlabel(r'hour LT ') 
    ax.set_ylabel(r'uMf [$\mathrm{ms^{-1}}$]') 

    ax.text( data_amz[1],0.01,'R=%5.2f'%(call), fontsize=6)

    ax.scatter(data_amz[::npt]  ,eq3_amz[::npt] ,color='green' ,marker='.',alpha=0.8 , label='Amazon')
    ax.plot(data_amz[::npt] ,mfi_amz[::npt] ,color='green',marker='' )

    ax.scatter(data_lall[::npt],eq3_lall[::npt],color='red'  ,marker='.' ,alpha=0.8, label='Large')
    ax.plot(data_lall[::npt],mfi_lall[::npt],color='red' ,marker=''  )

    ax.scatter(data_m[::npt]    ,eq3_m[::npt]  ,color='orange',marker='.',alpha=0.8, label='Medium')
    ax.plot(data_m[::npt]   ,mfi_m[::npt]   ,color='orange',marker='' )

    ax.scatter(data_s[::npt]    ,eq3_s[::npt]  ,color='b' ,marker='.'   ,alpha=0.8  , label='Small')
    ax.plot(data_s[::npt]   ,mfi_s[::npt]   ,color='b',marker=''     )

    ax.legend(frameon=False,loc='upper right')

    fig.savefig('%stemporal_eq3_mf_%s.pdf'%(file_temp,exp_label2[0]),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    exit()

    #############################
    #############################

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,7,'c) Large ')
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    ax.scatter(tke_cloud_lrn,cin_lrn,marker='s',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(tke_cloud_lnr,cin_lnr,marker='o',facecolors='none',edgecolors='k'    ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_tke_cloud_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,0.15])
    ax.text(  0.1,0.13,'b) Medium')
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'Mup [$\mathrm{ms^{-1}}$]') 
    ax.scatter(tke_m,mfi_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_mf_tke_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    return cin

def cin_uw_z0(exp,days,exp_label,exp_case):


    k=0

    data=[]

    tvmin   =[]
    cb      =[]
    ct      =[]
    z0_all  =[]

    cin =[]
    cin_1 =[]
    cin_2 =[]
    cin_l=[]
    cin_lrn=[]
    cin_lnr=[]
    cin_lall=[]
    cin_m=[]
    cin_s=[]

    cin_uw =[]
    cin_uw_1 =[]
    cin_uw_2 =[]
    cin_uw_l=[]
    cin_uw_lrn=[]
    cin_uw_lnr=[]
    cin_uw_lall=[]
    cin_uw_m=[]
    cin_uw_s=[]

    tke =[]
    tke_1 =[]
    tke_2 =[]
    tke_l =[]
    tke_lrn =[]
    tke_lnr =[]
    tke_lall =[]
    tke_m =[]
    tke_s =[]

    tke_cloud =[]
    tke_cloud_1 =[]
    tke_cloud_2 =[]
    tke_cloud_l =[]
    tke_cloud_lrn =[]
    tke_cloud_lnr =[]
    tke_cloud_lall =[]
    tke_cloud_m =[]
    tke_cloud_s =[]

    tke_all   =[]
    tke_all_1 =[]
    tke_all_2 =[]
    tke_all_l =[]
    tke_all_lrn =[]
    tke_all_lnr =[]
    tke_all_lall=[]
    tke_all_m =[]
    tke_all_s =[]

    mc      =[]
    mfi     =[]
    mfi_1   =[]
    mfi_2   =[]
    mfi_l   =[]
    mfi_lrn =[]
    mfi_lnr =[]
    mfi_lall=[]
    mfi_m   =[]
    mfi_s   =[]
    mfi2    =[]
    mfi3    =[]
    mup     =[]

    eq1_all =[]
    eq1_1   =[]
    eq1_2   =[]
    eq1_l   =[]
    eq1_lrn =[]
    eq1_lnr =[]
    eq1_lall=[]
    eq1_m   =[]
    eq1_s   =[]

    eq2_all =[]
    eq2_1   =[]
    eq2_2   =[]
    eq2_l   =[]
    eq2_lrn =[]
    eq2_lnr =[]
    eq2_lall=[]
    eq2_m   =[]
    eq2_s   =[]

    eq3_all   =[]
    eq3_1   =[]
    eq3_2   =[]
    eq3_l   =[]
    eq3_lrn =[]
    eq3_lnr =[]
    eq3_lall=[]
    eq3_m   =[]
    eq3_s   =[]


    color   =[]
    marker  =[]
    alpha   =[]
    psize   =[]

    for ex in exp: 
    

        idi     = dt.datetime(days[k][0], days[k][1] ,days[k][2], days[k][3]) 
        idf     = dt.datetime(days[k][4], days[k][5] ,days[k][6], days[k][7])

        ni,nf= down.data_n(idi,idf,ex.data[:])

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
        specific_humidit_t	=   units.Quantity(ex.QT  ,'g/kg')

        alt            		=   units.Quantity(ex.z   ,'m')
        v_wind      		=   units.Quantity(ex.U   ,'m/seconds')
        u_wind      		=   units.Quantity(ex.V   ,'m/seconds')

        #Deep point temperature
        dw   	    =   mpy.dewpoint_from_specific_humidity( pressure[:], temperature[:,:],specific_humidity_v[:,:])

        mxr         =   mpy.mixing_ratio_from_specific_humidity(specific_humidity_v[:,:])
        tv          =   mpy.virtual_temperature(temperature[:,:],mxr[:])


        t1   =   nf-ni#ex.data.shape[0]        

        #initial and final point 
        z0   = 1
        z3   = len(pressure)


        theta=np.zeros((t1,ex.z.shape[0]))

        tp =np.zeros((t1,z3-z0))
        tv =np.zeros((t1,z3-z0))
        tvp=np.zeros((t1,z3-z0))

        mean_theta  =   np.zeros(t1)
        mean_temp   =   np.zeros(t1)
        mean_mxr    =   np.zeros(t1)
        mean_spec   =   np.zeros(t1)
        dwp         =   np.zeros(t1)
        cin_flecher =   np.zeros(t1)
        cin_uw      =   np.zeros(t1)
        tke_pbl     =   np.zeros(t1)
        mtke_cloud  =   np.zeros(t1)
        mtke_all    =   np.zeros(t1)
        mf          =   np.zeros(t1)


        #for i in range(0,ex.data.shape[0]): 
        jj=0
        for i in range(ni,nf): 

            #calculate before cin
            tp[jj,:]      =   mpy.parcel_profile(pressure[z0:z3], temperature[i,z0], dw[i,z0]) 
            tvp           =   mpy.virtual_temperature(tp[jj,:]*units('kelvin') ,mxr[i,z0:z3] ) 
            tv            =   mpy.virtual_temperature(temperature[i,z0:z3]    ,mxr[i,z0:z3] ) 

            ipblh         =   np.argmin(ex.TVFLUX[i,1:30])

            lcl_m         =   mpy.lcl(pressure[z0], temperature[i,z0], dw[i,z0],max_iters=50,eps=1e-2)
            lcl           =   lcl_m[0].magnitude

            #to calculate from flecher defitions
            #lfc_c         =   mpy.lfc(pressure[z0:z3],temperature[i,z0:z3], dw[i,z0:z3],tp[jj,:]*units('kelvin'), dwp,which='top')
            #lfc           =   lfc_c[0].magnitude
            
            #to calculate from uw defitions
            lfc_c         =   mpy.lfc(pressure[z0:z3],temperature[i,z0:z3], dw[i,z0:z3],which='top')
            lfc           =   lfc_c[0].magnitude

            l1   ,l2      =   down.pressure_n(lcl,lfc,pressure[:].magnitude,ex)

            #print(l1,l2)
            #print(ex.z[l1],ex.z[l2])

            if l1<=z0:
                l1+=3

            if l2<=l1:
                l2+=3

            if ex.MCUP[i,l1]>0.005:

                zn1     =   ex.z[z0:l1+1]
                l3      =   len(zn1)

                zn2      =   ex.z[l1+1:l2+1]
                l4       =   len(zn2)


                ini=l3+1
                ifi=ini+l4
                inte_uw       =   (tvp[ini:ifi]-tv[ini:ifi])/(tv[ini:ifi])
                cin_uw[jj]    =   -9.81*integrate.simps(inte_uw,zn2)

                rho           =ex.RHO[i,l1]

                TL=ex.TLFLUX[i][:]
                for j in range(0,len(ex.z)):

                    if j <= ipblh:

                        TL[j]=-10.0 

                tlmin =np.where(TL>-0.001)

                if(len(tlmin[0])>0 ):
                    
                    icloud      = tlmin[0][0]
                    
                else:
                    icloud=100

                if(icloud>ipblh and icloud>z0 and icloud<100 ):

                    mtke_cloud[jj]= 1.0/(ex.z[icloud]-ex.z[ipblh])*integrate.simps(ex.TKE[i][ipblh:icloud],ex.z[ipblh:icloud])
                    mtke_all[jj]  = 1.0/(ex.z[icloud]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:icloud],ex.z[z0:icloud])
                else:
                    icloud=100
                    mtke_cloud[jj]= 1.0/(ex.z[icloud]-ex.z[ipblh])*integrate.simps(ex.TKE[i][ipblh:icloud],ex.z[ipblh:icloud])
                    mtke_all[jj]  = 1.0/(ex.z[icloud]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:icloud],ex.z[z0:icloud])


                if ipblh<=z0:

                     tke_pbl[jj]=tke_pbl[ipblh]   

                else: 

                    tke_pbl[jj]    =   1.0/(ex.z[ipblh]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:ipblh],ex.z[z0:ipblh])


                eq1           =   0.06*(0.28*np.sqrt(tke_pbl[jj])+0.64)*np.exp(-1.0*cin_flecher[jj]/tke_pbl[jj])
                eq2           =   0.4*rho*(np.sqrt(tke_pbl[jj]))*np.exp(-1.0*cin_flecher[jj]/tke_pbl[jj])
                eq3           =   0.4*rho*(np.sqrt(tke_pbl[jj]))*np.exp(-1.0/tke_pbl[jj])

                if math.isnan(eq1) or math.isinf(eq1):
                    eq1=0
                if math.isnan(eq2) or math.isinf(eq2):
                    eq2=0
                if math.isnan(eq3) or math.isinf(eq3):
                    eq3=0
                    
                data.append(ex.data[i]       )
                cin.append ( cin_uw[jj]  )
                tke.append ( tke_pbl[jj]      )
                mfi.append ( ex.MCUP[i,l1]   )
                tke_all.append(mtke_cloud[jj])
                tke_cloud.append(mtke_all[jj])
                eq1_all.append(eq1)
                eq2_all.append(eq2)
                eq3_all.append(eq3)

                cb.append(lcl)
                ct.append(ex.z[icloud])
                tvmin.append(ex.z[ipblh])
                z0_all.append(ex.z[z0])


                if exp_label[k][0:3]=='Feb' or exp_label[k][0:3]=='Mar':
                    col='darkred'
                    mark='s'
                    alp=0.5
                    ps=20
                    cin_1.append(cin_uw[jj])
                    tke_1.append(tke_pbl[jj])
                    tke_cloud_1.append(mtke_cloud[jj])
                    tke_all_1.append(mtke_all[jj])
                    mfi_1.append(ex.MCUP[i,l1])
                    eq1_1.append(eq1)
                    eq2_1.append(eq2)
                    eq3_1.append(eq3)

                else: 
                    cin_2.append(cin_uw[jj])
                    tke_2.append(tke_pbl[jj])
                    tke_cloud_2.append(mtke_cloud[jj])
                    tke_all_2.append(mtke_all[jj])
                    mfi_2.append(ex.MCUP[i,l1])
                    eq1_2.append(eq1)
                    eq2_2.append(eq2)
                    eq3_2.append(eq3)

                if exp_case[k]=='large_rn':
                    col='darkred'
                    mark='s'
                    alp=0.5
                    ps=20
                    cin_lrn.append(cin_uw[jj])
                    tke_lrn.append(tke_pbl[jj])
                    tke_cloud_lrn.append(mtke_all[jj])
                    tke_all_lrn.append(mtke_all[jj])
                    mfi_lrn.append(ex.MCUP[i,l1])
                    eq1_lrn.append(eq1)
                    eq2_lrn.append(eq2)
                    eq3_lrn.append(eq3)

                if exp_case[k]=='large':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_lnr.append(cin_uw[jj])
                    tke_lnr.append(tke_pbl[jj])
                    tke_cloud_lnr.append(mtke_cloud[jj])
                    tke_all_lnr.append(mtke_all[jj])
                    mfi_lnr.append(ex.MCUP[i,l1])
                    eq1_lnr.append(eq1)
                    eq2_lnr.append(eq2)
                    eq3_lnr.append(eq3)

                if exp_case[k]=='large' or exp_case[k]=='large_rn':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_lall.append(cin_uw[jj])
                    tke_lall.append(tke_pbl[jj])
                    tke_cloud_lall.append(mtke_cloud[jj])
                    tke_all_lall.append(mtke_all[jj])
                    mfi_lall.append(ex.MCUP[i,l1])
                    eq1_lall.append(eq1)
                    eq2_lall.append(eq2)
                    eq3_lall.append(eq3)


                if exp_case[k]=='medium':
                    col='yellow'
                    mark='*'
                    alp=0.5
                    ps=20
                    cin_m.append(cin_uw[jj])
                    tke_m.append(tke_pbl[jj])
                    tke_cloud_m.append(mtke_cloud[jj])
                    tke_all_m.append(mtke_all[jj])
                    mfi_m.append(ex.MCUP[i,l1])
                    eq1_m.append(eq1)
                    eq2_m.append(eq2)
                    eq3_m.append(eq3)

                if exp_case[k]=='small':
                    col='blue'
                    mark='d'
                    alp=0.5
                    ps=20
                    cin_s.append(cin_uw[jj])
                    tke_s.append(tke_pbl[jj])
                    tke_cloud_s.append(mtke_cloud[jj])
                    tke_all_s.append(mtke_all[jj])
                    mfi_s.append(ex.MCUP[i,l1])
                    eq1_s.append(eq1)
                    eq2_s.append(eq2)
                    eq3_s.append(eq3)

                if exp_case[k]=='test':
                    col='white'
                    mark='p'
                    alp=0.3
                    ps=0.1

                color.append(col)
                marker.append(mark)
                alpha.append(alp)
                psize.append(ps)

            jj+=1

        k=k+1
    ################################################3
    ################################################3

    call, sall = pearsonr(tke,cin)
    print('all',call)

    c_iop1, sall = pearsonr(tke_1,cin_1)
    print('iop1',c_iop1)

    c_iop2, sall = pearsonr(tke_2,cin_2)
    print('iop2',c_iop2)

    clall, slall = pearsonr(tke_lall,cin_lall)
    print('large all',clall)

    clrn, slrn = pearsonr(tke_lrn,cin_lrn)
    print('large rain',clrn)

    clnr, slnr = pearsonr(tke_lnr,cin_lnr)
    print('large not rain',clnr)

    cm  , sm   = pearsonr(tke_m,cin_m)
    print('medium',cm)

    cs  , ss   = pearsonr(tke_s,cin_s)
    print('small',cs)

    print('################')
    print('TKE vs CIN')
    print('################')

    fig,ax =fown.figure_scatter(0.4)
    ax.text( 0.1,6.0,'R=%5.2f'%(call), fontsize=6)
    ax.text( 0.1,7.0,'a)IOPs ')
    ax.axis( [0,1.5,0,8])
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-1}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{Jkg^{-1}}$]') 
    ax.scatter(tke_1,cin_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(tke_2,cin_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_uw_tke_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(clall), fontsize=6)
    ax.text( 0.1,7.0,'d) Large ')
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-1}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{Jkg^{-1}}$]') 
    ax.scatter(tke_lrn,cin_lrn,marker='s',facecolors='none',edgecolors='k' ,s=4,)# label='Rain')
    ax.scatter(tke_lnr,cin_lnr,marker='s',facecolors='none',edgecolors='k' ,s=4,)# label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_uw_tke_large_all.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(clall), fontsize=6)
    ax.text( 0.1,7.0,'d) Large ')
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-1}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{Jkg^{-1}}$]') 
    ax.scatter(tke_lrn,cin_lrn,marker='o',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(tke_lnr,cin_lnr,marker='s',facecolors='none',edgecolors='k' ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_uw_tke_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(cm), fontsize=6)
    ax.text( 0.1,7,'c) Medium')
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-1}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{Jkg^{-1}}$]') 
    ax.scatter(tke_m,cin_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_uw_tke_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

def cin_flecher(exp,days,exp_label,exp_case):


    k=0

    data=[]

    tvmin   =[]
    cb      =[]
    ct      =[]
    z0_all  =[]

    cin =[]
    cin_1 =[]
    cin_2 =[]
    cin_l=[]
    cin_lrn=[]
    cin_lnr=[]
    cin_lall=[]
    cin_m=[]
    cin_s=[]

    cin_uw =[]
    cin_uw_1 =[]
    cin_uw_2 =[]
    cin_uw_l=[]
    cin_uw_lrn=[]
    cin_uw_lnr=[]
    cin_uw_lall=[]
    cin_uw_m=[]
    cin_uw_s=[]

    tke =[]
    tke_1 =[]
    tke_2 =[]
    tke_l =[]
    tke_lrn =[]
    tke_lnr =[]
    tke_lall =[]
    tke_m =[]
    tke_s =[]

    tke_cloud =[]
    tke_cloud_1 =[]
    tke_cloud_2 =[]
    tke_cloud_l =[]
    tke_cloud_lrn =[]
    tke_cloud_lnr =[]
    tke_cloud_lall =[]
    tke_cloud_m =[]
    tke_cloud_s =[]

    tke_all   =[]
    tke_all_1 =[]
    tke_all_2 =[]
    tke_all_l =[]
    tke_all_lrn =[]
    tke_all_lnr =[]
    tke_all_lall=[]
    tke_all_m =[]
    tke_all_s =[]

    mc      =[]
    mfi     =[]
    mfi_1   =[]
    mfi_2   =[]
    mfi_l   =[]
    mfi_lrn =[]
    mfi_lnr =[]
    mfi_lall=[]
    mfi_m   =[]
    mfi_s   =[]
    mfi2    =[]
    mfi3    =[]
    mup     =[]

    eq1_all =[]
    eq1_1   =[]
    eq1_2   =[]
    eq1_l   =[]
    eq1_lrn =[]
    eq1_lnr =[]
    eq1_lall=[]
    eq1_m   =[]
    eq1_s   =[]

    eq2_all =[]
    eq2_1   =[]
    eq2_2   =[]
    eq2_l   =[]
    eq2_lrn =[]
    eq2_lnr =[]
    eq2_lall=[]
    eq2_m   =[]
    eq2_s   =[]

    eq3_all =[]
    eq3_1   =[]
    eq3_2   =[]
    eq3_l   =[]
    eq3_lrn =[]
    eq3_lnr =[]
    eq3_lall=[]
    eq3_m   =[]
    eq3_s   =[]

    eq4_all =[]
    eq4_1   =[]
    eq4_2   =[]
    eq4_l   =[]
    eq4_lrn =[]
    eq4_lnr =[]
    eq4_lall=[]
    eq4_m   =[]
    eq4_s   =[]

    eq1_uw_1   =[]
    eq1_uw_2   =[]
    eq1_uw_l   =[]
    eq1_uw_lrn =[]
    eq1_uw_lnr =[]
    eq1_uw_lall=[]
    eq1_uw_m   =[]
    eq1_uw_s   =[]

    eq2_uw_1   =[]
    eq2_uw_2   =[]
    eq2_uw_l   =[]
    eq2_uw_lrn =[]
    eq2_uw_lnr =[]
    eq2_uw_lall=[]
    eq2_uw_m   =[]
    eq2_uw_s   =[]


    color   =[]
    marker  =[]
    alpha   =[]
    psize   =[]

    for ex in exp: 
    

        idi     = dt.datetime(days[k][0], days[k][1] ,days[k][2], days[k][3]) 
        idf     = dt.datetime(days[k][4], days[k][5] ,days[k][6], days[k][7])

        ni,nf= down.data_n(idi,idf,ex.data[:])

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
        specific_humidit_t	=   units.Quantity(ex.QT  ,'g/kg')

        alt            		=   units.Quantity(ex.z   ,'m')
        v_wind      		=   units.Quantity(ex.U   ,'m/seconds')
        u_wind      		=   units.Quantity(ex.V   ,'m/seconds')

        #Deep point temperature
        dw   	    =   mpy.dewpoint_from_specific_humidity( pressure[:], temperature[:,:],specific_humidity_v[:,:])

        mxr         =   mpy.mixing_ratio_from_specific_humidity(specific_humidity_v[:,:])
        tv          =   mpy.virtual_temperature(temperature[:,:],mxr[:])


        #funcionando arm e kwajex
        #z1,z2=down.level_n(200,500,ex.z)
        #z3   =len(pressure)
        #z0,z4=down.level_n(300,600,ex.z)

        z1,z2=down.level_n(200,450,ex.z)
        z3   =len(pressure)
        z0,z4=down.level_n(320,600,ex.z)


        t1   =   nf-ni#ex.data.shape[0]        

        theta=np.zeros((t1,ex.z.shape[0]))

        tp =np.zeros((t1,z3-z0))
        tv =np.zeros((t1,z3-z0))
        tvp=np.zeros((t1,z3-z0))

        mean_theta  =   np.zeros(t1)
        mean_temp   =   np.zeros(t1)
        mean_mxr    =   np.zeros(t1)
        mean_spec   =   np.zeros(t1)
        dwp         =   np.zeros(t1)
        cin_flecher =   np.zeros(t1)
        cin_uw      =   np.zeros(t1)
        tke_pbl     =   np.zeros(t1)
        mtke_cloud  =   np.zeros(t1)
        mtke_all    =   np.zeros(t1)
        mf          =   np.zeros(t1)


        #for i in range(0,ex.data.shape[0]): 
        jj=0
        for i in range(ni,nf): 

            #theta[i,:]    =   mpy.potential_temperature(pressure[:],temperature[i,:])
            #mean_theta[i] =   np.mean(theta[i,z1:z2])

            mean_mxr[jj]   =   np.mean(mxr[i,z1:z2].magnitude)*(units('g/kg')) 

            #standar deviation
            qv_s          =   np.std(specific_humidity_v[i,z1:z2].magnitude,axis=0)
            mean_spec[jj]  =   (np.mean(specific_humidity_v[i,z1:z2].magnitude)+qv_s)*(units('g/kg')) 


            temp          =   np.mean(temperature[i,z1:z2])
            dwp           =   mpy.dewpoint_from_specific_humidity( pressure[z1],temp,mean_spec[jj])#.magnitude

            #calculate before cin
            tp[jj,:]      =   mpy.parcel_profile(pressure[z0:z3], temp, dwp) 
            tvp           =   mpy.virtual_temperature(tp[jj,:]*units('kelvin') ,mxr[i,z0:z3] ) 
            tv            =   mpy.virtual_temperature(temperature[i,z0:z3]    ,mxr[i,z0:z3] ) 

            ipblh         =   np.argmin(ex.TVFLUX[i,1:30])

            lcl_m         =   mpy.lcl(pressure[z0], temp, dwp,max_iters=50,eps=1e-4)
            lcl           =   lcl_m[0].magnitude

            #to calculate from flecher defitions
            lfc_c         =   mpy.lfc(pressure[z0:z3],temperature[i,z0:z3], dw[i,z0:z3],tp[jj,:]*units('kelvin'), dwp,which='top')
            lfc           =   lfc_c[0].magnitude

            l1   ,l2      =   down.pressure_n(lcl,lfc,pressure[:].magnitude,ex)

            if l1<=z0:
                l1+=2

            if l2<=l1:
                l2+=2

            if ex.MCUP[i,l1+1]>0.005:

                zn1     =   ex.z[z0:l1+1]
                l3      =   len(zn1)

                zn2      =   ex.z[l1+1:l2+1]
                l4       =   len(zn2)


                #virtual temperature
                #tp[i,:]       =   mpy.parcel_profile(pressure[z0:z3], temp, dwp) 
                #tvp           =   mpy.virtual_temperature(tp[i,z0:l1]*units('kelvin') ,mxr[i,z0:l1] ) 
                #tv            =   mpy.virtual_temperature(temperature[i,z0:l1],mxr[i,z0:l1] ) 

                ini=0
                ifi=ini+l3
                inte_cin      =   (tvp[ini:ifi]-tv[ini:ifi])/(tv[ini:ifi])
                cin_flecher[jj]=   -9.81*integrate.simps(inte_cin,zn1)


                #ini=l3+1
                #ifi=ini+l4
                #inte_uw       =   (tvp[ini:ifi]-tv[ini:ifi])/(tv[ini:ifi])
                #cin_uw[jj]    =   -9.81*integrate.simps(inte_uw,zn2)

                #print(l3+1,l3+1+l4)

                rho           =ex.RHO[i,l1+1]

                TL=ex.TLFLUX[i][:]
                for j in range(0,len(ex.z)):

                    if j <= ipblh:

                        TL[j]=-10.0 

                tlmin =np.where(TL>-0.001)

                if(len(tlmin[0])>0 ):
                    
                    icloud      = tlmin[0][0]
                    
                else:
                    icloud=100

                if(icloud>ipblh and icloud>z0 and icloud<100 ):

                    mtke_cloud[jj]= 1.0/(ex.z[icloud]-ex.z[ipblh])*integrate.simps(ex.TKE[i][ipblh:icloud],ex.z[ipblh:icloud])
                    mtke_all[jj]  = 1.0/(ex.z[icloud]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:icloud],ex.z[z0:icloud])

                else:

                    icloud=100
                    mtke_cloud[jj]= 1.0/(ex.z[icloud]-ex.z[ipblh])*integrate.simps(ex.TKE[i][ipblh:icloud],ex.z[ipblh:icloud])
                    mtke_all[jj]  = 1.0/(ex.z[icloud]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:icloud],ex.z[z0:icloud])


                #print( z0,ipblh,icloud)
                #print(l3,cin_flecher[i])
                #tke_pbl[i]    =   1.0/(ex.z[l1]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:l1],ex.z[z0:l1])
                #print(ipblh)

                if ipblh<=z0:

                     tke_pbl[jj]=ex.TKE[i,ipblh]   
                     #tke_pbl[jj]=ex.TKE[i,l1+1]   

                else: 

                    tke_pbl[jj]    =   1.0/(ex.z[ipblh]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:ipblh],ex.z[z0:ipblh])
                    #tke_pbl[jj]    =   1.0/(ex.z[l1]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:l1],ex.z[z0:l1])


                eq1           =   0.06*(0.28*np.sqrt(tke_pbl[jj])+0.64)*np.exp(-1.0*np.abs(cin_flecher[jj])/tke_pbl[jj])

                eq2           =   0.4*rho*(np.sqrt(tke_pbl[jj]))*np.exp(-1.0*np.abs(cin_flecher[jj])/tke_pbl[jj])

                kf=2.00
                eq3           =  0.5*rho*(np.sqrt(kf*tke_pbl[jj]/(2.0*math.pi)))*np.exp(-1.0*np.abs(cin_flecher[jj])/(2.0*kf*tke_pbl[jj]))

                kf=0.65
                eq4           =   rho*(np.sqrt(kf*tke_pbl[jj]/(2.0*math.pi)))*np.exp(-1.0/(2.0*kf*tke_pbl[jj]))

                eq1_uw        =   0.06*(0.28*np.sqrt(tke_pbl[jj])+0.64)*np.exp(-1.0*cin_uw[jj]/tke_pbl[jj])
                eq2_uw        =   0.4*rho*(np.sqrt(tke_pbl[jj]))*np.exp(-1.0*cin_uw[jj]/tke_pbl[jj])

                if math.isnan(eq1) or math.isinf(eq1) :
                    eq1=0
                    print(exp_label[k],cin_flecher[jj],tke_pbl[jj])
                if math.isnan(eq2) or math.isinf(eq2):
                    eq2=0
                if math.isnan(eq3) or math.isinf(eq3):
                    eq3=0
                    
                data.append(ex.data[i]       )
                cin.append ( cin_flecher[jj]  )
                tke.append ( tke_pbl[jj]      )
                mfi.append ( ex.MCUP[i,l1+1]   )
                tke_all.append(mtke_cloud[jj])
                tke_cloud.append(mtke_all[jj])
                eq1_all.append(eq1)
                eq2_all.append(eq2)
                eq3_all.append(eq3)
                eq4_all.append(eq4)

                cb.append(lcl)
                ct.append(ex.z[icloud])
                tvmin.append(ex.z[ipblh])
                z0_all.append(ex.z[z0])


                if exp_label[k][0:3]=='Feb' or exp_label[k][0:3]=='Mar':
                    col='darkred'
                    mark='s'
                    alp=0.5
                    ps=20
                    cin_1.append(cin_flecher[jj])
                    tke_1.append(tke_pbl[jj])
                    tke_cloud_1.append(mtke_cloud[jj])
                    tke_all_1.append(mtke_all[jj])
                    mfi_1.append(ex.MCUP[i,l1+1])
                    eq1_1.append(eq1)
                    eq2_1.append(eq2)
                    eq3_1.append(eq3)
                    eq4_1.append(eq4)
                    eq1_uw_1.append(eq1_uw)
                    eq2_uw_1.append(eq2_uw)

                else: 
                    cin_2.append(cin_flecher[jj])
                    tke_2.append(tke_pbl[jj])
                    tke_cloud_2.append(mtke_cloud[jj])
                    tke_all_2.append(mtke_all[jj])
                    mfi_2.append(ex.MCUP[i,l1+1])
                    eq1_2.append(eq1)
                    eq2_2.append(eq2)
                    eq3_2.append(eq3)
                    eq4_2.append(eq4)
                    eq1_uw_2.append(eq1_uw)
                    eq2_uw_2.append(eq2_uw)

                if exp_case[k]=='large_rn':
                    col='darkred'
                    mark='s'
                    alp=0.5
                    ps=20
                    cin_lrn.append(cin_flecher[jj])
                    tke_lrn.append(tke_pbl[jj])
                    tke_cloud_lrn.append(mtke_all[jj])
                    tke_all_lrn.append(mtke_all[jj])
                    mfi_lrn.append(ex.MCUP[i,l1+1])
                    eq1_lrn.append(eq1)
                    eq2_lrn.append(eq2)
                    eq3_lrn.append(eq3)
                    eq4_lrn.append(eq4)
                    eq1_uw_lrn.append(eq1_uw)
                    eq2_uw_lrn.append(eq2_uw)

                if exp_case[k]=='large':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_lnr.append(cin_flecher[jj])
                    tke_lnr.append(tke_pbl[jj])
                    tke_cloud_lnr.append(mtke_cloud[jj])
                    tke_all_lnr.append(mtke_all[jj])
                    mfi_lnr.append(ex.MCUP[i,l1+1])
                    eq1_lnr.append(eq1)
                    eq2_lnr.append(eq2)
                    eq3_lnr.append(eq3)
                    eq4_lnr.append(eq4)
                    eq1_uw_lnr.append(eq1_uw)
                    eq2_uw_lnr.append(eq2_uw)

                if exp_case[k]=='large' or exp_case[k]=='large_rn':
                    col='red'
                    mark='o'
                    alp=0.5
                    ps=20
                    cin_lall.append(cin_flecher[jj])
                    tke_lall.append(tke_pbl[jj])
                    tke_cloud_lall.append(mtke_cloud[jj])
                    tke_all_lall.append(mtke_all[jj])
                    mfi_lall.append(ex.MCUP[i,l1+1])
                    eq1_lall.append(eq1)
                    eq2_lall.append(eq2)
                    eq3_lall.append(eq3)
                    eq4_lall.append(eq4)
                    eq1_uw_lall.append(eq1_uw)
                    eq2_uw_lall.append(eq2_uw)


                if exp_case[k]=='medium':
                    col='yellow'
                    mark='*'
                    alp=0.5
                    ps=20
                    cin_m.append(cin_flecher[jj])
                    tke_m.append(tke_pbl[jj])
                    tke_cloud_m.append(mtke_cloud[jj])
                    tke_all_m.append(mtke_all[jj])
                    mfi_m.append(ex.MCUP[i,l1+1])
                    eq1_m.append(eq1)
                    eq2_m.append(eq2)
                    eq3_m.append(eq3)
                    eq4_m.append(eq4)
                    eq1_uw_m.append(eq1_uw)
                    eq2_uw_m.append(eq2_uw)

                if exp_case[k]=='small':
                    col='blue'
                    mark='d'
                    alp=0.5
                    ps=20
                    cin_s.append(cin_flecher[jj])
                    tke_s.append(tke_pbl[jj])
                    tke_cloud_s.append(mtke_cloud[jj])
                    tke_all_s.append(mtke_all[jj])
                    mfi_s.append(ex.MCUP[i,l1+1])
                    eq1_s.append(eq1)
                    eq2_s.append(eq2)
                    eq3_s.append(eq3)
                    eq4_s.append(eq4)
                    eq1_uw_s.append(eq1_uw)
                    eq2_uw_s.append(eq2_uw)

                if exp_case[k]=='test':
                    col='white'
                    mark='p'
                    alp=0.3
                    ps=0.1

                color.append(col)
                marker.append(mark)
                alpha.append(alp)
                psize.append(ps)

            jj+=1

        k=k+1
    ################################################3
    ################################################3

    call, sall = pearsonr(tke,cin)
    print('all',call)

    c_iop1, sall = pearsonr(tke_1,cin_1)
    print('iop1',c_iop1)

    c_iop2, sall = pearsonr(tke_2,cin_2)
    print('iop2',c_iop2)

    clall, slall = pearsonr(tke_lall,cin_lall)
    print('large all',clall)

    clrn, slrn = pearsonr(tke_lrn,cin_lrn)
    print('large rain',clrn)

    clnr, slnr = pearsonr(tke_lnr,cin_lnr)
    print('large not rain',clnr)

    cm  , sm   = pearsonr(tke_m,cin_m)
    print('medium',cm)

    cs  , ss   = pearsonr(tke_s,cin_s)
    print('small',cs)

    print('################')
    print('TKE vs CIN')
    print('################')

    fig,ax =fown.figure_scatter(0.4)
    ax.text( 0.1,6.0,'R=%5.2f'%(call), fontsize=6)
    ax.text( 0.1,7.0,'a)IOPs ')
    ax.axis( [0,1.5,0,8])
    ax.set_xlabel(r'TKE [$\mathrm{m^{-2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_1,cin_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(tke_2,cin_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_uw_tke_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(clall), fontsize=6)
    ax.text( 0.1,7.0,'d) Large ')
    ax.set_xlabel(r'TKE [$\mathrm{m^{-2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_lrn,cin_lrn,marker='s',facecolors='none',edgecolors='k' ,s=4,)# label='Rain')
    ax.scatter(tke_lnr,cin_lnr,marker='s',facecolors='none',edgecolors='k' ,s=4,)# label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_uw_tke_large_all.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(clall), fontsize=6)
    ax.text( 0.1,7.0,'d) Large ')
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-1}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_lrn,cin_lrn,marker='o',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(tke_lnr,cin_lnr,marker='s',facecolors='none',edgecolors='k' ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_uw_tke_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(cm), fontsize=6)
    ax.text( 0.1,7,'c) Medium')
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-1}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_m,cin_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_uw_tke_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    ################################################3
    ################################################3

    call, sall = pearsonr(tke,cin)
    print('all',call)

    c_iop1, sall = pearsonr(tke_1,cin_1)
    print('iop1',c_iop1)

    c_iop2, sall = pearsonr(tke_2,cin_2)
    print('iop2',c_iop2)

    clall, slall = pearsonr(tke_lall,cin_lall)
    print('large all',clall)

    clrn, slrn = pearsonr(tke_lrn,cin_lrn)
    print('large rain',clrn)

    clnr, slnr = pearsonr(tke_lnr,cin_lnr)
    print('large not rain',clnr)

    cm  , sm   = pearsonr(tke_m,cin_m)
    print('medium',cm)

    cs  , ss   = pearsonr(tke_s,cin_s)
    print('small',cs)

    print('################')
    print('TKE vs CIN')
    print('################')

    fig,ax =fown.figure_scatter(0.4)
    ax.text( 0.1,6.0,'R=%5.2f'%(call), fontsize=6)
    ax.text( 0.1,7.0,'a)IOPs ')
    ax.axis( [0,1.5,0,8])
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_1,cin_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(tke_2,cin_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_tke_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(clall), fontsize=6)
    ax.text( 0.1,7.0,'d) Large ')
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_lrn,cin_lrn,marker='s',facecolors='none',edgecolors='k' ,s=4,)# label='Rain')
    ax.scatter(tke_lnr,cin_lnr,marker='s',facecolors='none',edgecolors='k' ,s=4,)# label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_tke_large_all.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(clall), fontsize=6)
    ax.text( 0.1,7.0,'d) Large ')
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_lrn,cin_lrn,marker='o',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(tke_lnr,cin_lnr,marker='s',facecolors='none',edgecolors='k' ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_tke_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(cm), fontsize=6)
    ax.text( 0.1,7,'c) Medium')
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_m,cin_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_tke_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,8])
    ax.text( 0.1,6.0,'R=%5.2f'%(cs), fontsize=6)
    ax.text( 0.1,7,'b) Small')
    ax.set_xlabel(r'TKE [$\mathrm{kgm^{-2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_s,cin_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_tke_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)


    ########################################
    ########################################
    call     =0 
    c_iop1   =0
    c_iop2   =0
    clall    =0 
    clrn     =0 
    clnr     =0 
    cm       =0 
    cs       =0

    print('################')
    print('CIN - MF')
    print('################')

    call, sall = pearsonr(cin,mfi)
    print('mf tke all',call)

    c_iop1, sall = pearsonr(cin_1,mfi_1)
    print('mf tke iop1',c_iop1)

    c_iop1, sall = pearsonr(cin_2,mfi_2)
    print('mf tke iop2',c_iop2)

    clrn, slrn = pearsonr(cin_lrn,mfi_lrn)
    print('mf tke large rain',clrn)

    clnr, slnr = pearsonr(cin_lnr,mfi_lnr)
    print('mf tke large not rain',clnr)

    clall, slall = pearsonr(cin_lall,mfi_lall)
    print('mf tke large all',clall)

    cm  , sm   = pearsonr(cin_m,mfi_m)
    print('mf tke medium',cm)

    cs  , ss   = pearsonr(cin_s,mfi_s)
    print('mf tke small',cs)

    fig,ax =fown.figure_scatter(0.4)
    #ax.text( 0.2,7,'Shallow Cases', fontsize=8)

    ax.axis( [0,8.0,0,0.2])
    ax.text( 1,0.18,'a) IOPs ')
    ax.text( 1,0.16,'R=%5.2f'%(call), fontsize=6)
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'uMF [$\mathrm{kgm^{-2}s^{-1}}$]') 
    ax.scatter(cin_1,mfi_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(cin_2,mfi_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_mfi_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)



    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,8.0,0,0.2])
    ax.text( 1,0.16,'R=%5.2f'%(clall), fontsize=6)
    ax.text( 1,0.18,'d) Large ')
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'uMF [$\mathrm{kgm^{-2}s^{-1}}$]') 
    ax.scatter(cin_lrn,mfi_lrn,marker='o',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(cin_lnr,mfi_lnr,marker='s',facecolors='none',edgecolors='k'    ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_mfi_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,8.0,0,0.2])
    ax.text( 1,0.18,'c) Medium')
    ax.text( 1,0.16,'R=%5.2f'%(cm), fontsize=6)
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'uMF [$\mathrm{kgm^{-2}s^{-1}}$]') 
    ax.scatter(cin_m,mfi_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_mfi_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)


    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,8.0,0,0.2])
    ax.text( 1,0.16,'R=%5.2f'%(cs), fontsize=6)
    ax.text( 1,0.18,'b) Small')
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'uMF [$\mathrm{kgm^{-2}s^{-1}}$]') 
    ax.scatter(cin_s,mfi_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_mfi_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)


    #############################

    print('################')
    print('TKE vs MFI')
    print('################')

    call     =0 
    c_iop1   =0
    c_iop2   =0
    clall    =0 
    clrn     =0 
    clnr     =0 
    cm       =0 
    cs       =0

    call, sall = pearsonr(tke,mfi)
    print('mf tke all',call)

    c_iop1, sall = pearsonr(tke_1,mfi_1)
    print('mf tke iop1',c_iop1)

    c_iop1, sall = pearsonr(tke_2,mfi_2)
    print('mf tke iop2',c_iop2)

    clrn, slrn = pearsonr(tke_lrn,mfi_lrn)
    print('mf tke large rain',clrn)

    clnr, slnr = pearsonr(tke_lnr,mfi_lnr)
    print('mf tke large not rain',clnr)

    clall, slall = pearsonr(tke_lall,mfi_lall)
    print('mf tke large all',clall)

    cm  , sm   = pearsonr(tke_m,mfi_m)
    print('mf tke medium',cm)

    cs  , ss   = pearsonr(tke_s,mfi_s)
    print('mf tke small',cs)


    fig,ax =fown.figure_scatter(0.4)
    #ax.text( 0.2,7,'Shallow Cases', fontsize=8)
    ax.axis( [0,1.5,0,0.2])
    ax.text( 0.4,0.18,'a) IOPs ')
    ax.text( 0.4,0.16,'R=%5.2f'%(call), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'uMF_{les} [$\mathrm{kgm^{-2}s^{-1}}$]') 
    ax.scatter(tke_1,mfi_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(tke_2,mfi_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_tke_mfi_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,0.2])
    ax.text( 0.2,0.18,'d) Large ')
    ax.text( 0.2,0.16,'R=%5.2f'%(clall), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'uMF_{les} [$\mathrm{kgm^{-2}s^{-1}}$]') 
    ax.scatter(tke_lrn,mfi_lrn,marker='s',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(tke_lnr,mfi_lnr,marker='o',facecolors='none',edgecolors='k'    ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_tke_mfi_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)


    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.5,0,0.2])
    ax.text( 0.1,0.18,'c) Medium')
    ax.text( 0.1,0.16,'R=%5.2f'%(cm), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'uMF_{les} [$\mathrm{kgm^{-2}s^{-1}}$]') 
    ax.scatter(tke_m,mfi_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_tke_mfi_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.text( 0.1,0.18,'b) Small')
    ax.text( 0.1,0.16,'R=%5.2f'%(cs), fontsize=6)
    ax.axis( [0,1.5,0,0.2])
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'uMF_{les} [$\mathrm{kgm^{-2}s^{-1}}$]') 
    ax.scatter(tke_s,mfi_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_tke_mfi_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)
    #############################
    #############################


    print('################')
    print('TKE ALL vs CIN')
    print('################')

    call     =0 
    c_iop1   =0
    c_iop2   =0
    clall    =0 
    clrn     =0 
    clnr     =0 
    cm       =0 
    cs       =0

    call, sall = pearsonr(tke_all,cin)
    print('mf tke all',call)

    c_iop1, sall = pearsonr(tke_all_1,cin_1)
    print('mf tke iop1',c_iop1)

    c_iop1, sall = pearsonr(tke_all_2,cin_2)
    print('mf tke iop2',c_iop2)

    clrn, slrn = pearsonr(tke_all_lrn,cin_lrn)
    print('mf tke large rain',clrn)

    clnr, slnr = pearsonr(tke_all_lnr,cin_lnr)
    print('mf tke large not rain',clnr)

    clall, slall = pearsonr(tke_all_lall,cin_lall)
    print('mf tke large all',clall)

    cm  , sm   = pearsonr(tke_all_m,cin_m)
    print('mf tke medium',cm)

    cs  , ss   = pearsonr(tke_all_s,cin_s)
    print('mf tke small',cs)


    ###########################################################################333
    ###########################################################################333


    fig,ax =fown.figure_scatter(0.4)
    #ax.text( 0.2,7,'Shallow Cases', fontsize=8)
    ax.axis( [0,1.0,0,8])
    ax.text( 0.4,7,'a) IOPs ')
    ax.text( 0.4,6,'R=%5.2f'%(call), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_all_1,cin_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(tke_all_2,cin_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_cin_tke_all_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.0,0,8])
    ax.text( 0.2,7,'d) Large ')
    ax.text( 0.2,6,'R=%5.2f'%(clall), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_all_lrn,cin_lrn,marker='s',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(tke_all_lnr,cin_lnr,marker='o',facecolors='none',edgecolors='k'    ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_tke_all_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.0,0,8])
    ax.text( 0.6,7,'c) Medium')
    ax.text( 0.6,6,'R=%5.2f'%(cm), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_all_m,cin_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left',markerfirst=False)
    fig.savefig('%sscatter_cin_tke_all_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,1.0,0,8])
    ax.text( 0.7,7,'b) Small')
    ax.text( 0.7,6,'R=%5.2f'%(cs), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_all_s,cin_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left',markerfirst=False)
    fig.savefig('%sscatter_cin_tke_all_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    #############################
    #############################
    print('################')
    print('TKE CLOUD vs CIN')
    print('################')

    call     =0 
    c_iop1   =0
    c_iop2   =0
    clall    =0 
    clrn     =0 
    clnr     =0 
    cm       =0 
    cs       =0


    call, sall = pearsonr(tke_cloud,cin)
    print('mf tke all',call)

    c_iop1, sall = pearsonr(tke_cloud_1,cin_1)
    print('mf tke iop1',c_iop1)

    c_iop1, sall = pearsonr(tke_cloud_2,cin_2)
    print('mf tke iop2',c_iop2)

    clrn, slrn = pearsonr(tke_cloud_lrn,cin_lrn)
    print('mf tke large rain',clrn)

    clnr, slnr = pearsonr(tke_cloud_lnr,cin_lnr)
    print('mf tke large not rain',clnr)

    clall, slall = pearsonr(tke_cloud_lall,cin_lall)
    print('mf tke large all',clall)

    cm  , sm   = pearsonr(tke_cloud_m,cin_m)
    print('mf tke medium',cm)

    cs  , ss   = pearsonr(tke_cloud_s,cin_s)
    print('mf tke small',cs)


    ###########################################################################333
    ###########################################################################333

    fig,ax =fown.figure_scatter(0.4)
    #ax.text( 0.2,7,'Shallow Cases', fontsize=8)
    ax.axis( [0,0.75,0,8])
    ax.text( 0.2,7,'a) IOPs ')
    ax.text( 0.2,6,'R=%5.2f'%(call), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_cloud_1,cin_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(tke_cloud_2,cin_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_cin_tke_cloud_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.75,0,8])
    ax.text( 0.1,7,'d) Large ')
    ax.text( 0.1,6,'R=%5.2f'%(clall), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_cloud_lrn,cin_lrn,marker='s',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(tke_cloud_lnr,cin_lnr,marker='o',facecolors='none',edgecolors='k'    ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_cin_tke_cloud_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.75,0,8])
    ax.text( 0.3,7,'c) Medium')
    ax.text( 0.3,6,'R=%5.2f'%(cm), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_cloud_m,cin_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_tke_cloud_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.75,0,8])
    ax.text( 0.3,7,'b) Small')
    ax.text( 0.3,6,'R=%5.2f'%(cs), fontsize=6)
    ax.set_xlabel(r'TKE [$\mathrm{m^{2}s^{-2}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{m^{2}s^{-2}}$]') 
    ax.scatter(tke_cloud_s,cin_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_tke_cloud_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    ######################################################33
    ######################################################33

    print('################')
    print('MFI vs EQ1')
    print('################')
    call     =0 
    c_iop1   =0
    c_iop2   =0
    clall    =0 
    clrn     =0 
    clnr     =0 
    cm       =0 
    cs       =0

    call, sall = pearsonr(mfi,eq1_all)
    print('mf tke all',call)

    c_iop1, sall = pearsonr(mfi_1,eq1_1)
    print('mf tke iop1',c_iop1)

    c_iop2, sall = pearsonr(mfi_2,eq1_2)
    print('mf tke iop2',c_iop2)

    clrn, slrn = pearsonr(mfi_lrn,eq1_lrn)
    print('mf tke large rain',clrn)

    clnr, slnr = pearsonr(mfi_lnr,eq1_lnr)
    print('mf tke large not rain',clnr)

    clall, slall = pearsonr(mfi_lall,eq1_lall)
    print('mf tke large all',clall)

    cm  , sm   = pearsonr(mfi_m,eq1_m)
    print('mf tke medium',cm)

    cs  , ss   = pearsonr(mfi_s,eq1_s)
    print('mf tke small',cs)

    fig,ax =fown.figure_scatter(0.4)
    ax.scatter(mfi_1,eq1_1, marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(mfi_2,eq1_2, marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.axis( [0,0.25,0,0.25])
    ax.text(  0.01,0.18,'a) IOPs')
    ax.text( 0.01,0.16,'R=%5.2f'%(call), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_mf_eq1_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.scatter( mfi_lrn,eq1_lrn,marker='o',facecolors='none',edgecolors='blue'  ,s=4)
    ax.scatter( mfi_lnr,eq1_lnr,marker='s',facecolors='none',edgecolors='k'     ,s=4)
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.09,0.18,'d) Large')
    ax.text( 0.09,0.16,'R=%5.2f'%(clall), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_mf_eq1_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.25,0,0.25])
    ax.text(  0.09,0.18,'c) Medium')
    ax.text( 0.09,0.16,'R=%5.2f'%(cm), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.scatter(mfi_m,eq1_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_mf_eq1_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.1,0.18,'b) Small')
    ax.text( 0.1,0.16,'R=%5.2f'%(cs), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.scatter(mfi_s,eq1_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_mf_eq1_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)
    ##########################################
    ##########################################
    print('################')
    print('MFI vs EQ2')
    print('################')

    call     =0 
    c_iop1   =0
    c_iop2   =0
    clall    =0 
    clrn     =0 
    clnr     =0 
    cm       =0 
    cs       =0

    call, sall = pearsonr(mfi,eq2_all)
    print('mf tke all',call)

    c_iop1, sall = pearsonr(mfi_1,eq2_1)
    print('mf tke iop1',c_iop1)

    c_iop2, sall = pearsonr(mfi_2,eq2_2)
    print('mf tke iop2',c_iop2)

    clrn, slrn = pearsonr(mfi_lrn,eq2_lrn)
    print('mf tke large rain',clrn)

    clnr, slnr = pearsonr(mfi_lnr,eq2_lnr)
    print('mf tke large not rain',clnr)

    clall, slall = pearsonr(mfi_lall,eq2_lall)
    print('mf tke large all',clall)

    cm  , sm   = pearsonr(mfi_m,eq2_m)
    print('mf tke medium',cm)

    cs  , ss   = pearsonr(mfi_s,eq2_s)
    print('mf tke small',cs)

    fig,ax =fown.figure_scatter(0.4)
    ax.scatter(mfi_1,eq2_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(mfi_2,eq2_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.16,0.04,'a) IOPs')
    ax.text( 0.16,0.02,'R=%5.2f'%(call), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_mf_eq2_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.scatter( mfi_lrn,eq2_lrn,marker='o',facecolors='none',edgecolors='blue'  ,s=4)
    ax.scatter( mfi_lnr,eq2_lnr,marker='s',facecolors='none',edgecolors='k'     ,s=4)
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.16,0.04,'d) Large')
    ax.text( 0.16,0.02,'R=%5.2f'%(clall), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_mf_eq2_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.25,0,0.25])
    ax.text(  0.16,0.04,'c) Medium')
    ax.text(  0.16,0.02,'R=%5.2f'%(cm), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.scatter(mfi_m,eq2_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_mf_eq2_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.16,0.04,'b) Small')
    ax.text( 0.16,0.02,'R=%5.2f'%(cs), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.scatter(mfi_s,eq2_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_mf_eq2_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    plt.close('all')

    ##########################################
    print('################')
    print('MFI vs EQ3')
    print('################')

    call     =0 
    c_iop1   =0
    c_iop2   =0
    clall    =0 
    clrn     =0 
    clnr     =0 
    cm       =0 
    cs       =0

    call, sall = pearsonr(mfi,eq3_all)
    print('mf tke all',call)

    c_iop1, sall = pearsonr(mfi_1,eq3_1)
    print('mf tke iop1',c_iop1)

    c_iop2, sall = pearsonr(mfi_2,eq3_2)
    print('mf tke iop2',c_iop2)

    clrn, slrn = pearsonr(mfi_lrn,eq3_lrn)
    print('mf tke large rain',clrn)

    clnr, slnr = pearsonr(mfi_lnr,eq3_lnr)
    print('mf tke large not rain',clnr)

    clall, slall = pearsonr(mfi_lall,eq3_lall)
    print('mf tke large all',clall)

    cm  , sm   = pearsonr(mfi_m,eq3_m)
    print('mf tke medium',cm)

    cs  , ss   = pearsonr(mfi_s,eq3_s)
    print('mf tke small',cs)


    fig,ax =fown.figure_scatter(0.4)
    ax.scatter(mfi_1,eq3_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(mfi_2,eq3_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.16,0.04,'a) IOPs')
    ax.text( 0.16,0.02,'R=%5.2f'%(call), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_mf_eq3_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.scatter( mfi_lrn,eq3_lrn,marker='o',facecolors='none',edgecolors='blue'  ,s=4)
    ax.scatter( mfi_lnr,eq3_lnr,marker='s',facecolors='none',edgecolors='k'     ,s=4)
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.16,0.04,'d) Large')
    ax.text( 0.16,0.02,'R=%5.2f'%(clall), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_mf_eq3_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.25,0,0.25])
    ax.text(  0.16,0.04,'c) Medium')
    ax.text(  0.16,0.02,'R=%5.2f'%(cm), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.scatter(mfi_m,eq3_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_mf_eq3_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.16,0.04,'b) Small')
    ax.text( 0.16,0.02,'R=%5.2f'%(cs), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.scatter(mfi_s,eq3_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_mf_eq3_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    ##########################################
    print('################')
    print('MFI vs EQ4')
    print('################')

    call     =0 
    c_iop1   =0
    c_iop2   =0
    clall    =0 
    clrn     =0 
    clnr     =0 
    cm       =0 
    cs       =0

    call, sall = pearsonr(mfi,eq4_all)
    print('mf tke all',call)

    c_iop1, sall = pearsonr(mfi_1,eq4_1)
    print('mf tke iop1',c_iop1)

    c_iop2, sall = pearsonr(mfi_2,eq4_2)
    print('mf tke iop2',c_iop2)

    clrn, slrn = pearsonr(mfi_lrn,eq4_lrn)
    print('mf tke large rain',clrn)

    clnr, slnr = pearsonr(mfi_lnr,eq4_lnr)
    print('mf tke large not rain',clnr)

    clall, slall = pearsonr(mfi_lall,eq4_lall)
    print('mf tke large all',clall)

    cm  , sm   = pearsonr(mfi_m,eq4_m)
    print('mf tke medium',cm)

    cs  , ss   = pearsonr(mfi_s,eq4_s)
    print('mf tke small',cs)
    #############################
    fig,ax =fown.figure_scatter(0.4)
    ax.scatter(mfi_1,eq4_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(mfi_2,eq4_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.01,0.11,'R=%5.2f'%(call), fontsize=6)
    ax.text( 0.01,0.13,'a) IOPs')
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_mf_eq4_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.scatter( mfi_lrn,eq4_lrn,marker='o',facecolors='none',edgecolors='blue'  ,s=4)
    ax.scatter( mfi_lnr,eq4_lnr,marker='s',facecolors='none',edgecolors='k'     ,s=4)
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.01,0.16,'R=%5.2f'%(clall), fontsize=6)
    ax.text( 0.01,0.18,'d) Large')
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.legend(frameon=False,loc='upper right',markerfirst=False)
    fig.savefig('%sscatter_mf_eq4_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.25,0,0.25])
    ax.text(  0.01,0.18,'c) Medium')
    ax.text(  0.01,0.16,'R=%5.2f'%(cm), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.scatter(mfi_m,eq4_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_mf_eq4_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.25,0,0.25])
    ax.text( 0.01,0.18,'b) Small')
    ax.text( 0.01,0.16,'R=%5.2f'%(cs), fontsize=6)
    ax.set_xlabel(r' $\mathrm{uMF_{les}[kgm^{-2}s^{-1}]}$') 
    ax.set_ylabel(r' $\mathrm{uMF_{cb} [kgm^{-2}s^{-1}]}$') 
    ax.scatter(mfi_s,eq4_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_mf_eq4_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()

    #cin     =np.array(cin)
    #cin_1   =np.array(cin_1)
    #cin_2   =np.array(cin_2)
    #cin_all =np.array(cin_lall)
    #cin_lrn =np.array(cin_lrn)
    #cin_lnr =np.array(cin_lnr)
    #cin_m   =np.array(cin_m)
    #cin_s   =np.array(cin_s)

    #tke     =np.array(tke)
    #tke_1   =np.array(tke_1)
    #tke_2   =np.array(tke_2)
    #tke_all =np.array(tke_lall)
    #tke_lrn =np.array(tke_lrn)
    #tke_lnr =np.array(tke_lnr)
    #tke_m   =np.array(tke_m)
    #tke_s   =np.array(tke_s)

    #mfi     =np.array(mfi)
    #mfi_1   =np.array(mfi_1)
    #mfi_2   =np.array(mfi_2)
    #mfi_all =np.array(mfi_lall)
    #mfi_lrn =np.array(mfi_lrn)
    #mfi_lnr =np.array(mfi_lnr)
    #mfi_m   =np.array(mfi_m)
    #mfi_s   =np.array(mfi_s)

    #call, sall = pearsonr(mfi,cin/tke)
    #print(' c/t all',call)

    #c_iop1, sall = pearsonr(mfi_1,cin_1/tke_1)
    #print(' c/t iop1',m_iop1)

    #c_iop1, sall = pearsonr(mfi_2,cin_2/tke_2)
    #print(' c/t iop2',m_iop2)

    #clall, slall = pearsonr(mfi_lall,cin_lall/cin_lall)
    #print(' c/t large all',mlall)

    #clrn, slrn = pearsonr(mfi_lrn,cin_lrn/tke_lrn)
    #print(' c/t large rain',mlrn)

    #clnr, slnr = pearsonr(mfi_lnr,cin_lnr/tke_lnr)
    #print(' c/t large not rain',mlnr)

    #cm  , sm   = pearsonr(mfi_m,cin_m/tke_m)
    #print(' c/t medium',mm)

    #cs  , ss   = pearsonr(mfi_s,cin_s/tke_s)
    #print(' c/t small',cs)


    #fig,ax =fown.figure_scatter(0.4)
    #ax.scatter(mfi_1[:],cin_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    #ax.scatter(mfi_2[:],cin_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    #ax.axis( [0,0.1,0,1])
    #ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    #ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    #ax.legend(frameon=False,loc='upper right')
    #fig.savefig('%sscatter_mf_cin_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    #fig,ax =fown.figure_scatter(0.4)
    #ax.scatter(mfi_lrn[:],cin_lrn ,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    #ax.scatter(mfi_lnr[:],cin_lnr ,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    #ax.axis( [0,0.1,0,1])
    #ax.text( 0.01,1.30,'c) large')
    #ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    #ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    #ax.legend(frameon=False,loc='upper right')
    #fig.savefig('%sscatter_mf_cin_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    #fig,ax =fown.figure_scatter(0.4)
    #ax.axis( [0,0.1,0,1])
    #ax.text( 0.01,1.30,'b) Medium')
    #ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    #ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    #ax.scatter(mfi_m[:],cin_m[:],marker='s',facecolors='none',edgecolors='k',s=4)
    #ax.legend(frameon=False,loc='center left')

    #fig.savefig('%sscatter_mf_cin_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    #fig,ax =fown.figure_scatter(0.4)
    #ax.axis( [0,0.1,0,1])
    #ax.text( 0.01,1.30,'a) Small')
    #ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    #ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    #ax.scatter(mfi_s[:],cin_s[:],marker='s',facecolors='none',edgecolors='k',s=4)
    #ax.legend(frameon=False,loc='center left')

    #fig.savefig('%sscatter_mf_cin_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    #sb.jointplot(x = tke_lrn, y = cin_lrn,
    #          kind = "reg")
    #sb.jointplot(x = umf, y = massflux2,
    #          kind = "kde")
            
    return cin

def cin_uw(exp,days,exp_label,exp_case):


    k=0

    data=[]

    cin =[]
    cin_1 =[]
    cin_2 =[]
    cin_l=[]
    cin_lrn=[]
    cin_lnr=[]
    cin_lall=[]
    cin_m=[]
    cin_s=[]

    tke =[]
    tke_1 =[]
    tke_2 =[]
    tke_l =[]
    tke_lrn =[]
    tke_lnr =[]
    tke_lall =[]
    tke_m =[]
    tke_s =[]

    tke_cloud =[]
    tke_cloud_1 =[]
    tke_cloud_2 =[]
    tke_cloud_l =[]
    tke_cloud_lrn =[]
    tke_cloud_lnr =[]
    tke_cloud_lall =[]
    tke_cloud_m =[]
    tke_cloud_s =[]

    tke_all   =[]
    tke_all_1 =[]
    tke_all_2 =[]
    tke_all_l =[]
    tke_all_lrn =[]
    tke_all_lnr =[]
    tke_all_lall=[]
    tke_all_m =[]
    tke_all_s =[]

    mc      =[]
    mfi     =[]
    mfi_1   =[]
    mfi_2   =[]
    mfi_l   =[]
    mfi_lrn =[]
    mfi_lnr =[]
    mfi_lall=[]
    mfi_m   =[]
    mfi_s   =[]
    mfi2    =[]
    mfi3    =[]
    mup     =[]

    eq1_1   =[]
    eq1_2   =[]
    eq1_l   =[]
    eq1_lrn =[]
    eq1_lnr =[]
    eq1_lall=[]
    eq1_m   =[]
    eq1_s   =[]

    eq2_1   =[]
    eq2_2   =[]
    eq2_l   =[]
    eq2_lrn =[]
    eq2_lnr =[]
    eq2_lall=[]
    eq2_m   =[]
    eq2_s   =[]

    eq3_1   =[]
    eq3_2   =[]
    eq3_l   =[]
    eq3_lrn =[]
    eq3_lnr =[]
    eq3_lall=[]
    eq3_m   =[]
    eq3_s   =[]

    lcl_all         =   []         
    lfc_all         =   []         
    cb_all          =   []         
    tvmin_all       =   []         


    color   =[]
    marker  =[]
    alpha   =[]
    psize   =[]

    for ex in exp: 
    

        idi     = dt.datetime(days[k][0], days[k][1] ,days[k][2], days[k][3]) 
        idf     = dt.datetime(days[k][4], days[k][5] ,days[k][6], days[k][7])

        ni,nf= down.data_n(idi,idf,ex.data[:])

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
        specific_humidit_t	=   units.Quantity(ex.QT  ,'g/kg')

        alt            		=   units.Quantity(ex.z   ,'m')
        v_wind      		=   units.Quantity(ex.U   ,'m/seconds')
        u_wind      		=   units.Quantity(ex.V   ,'m/seconds')

        #Deep point temperature
        dw   	    =   mpy.dewpoint_from_specific_humidity( pressure[:], temperature[:,:],specific_humidity_v[:,:])


        mxr         =   mpy.mixing_ratio_from_specific_humidity(specific_humidity_v[:,:])
        tv          =   mpy.virtual_temperature(temperature[:,:],mxr[:])


        theta=np.zeros((ex.data.shape[0],ex.z.shape[0]))

        mean_theta  =   np.zeros(ex.data.shape[0])
        mean_temp   =   np.zeros(ex.data.shape[0])
        mean_mxr    =   np.zeros(ex.data.shape[0])
        mean_spec   =   np.zeros(ex.data.shape[0])
        dwp         =   np.zeros(ex.data.shape[0])



        z1,z2=down.level_n(25,100,ex.z)
        z3   =len(pressure)
        z0,z4=down.level_n(25,600,ex.z)

        z0=2

        #print(z0,z1,z3)

        t1   =   ex.data.shape[0]        

        tp =np.zeros((t1,z3-z0))
        tv =np.zeros((t1,z3-z0))
        tvp=np.zeros((t1,z3-z0))

        lcl         =   np.zeros(t1)         
        lfc         =   np.zeros(t1)         
        cb          =   np.zeros(t1)         
        tvmin       =   np.zeros(t1)         
        cin_flecher =   np.zeros(t1)
        tke_pbl     =   np.zeros(t1)
        mtke_cloud   =   np.zeros(t1)
        mtke_all     =   np.zeros(t1)
        mf          =   np.zeros(t1)


        for i in range(0,ex.data.shape[0]): 


            #from sam
            ipblh         =   np.argmin(ex.TVFLUX[i,1:50])
            tvmin[i]      =   ex.z[ipblh]

            #print(pressure[z0:z3],dwp)
            #lfc_c         =   mpy.lfc(pressure[z0:z3],temperature[i,z0:z3],dw[i,z0:z3],which='top')
            lfc_c         =   mpy.lfc(pressure[0:z3],temperature[i,0:z3],dw[i,0:z3],which='top')
            lfc[i]        =   lfc_c[0].magnitude

            lcl_m         =   mpy.lcl(pressure[z0], temperature[i,z0], dw[i,z0],max_iters=50,eps=1e-2)
            lcl[i]        =   lcl_m[0].magnitude


            #using lcl
            l1   ,l2      =   down.pressure_n(lcl[i],lfc[i],pressure[:].magnitude)

            #using pblheight
            l1=ipblh
            if l2<=l1:
                l2= l1+2

            #print('l1,l2',l1,l2)
            #cb[i]   =   ipblh 

            z       =   ex.z[l1:l2+1]
            l3      =   len(z)

            tp[i,:]       =   mpy.parcel_profile(pressure[z0:z3], temperature[i,z0], dw[i,z0]) 
            tvp           =   mpy.virtual_temperature(tp[i,l1:l2+1]*units('kelvin') ,mxr[i,l1:l2+1] ) 
            tv            =   mpy.virtual_temperature(temperature[i,l1:l2+1],mxr[i,l1:l2+1] ) 

            inte_cin      =   (tvp-tv)/(tv)
            cin_flecher[i]=   -9.81*integrate.simps(inte_cin,z)


            #if cin_flecher[i]<0:
            #    cin_flecher[i]=  1.0  
            

            if ipblh<=z0:
                 tke_pbl[i]=tke_pbl[z0]   
            else: 
                tke_pbl[i]    =   1.0/(ex.z[ipblh]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:ipblh],ex.z[z0:ipblh])


            #print(ipblh) 
            #Way to calculate the cloud top with tlflux
            #work!
            #TL=ex.TLFLUX[i][:]
            #for j in range(0,len(ex.z)):

            #    if j <= ipblh:

            #        TL[j]=-10.0 

            #tlmin =np.where(TL>-0.001)

            #if(len(tlmin[0])>0 ):
            #    
            #    icloud      = tlmin[0][0]
            #    
            #else:
            #    icloud=100

            #if(icloud>ipblh and icloud>z0 and icloud<100 ):

            #    mtke_cloud[i]= 1.0/(ex.z[icloud]-ex.z[ipblh])*integrate.simps(ex.TKE[i][ipblh:icloud],ex.z[ipblh:icloud])
            #    mtke_all[i]  = 1.0/(ex.z[icloud]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:icloud],ex.z[z0:icloud])
            #else:
            #    icloud=100
            #    mtke_cloud[i]= 1.0/(ex.z[icloud]-ex.z[ipblh])*integrate.simps(ex.TKE[i][ipblh:icloud],ex.z[ipblh:icloud])
            #    mtke_all[i]  = 1.0/(ex.z[icloud]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:icloud],ex.z[z0:icloud])

            #if ipblh<=z0:
            #     tke_pbl[i]=tke_pbl[z0]   
            #else: 
            #    tke_pbl[i]    =   1.0/(ex.z[ipblh]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:ipblh],ex.z[z0:ipblh])


            #eq1           =   0.06*(0.28*np.sqrt(tke_pbl[i])+0.64)*np.exp(-1.0*cin_flecher[i]/tke_pbl[i])
            eq2           =   0.4*(np.sqrt(tke_pbl[i]))*np.exp(-1.0*cin_flecher[i]/tke_pbl[i])
            #eq3           =   0.4*(np.sqrt(tke_pbl[i]))*np.exp(-1.0/tke_pbl[i])


            if ex.MCUP[i,l1]>0.005:

               data.append(ex.data[i]       )
               cin.append ( cin_flecher[i]  )
               tke.append ( tke_pbl[i]      )
               mfi.append ( ex.MCUP[i,l1]   )
               lcl_all.append(ex.z[l1])
               lfc_all.append(ex.z[l2])
               tvmin_all.append(tvmin[i])

               #mfi .append( mf[i])
               #mfi2.append( mf2)
               #mfi3.append( mf3)

               if exp_label[k][0:3]=='Feb' or exp_label[k][0:3]=='Mar':
                   #print(exp_label[k][0:3])
                   col='darkred'
                   mark='s'
                   alp=0.5
                   ps=20
                   cin_1.append(cin_flecher[i])
                   tke_1.append(tke_pbl[i])
                   tke_cloud_1.append(mtke_cloud[i])
                   tke_all_1.append(mtke_all[i])
                   mfi_1.append(ex.MCUP[i,l1])
                   #eq1_1.append(eq1)
                   eq2_1.append(eq2)
                   #eq3_1.append(eq3)
               else: 
                   cin_2.append(cin_flecher[i])
                   tke_2.append(tke_pbl[i])
                   tke_cloud_2.append(mtke_cloud[i])
                   tke_all_2.append(mtke_all[i])
                   mfi_2.append(ex.MCUP[i,l1])
                   #eq1_2.append(eq1)
                   eq2_2.append(eq2)
                   #eq3_2.append(eq3)

               if exp_case[k]=='large_rn':
                   col='darkred'
                   mark='s'
                   alp=0.5
                   ps=20
                   cin_lrn.append(cin_flecher[i])
                   tke_lrn.append(tke_pbl[i])
                   tke_cloud_lrn.append(mtke_all[i])
                   tke_all_lrn.append(mtke_all[i])
                   mfi_lrn.append(ex.MCUP[i,l1])
                   #eq1_lrn.append(eq1)
                   eq2_lrn.append(eq2)
                   #eq3_lrn.append(eq3)

               if exp_case[k]=='large':
                   col='red'
                   mark='o'
                   alp=0.5
                   ps=20
                   cin_lnr.append(cin_flecher[i])
                   tke_lnr.append(tke_pbl[i])
                   tke_cloud_lnr.append(mtke_cloud[i])
                   tke_all_lnr.append(mtke_all[i])
                   mfi_lnr.append(ex.MCUP[i,l1])
                   #eq1_lnr.append(eq1)
                   eq2_lnr.append(eq2)
                   #eq3_lnr.append(eq3)

               if exp_case[k]=='medium':
                   col='yellow'
                   mark='*'
                   alp=0.5
                   ps=20
                   cin_m.append(cin_flecher[i])
                   tke_m.append(tke_pbl[i])
                   tke_cloud_m.append(mtke_cloud[i])
                   tke_all_m.append(mtke_all[i])
                   mfi_m.append(ex.MCUP[i,l1])
                   #eq1_m.append(eq1)
                   eq2_m.append(eq2)
                   #eq3_m.append(eq3)

               if exp_case[k]=='small':
                   col='blue'
                   mark='d'
                   alp=0.5
                   ps=20
                   cin_s.append(cin_flecher[i])
                   tke_s.append(tke_pbl[i])
                   tke_cloud_s.append(mtke_cloud[i])
                   tke_all_s.append(mtke_all[i])
                   mfi_s.append(ex.MCUP[i,l1])
                   #eq1_s.append(eq1)
                   eq2_s.append(eq2)
                   #eq3_s.append(eq3)

               if exp_case[k]=='test':
                   col='white'
                   mark='p'
                   alp=0.3
                   ps=0.1

               color.append(col)
               marker.append(mark)
               alpha.append(alp)
               psize.append(ps)

        #fig,ax =fown.figure_sam(0.8)
        #plt.plot(data,cin)
        #fig,ax =fown.figure_sam(0.8)
        #plt.plot(data,lcl_all ,'r',label='lcl')
        #plt.plot(data,lfc_all ,'b',label='lfc')
        #plt.plot(data,tvmin_all,'g',label='tvmin')
        #ax.legend(frameon=False,loc='upper right')

        #plt.show()

        k=k+1

    #fig,ax =fown.figure_sam(0.8)
    #plt.plot(data,tke)

    #fig,ax =fown.figure_sam(0.8)
    #plt.plot(data,cin)

    #fig,ax =fown.figure_sam(0.8)
    #plt.plot(data,lcl_all ,'r',label='lcl')
    #plt.plot(data,lfc_all ,'b',label='lfc')
    #plt.plot(data,tvmin_all,'g',label='tvmin')
    #ax.legend(frameon=False,loc='upper right')

    #fig,ax =fown.figure_sam(0.4)
    #plt.plot(data,mfi)




    call, sall = pearsonr(tke,cin)
    print('all',call)

    fig,ax =fown.figure_scatter(0.4)
    #ax.text( 0.2,7,'Shallow Cases', fontsize=8)
    ax.axis( [0,2.0,0,8])
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    #ax.scatter(tke_1,cin_1,marker='s',color='blue'  ,s=4)
    #ax.scatter(tke_2,cin_2,marker='*',color='k',s=4)
    ax.scatter(tke_1,cin_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(tke_2,cin_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_uw_tke_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,2.0,0,8])
    ax.text( 0.1,7,'c) Large ')
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    ax.scatter(tke_lrn,cin_lrn,marker='s',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(tke_lnr,cin_lnr,marker='o',facecolors='none',edgecolors='k'    ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_uw_tke_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,2.0,0,8])
    ax.text( 0.1,7,'b) Medium')
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    ax.scatter(tke_m,cin_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_uw_tke_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,2.0,0,8])
    ax.text( 0.1,7,'a) Small')
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'CIN [$\mathrm{ms^{-1}}$]') 
    ax.scatter(tke_s,cin_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_cin_uw_tke_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)


    plt.show()

    ########################################
    fig,ax =fown.figure_scatter(0.4)
    #ax.text( 0.2,7,'Shallow Cases', fontsize=8)
    ax.axis( [0,0.2,0,0.2])
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'uMf [$\mathrm{ms^{-1}}$]') 
    #ax.scatter(tke_1,cin_1,marker='s',color='blue'  ,s=4)
    #ax.scatter(tke_2,cin_2,marker='*',color='k',s=4)
    ax.scatter(mfi_1,eq2_1,marker='o',facecolors='none',edgecolors='blue'  ,s=4, label='IOP1')
    ax.scatter(mfi_2,eq2_2,marker='s',facecolors='none',edgecolors='k'     ,s=4, label='IOP2')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_cin_uw_iop.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.2,0,0.2])
    ax.text( 0.2,0.2,'c) Large ')
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'uMf [$\mathrm{ms^{-1}}$]') 
    ax.scatter(mfi_lrn,eq2_lrn,marker='s',facecolors='none',edgecolors='blue' ,s=4, label='Rain')
    ax.scatter(mfi_lnr,eq2_lnr,marker='o',facecolors='none',edgecolors='k'    ,s=4, label='Not Rain')
    ax.legend(frameon=False,loc='upper right')
    fig.savefig('%sscatter_um_large.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.2,0,0.2])
    ax.text( 0.2,0.2,'b) Medium')
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'uMf [$\mathrm{ms^{-1}}$]') 
    ax.scatter(mfi_m,eq2_m,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_um_medium.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    fig,ax =fown.figure_scatter(0.4)
    ax.axis( [0,0.2,0,0.2])
    ax.text( 0.2,0.2,'a) Small')
    ax.set_xlabel(r'TKE [$\mathrm{ms^{-1}}$]') 
    ax.set_ylabel(r'uMf [$\mathrm{ms^{-1}}$]') 
    ax.scatter(mfi_s,eq2_s,marker='s',facecolors='none',edgecolors='k',s=4)
    ax.legend(frameon=False,loc='center left')
    fig.savefig('%sscatter_um_small.pdf'%(file_temp),bbox_inches='tight', format='pdf', dpi=1000)

    plt.show()
    ########################################
    ########################################



#work with a specific heigh defined cloud base in  z4 
def cape_flecher(exp,days,exp_label):


    k=0

    for ex in exp: 
    

        idi     = dt.datetime(days[k][3], days[k][2] ,days[k][1], days[k][2]) 
        idf     = dt.datetime(days[k][7], days[k][6] ,days[k][5], days[k][4])

        ni,nf= down.data_n(idi,idf,ex.data[:])

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
        specific_humidit_t	=   units.Quantity(ex.QT  ,'g/kg')

        alt            		=   units.Quantity(ex.z   ,'m')
        v_wind      		=   units.Quantity(ex.U   ,'m/seconds')
        u_wind      		=   units.Quantity(ex.V   ,'m/seconds')

        #Deep point temperature
        dw   	    =   mpy.dewpoint_from_specific_humidity( pressure[:], temperature[:,:],specific_humidity_v[:,:])

        mxr         =   mpy.mixing_ratio_from_specific_humidity(specific_humidity_v[:,:])
        tv          =   mpy.virtual_temperature(temperature[:,:],mxr[:])


        theta=np.zeros((ex.data.shape[0],ex.z.shape[0]))

        mean_theta  =   np.zeros(ex.data.shape[0])
        mean_temp   =   np.zeros(ex.data.shape[0])
        mean_mxr    =   np.zeros(ex.data.shape[0])
        mean_spec   =   np.zeros(ex.data.shape[0])
        dwp         =   np.zeros(ex.data.shape[0])


        #funcionando arm kwajex
        #z1,z2=down.level_n(200,500,ex.z)
        #z3   =len(pressure)
        #z0,z4=down.level_n(300,600,ex.z)

        z1,z2=down.level_n(200,400,ex.z)
        z3   =len(pressure)
        z0,z4=down.level_n(300,600,ex.z)

        #z4=z4+1

        t1   =   ex.data.shape[0]        
        tp =np.zeros((t1,z3-z0))
        tv =np.zeros((t1,z3-z0))
        tvp=np.zeros((t1,z3-z0))

        lcl         =   np.zeros(t1)         
        tvmin       =   np.zeros(t1)         
        cin_flecher =   np.zeros(t1)
        tke_pbl     =   np.zeros(t1)
        mf          =   np.zeros(t1)

        data=[]
        mc  =[]
        cin =[]
        tke =[]
        mfi =[]

        for i in range(0,ex.data.shape[0]): 

            #theta[i,:]    =   mpy.potential_temperature(pressure[:],temperature[i,:])
            #mean_theta[i] =   np.mean(theta[i,z1:z2])

            mean_mxr[i]   =   np.mean(mxr[i,z1:z2].magnitude)*(units('g/kg')) 

            #standar deviation
            qv_s          =   np.std(specific_humidity_v[i,z1:z2].magnitude,axis=0)
            mean_spec[i]  =   (np.mean(specific_humidity_v[i,z1:z2].magnitude)+qv_s)*(units('g/kg')) 


            temp          =   np.mean(temperature[i,z1:z2])
            dwp           =   mpy.dewpoint_from_specific_humidity( pressure[z0],temp,mean_spec[i])#.magnitude



            #parcel from z1 to end z3 
            tp[i,:]       =   mpy.parcel_profile(pressure[z0:z3], temp, dwp) 

            tvp           =   mpy.virtual_temperature(tp[i,:]*units('kelvin') ,mxr[i,z0:z3] ) 
            tv            =   mpy.virtual_temperature(temperature[i,z0:z3],mxr[i,z0:z3] ) 


            ibf       =   np.argmin(ex.TVFLUX[i,1:16])         
            tvmin[i]    =   ex.z[ibf]        

            z=ex.z[z0:z4]
            l3=len(z)
            #print(z[:],tvp[0:l3])
            #print(z[:],tvp[0:l3])
            #print(z0,z4)
            inte_cin      =   (tvp[0:l3]-tv[0:l3])/(tv[0:l3])
            cin_flecher[i]=   -9.81*integrate.simps(inte_cin,z)
            #print(cin_flecher[i])

            tke_pbl[i]    =   1.0/(ex.z[z4]-ex.z[z0])*integrate.simps(ex.TKE[i][z0:z4],ex.z[z0:z4])


            mf[i]         =   0.06*(0.28*np.sqrt(tke_pbl[i])+0.64)*np.exp(-1*cin_flecher[i]/tke_pbl[i])

            if ex.MCUP[i,z4]>0.005:

                data.append(ex.data[i])
                cin.append(cin_flecher[i])
                tke.append(tke_pbl[i])
                mfi.append(mf[i])

        fig = plt.figure()
        #####New axis
        ax  = plt.axes()
        #plt.plot(ex.data,lcl ,'red',label=' LCL')
        plt.plot(ex.data,tvmin ,'blue',label=' tvmin')


        tk=np.array(tke)
        ci=np.array(cin)

        corr1, st3 = pearsonr(tke,cin)
        print(corr1)
        #op=0.06*(0.28*np.sqrt(tk)+0.64)*np.exp(-1*ci/tk)
        
        fig = plt.figure()
        ####New axis
        ax  = plt.axes()
        #plt.plot(ex.data,np.sqrt(cin_flecher) ,'orange',label=' CIN Flecher')
        #plt.plot(ex.data,np.sqrt(tke_pbl)     ,'blue'  ,label=' TKE Flecher')
        plt.plot(data,np.sqrt(cin) ,'red',label=' CIN Flecher')
        plt.plot(data,np.sqrt(tke) ,'blue',label=' TKE')
        plt.axis([ data[0],data[len(data)-1],-1, 5])
        ax.legend(frameon=False)


        fig = plt.figure()
        #####New axis
        ax  = plt.axes()
        plt.plot(data,mfi ,'black',label=' MCUP')
        ax.legend(frameon=False)


        fig = plt.figure()
        ####New axis
        ax  = plt.axes()
        ax.legend(frameon=False)

        plt.scatter(tk,ci ,color='blue',marker='s')


        plt.show()

        k=k+1

    return cin

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
