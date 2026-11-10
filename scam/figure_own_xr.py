import  numpy as np

import  matplotlib.pyplot as plt

#Color map
from    matplotlib.colors import LinearSegmentedColormap

from matplotlib.ticker import (MultipleLocator, LinearLocator,NullFormatter,
                                   ScalarFormatter)
import matplotlib.ticker as tkr


#To work with date in plots 
import  matplotlib.dates as mdates

import  matplotlib as mpl

from datetime import datetime, timedelta

import datetime as dt

import  sam_python.data_own as down

#Filter the function, more smothy
from scipy.signal import lfilter

import scipy.ndimage as ndimage

import subprocess, sys

import importlib

import xarray as xr

import  sam_python.plotparameters      as pp

import os

import nc_time_axis

import cftime


#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/sam_python/', shell = True, executable="/bin/bash")

#used the user parameter to plot(plotparameter.py) if para:
#pars=__import__('source.Parameters_default',globals())
pars=importlib.import_module('.Parameters_default','sam_python',)

if hasattr(pars, "out_table"):
    file1 = f"{pars.out_table}table_days.tex"
    file2 =f"{pars.out_table}table_days_14.tex"
    file3 =f"{pars.out_table}table_days_15.tex"
else:
    print("out_table folder  does not exist, created in the run directory")
    file1 =f"table_days.tex"
    file2 =f"table_days_14.tex"
    file3 =f"table_days_15.tex"


    #os.remove(file1)
    #os.remove(file2)
    #os.remove(file3)
#except FileNotFoundError:
    #os.remove(file1)
    #os.remove(file2)
    #os.remove(file3)


#Color map
#########
#cmap = LinearSegmentedColormap.from_list('mycmap', ['skyblue','blue','navy','steelblue','lightskyblue','white'])
cmap = LinearSegmentedColormap.from_list('mycmap', ['white','lightblue','skyblue','RoyalBlue','blue','darkblue'])
cmap3 = LinearSegmentedColormap.from_list('mycmap', ['white','silver','blue','green','yellow'], N=256, gamma=0.5)
cmap4 = LinearSegmentedColormap.from_list('mycmap', ['white','grey','lightblue','blue','green','yellow'], N=256, gamma=1.0)



def d2_plot_im_diff(var,z,alt,contour,colors,explabel,leg_loc,hours=[]):


    #Data to plot 
    #used user parameter to plot(plotparameter.py
    #mpl.rcParams.update(params_2d)

    size_wg = leg_loc[6][0]
    size_hf = leg_loc[6][1]
    cmas    = leg_loc[6][2]
    #parameters plot
    try:
        plotdef   = leg_loc[6][3]

    except:
        plotdef   = pars.plotdef
        
    tama= pp.plotsize(size_wg,size_hf, cmas,plotdef)

    ################################3
    fig = plt.figure()
    ###New axis
    ax  = plt.axes()

    try:
        x       =  var.Time[:]
    except:
        x       =  var.time[:].values

    sx= x.shape[0]
    #sxx= var.shape[0]

    sy= z.shape[0]


    #x=np.zeros(sx)
    y=np.zeros(sy)
    MF=np.zeros((sx,sy))
    
    # with the data and no time

    y       =   z[:]/1000.0

    #Variable to plot
    #MF      =   var[0:sx,0:sy].values 
    MF      =   var.values 

    if colors=='cloud':
        colors=cmap

    if colors=='whbuyl':
        colors=cmap3


    X,Y= np.meshgrid(x,y)

    levels= np.linspace(contour[0],contour[1],contour[2],endpoint=True)
    #levels= np.arange(contour[0],contour[1],contour[2])

    #Z = ndimage.gaussian_filter(MF.T, sigma=1.0, order=0)

    #CU=ax.contourf(X,Y,MF.T,levels=levels, interpolation='bilinear',origin='lower',cmap=colors,aspect='auto',extend='both');
    #CU=plt.contourf(X,Y,MF.T,levels=levels[0:len(levels):1],origin='lower',cmap=colors,extend='max');
    CU=plt.contourf(X,Y,MF.T,levels=levels[0:len(levels):1],origin='lower',cmap=colors,extend='neither');

    #CU=ax.contourf(X,Y,Z,levels=levels,origin='lower',cmap=colors);

    #plt.grid(color = 'gray', linestyle = '--', linewidth = 0.25)
    #plt.grid(color = 'gray', linestyle = '--', linewidth = 0.25)
    plt.grid(color = 'gray',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0] )

    # Set all level lines to black
    #line_colors = ['black' for l in CU.levels]
    line_colors = ['darkgrey' for l in CU.levels]

    #Contour plot 
    CS=ax.contour(X,Y,MF.T,levels=levels[0:len(levels):2],colors=line_colors,linewidths=0.1 );


    #plot_bar
    if(leg_loc[2][1]):


        try: 
            forma=leg_loc[2][3]
        except:
            forma='%.2f'

        #CB = plt.colorbar()
        CB = fig.colorbar(CU, shrink=1.0, extend='neither',orientation=leg_loc[2][0], format=tkr.FormatStrFormatter(forma))


        CB.ax.tick_params(labelsize=tama) 


        if(contour[0]>contour[1]):

            kk= np.linspace(contour[0],0,11,endpoint=True,)
            cbarlabels=kk

        elif(contour[0]<0):

            cbarlabels = np.linspace(contour[0],contour[1] ,contour[2],endpoint=True)
            #cbarlabels=cbarlabels[1::]-contour[0]
            CB.set_ticks(cbarlabels[0::2])

        else:
            cbarlabels = np.linspace(contour[0],contour[1],contour[2],endpoint=True)
            #print(contour[0],contour[1],contour[2])
            #exit()
            #cbarlabels = np.arange(contour[0]-contour[0],contour[1],contour[2])

            CB.set_ticks(cbarlabels[1:len(levels):2]) 
            #CB.set_ticks(cbarlabels[0:len(levels):2]) 

        #CB.set_ticks(cbarlabels[0::3])
        CB.ax.set_title(r' %s'%leg_loc[2][2],size=tama-1)

    calendar = X[0, 0].calendar

    date_form = nc_time_axis.CFTimeFormatter("%H", calendar)
    ax.xaxis.set_major_formatter(date_form)
    
    locatormax = nc_time_axis.NetCDFTimeDateLocator(
        max_n_ticks=10,
        calendar=calendar
    )

    ax.xaxis.set_major_locator(locatormax)

    locatormin = nc_time_axis.NetCDFTimeDateLocator(
        max_n_ticks=20,
        calendar=calendar
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
    #ax.xaxis.set_minor_locator(locatormin)

    #print("major:", ax.xaxis.get_majorticklocs())
    #print("minor:", ax.xaxis.get_minorticklocs())


    if hours:
        ax.set_xlim([hours[0],hours[1]])


    ax.set_ylim([alt[0],alt[1]])

    #try: 
    #    ax.yaxis.set_major_locator(plt.MultipleLocator(alt[2]))
    #except:
    #    ax.yaxis.set_major_locator(plt.MultipleLocator(1.0))

    #ax.yaxis.set_major_locator(plt.MultipleLocator(2.0))
    ax=label_plots(x,ax,leg_loc,explabel[1],explabel[2],tama)

    #plt.savefig('%s/vertical_2d_%s.pdf'%(pars.out_fig,explabel[0]),bbox_inches='tight',dpi=200, format='pdf')

    return fig,ax    

def temporal(fig,ax,toplot,var):

    
    ax2 = ax.twinx()

    ax2.axhline(y=0.5, color='r', linestyle='--', linewidth=1)

    ax2.plot(toplot.time[:].values,toplot[var[0]].values,color='lime')

    ax2.set_ylabel(r'[mmh$^{-1}$]',fontsize=8)


    ax2.set_ylim([var[1][0],var[1][1]])
    
    #ax2.xaxis_date()
    ##date_form = mdates.DateFormatter("%H" )
    ##ax2.xaxis.set_major_formatter(date_form)
    ##
    ##locatormax = mdates.HourLocator(interval=2)
    ##locatormin = mdates.HourLocator(interval=1)
    ##ax2.xaxis.set_minor_locator(locatormin)
    #ax2.xaxis.set_major_locator(locatormax)
    
    #if hours:
    #ax2.set_xlim([hours[0],hours[1]])

    return fig,ax,ax2

def base_top_cloud_ghost(fig,ax,ex,color):

    size= ex.time.shape[0]
    tam = ex.MCUP.shape[0]

    #max heigh points
    #ex: resolution (50m)*30
    #for gomazon paper 
    #maxl=30

    #for arm paper 
    maxl=100

    ctop  =[]
    ctop2 =[]
    clfc  =[]
    cbase =[]
    cbase2=[]
    pblh  =[]
    cmflx =[]

    #lim_qc=0.0025
    lim_qc=0.0025

    for i in range(0,tam):

        index1  =  np.argmin(ex.TVFLUX[i][0:maxl].values)
        #print(index1,ex.TVFLUX[i][index1].values)

        indexmc =  np.max(  ex.MCUP[i][:].values)
        indexc  =  np.argmax(   ex.CLD[i][0:maxl].values)

        for j in range(0,20):

            index2=index1+j

            if (ex.QC[i][index2].values > lim_qc) and (index1>5):

                indexbase=index2

                break

            else:
                indexbase=index1


        indexmin=index1
        for j in range(0,20):

            #index3=indexbase+j
            index3=index1+j

            if ex.TVFLUX[i][index3].values>0:

                #print(ex.TVFLUX[i][index1].values,ex.TVFLUX[i][index3].values)
                
                indexmin=index3

                break

            #else:
            #    indexmin=index1

        #for gomazon paper
        for j in range(0,80):

            index4=indexbase+j
            #index4=index1+j

            if (ex.QC[i][index4].values < lim_qc):

                indexmax=index4

                break

            #else:
            #    indexmax=indexbase


        pblh.append(ex.z[index1].values/1000.0)
        clfc.append(ex.z[indexmin].values/1000.0)
        cmflx.append(ex.MCUP[i,indexmin].values)
        cbase.append(ex.z[indexbase].values/1000.0)
        cbase2.append(ex.z[indexc].values/1000.0)
        ctop.append(ex.z[indexmax].values/1000.0)

    step=1

    #Limits of time date
    #idi2     = datetime(ex.datei.year,ex.datei.month,ex.datei.day,10)#dt.datetime(2014, days[2] ,days[0], 10)
    #idf2     = datetime(ex.datef.year,ex.datef.month,ex.datef.day,18)#dt.datetime(2014, days[2] ,days[0], 10)
    ##idf2     = ex.datef#dt.datetime(2014, days[3] ,days[0], 18)

    year=ex.time[0].dt.year.values
    month=ex.time[0].dt.month.values
    day=ex.time[0].dt.day.values


    date_format = '%Y-%m-%dT%H:%M'
    idi2=dt.datetime.strptime('%s-%s-%sT10:20'%(year,month,day), date_format)
    idf2=dt.datetime.strptime('%s-%s-%sT17:00'%(year,month,day), date_format)
    time1 = np.datetime64(idi2) 
    time2 = np.datetime64(idf2) 

    ni2,nf2= down.data_n(time1,time2,ex.time[:].values)

    # To find 13 and 14 hours
    #i13     = datetime(ex.datef.year,ex.datef.month,ex.datef.day,13)#dt.datetime(2014, days[2] ,days[0], 10)
    #i14     = datetime(ex.datef.year,ex.datef.month,ex.datef.day,14)#dt.datetime(2014, days[2] ,days[0], 10)
    i13=dt.datetime.strptime('%s-%s-%sT13:20'%(year,month,day), date_format)
    i14=dt.datetime.strptime('%s-%s-%sT14:00'%(year,month,day), date_format)
    i3 = np.datetime64(i13) 
    i4 = np.datetime64(i14) 

    n13,n14= down.data_n(i3,i4,ex.time[:].values)


    #TO find the cloud fraction max
    cbi    =np.argmax(cbase)
    cbmax   =cbase[cbi]
    cbmax14 =cbase[n14]

    #TO find the mass flux max
    mfi   =np.argmax(cmflx)
    mfx   =np.argmax(idxmmf)
    cb_mf =cbase[mfx]

    mfmax =cmflx[mfi]
    cbmf  =cbase[mfi]

    #Tree ways to calculate the max 
    #topmax=np.max(ctop)

    top_cb  =ctop[cbi]
    top_14  =ctop[n14]
    top_mc  =ctop[mfi]
    top_mf  =ctop[mfx]

    ###print(ex.time[mfi],'mfmax')
    ###print(ex.time[cbi],'cbmax')
    ####print(ex.date[n14],'14')


    ################
    print('######')
    print('CB base='   ,cbmax)
    print('CB base 14=',cbmax14)
    print('MF base='   ,cbmf)

    #############
    print('######')
    print('CB top='   ,top_cb)
    print('CB top 14=',top_14)
    print('MF top='   ,top_mf)

    #############
    print('######')
    print('CB    Deep=',top_cb-cbmax)
    print('CB 14 Deep=',top_14-cbmax14)
    print('MF Deep=',top_mf-cbmf)
    

    n = 4#nf2-ni2  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1


    cbasef = lfilter(b, a, cbase)

    #lfcbf  = lfilter(b, a, clfc)

    pblhf = lfilter(b, a, pblh)

    ctopf = lfilter(b, a, ctop)

    n = 10#nf2-ni2  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1

    lfcbf  = lfilter(b, a, clfc)


    ax.plot( ex.time[ni2:nf2:step]     , pblhf[ni2:nf2:step]  ,color=color[0]     ,linewidth=1.0,alpha=1.0,marker='')

    ax.plot( ex.time[ni2:nf2:step]     , cbasef[ni2:nf2:step] ,color=color[1] ,dashes=[1,0]  ,linewidth=1.0,alpha=1.0,marker='')

    ax.plot( ex.time[ni2:nf2:step]     , lfcbf[ni2:nf2:step]  ,color='lime' ,  dashes=[1,0]  ,linewidth=1.0,alpha=1.0,marker='')

    ax.plot( ex.time[ni2:nf2:step]     , ctopf[ni2:nf2:step]  ,color=color[2] ,  dashes=[1,1]  ,linewidth=1.0,alpha=1.0,marker='')



    ytex,ytex2= down.data_n(time1,time2,ex.time[:].values)


    #pblh
    text1=r'$\mathrm{Z_i}$'
    idtex1    = idf2-timedelta(hours=0, minutes=0)
    ax.text(idtex1,pblhf[ytex2] -0.3 , r' %s'%(text1), fontsize=6, color=color[0])

    text2   =r'$\mathrm{h_{b}}$'
    #text2   =''#'$\mathrm{h_{b}}$'
    idtex2    = idf2-timedelta(hours=0, minutes=0)
    ax.text(idtex2, cbasef[ytex2]+0.0 , r' %s'%(text2), fontsize=7, color=color[1])

    text3='LFC'
    ##text1='NCL'
    #idtex3  = idf2-timedelta(hours=2, minutes=30)
    #ax.text(idtex3,cbase2[ytex2]+0.1 , r' %s'%(text3), fontsize=6, color='lime')

    text4=r'$\mathrm{h_{t}}$'
    #text3='$\mathrm{h_{topo}}$'
    idtex4    = idf2-timedelta(hours=0, minutes=00)
    ax.text(idtex4,ctopf[ytex2]+0.2 , r' %s'%(text4), fontsize=7, color=color[1])

    #if ex.name=='m_w_l' or  ex.name=='large':
    #    ax.text(idtex3,ctopf[ytex2]-0.4 , r' %s'%(text3), fontsize=7, color='black')
    #else :

    return fig,ax


def base_top_cloud(fig,ax,ex,color,plotime):


    size= ex.time.shape[0]
    tam = ex.MCUP.shape[0]


    #max heigh points
    #ex: resolution (50m)*30
    #for gomazon paper 
    #maxl=30

    #for arm paper 
    #maximum lev of pbl base
    maxl=200
    #print(ex.z[maxl].values)
    #exit()

    ctop  =[]
    ctop2 =[]

    clfc  =[]

    cbase =[]
    cbase2=[]

    pblh  =[]

    mcf   =[]
    mmf   =[]

    indextop=-1

    #lim_qc=0.0025
    #lim_qc=0.0025
    lim_qc=0.0025
    lim_qc2=0.0010000
    #i14     = datetime(ex.datef.year,ex.datef.month,ex.datef.day,14)#dt.datetime(2014, days[2] ,days[0], 10)

    date_format = '%Y-%m-%dT%H:%M'
    year    =ex.time[0].dt.year.values
    month   =ex.time[0].dt.month.values
    day     =ex.time[0].dt.day.values

    i10    = dt.datetime.strptime('%s-%s-%sT9:00'%(year,month,day), date_format)
    i17    = dt.datetime.strptime('%s-%s-%sT19:00'%(year,month,day), date_format)
    time10 = np.datetime64(i10) 
    time17 = np.datetime64(i17) 
    n10,n17= down.data_n(time10,time17,ex.time[:].values)


    ex=ex.sel(time=slice(i10, i17))

    time   = ex.time
    tam2   = len(time)
    
    for i in range(0,tam2):

        #to find the minimum and maximum index 
        indexpbl =  np.argmin(ex.TVFLUX[i][0:maxl].values)
        indexmf  =  np.argmax(ex.MCUP[i][0:maxl].values)
        indexcf  =  np.argmax(ex.CLD[i][0:maxl].values)

        #print(ex.z[indexpbl].values,ex.TVFLUX[i][indexpbl].values)


        ##fig2, ax2 = plt.subplots()
        ##ax2.plot(ex.TVFLUX[i][:].values,ex.z[:].values)
        #ax2.plot(ex.TVFLUX[i][indexpbl].values,ex.z[indexpbl].values,color='red', marker='p')

        #plt.show()

        for j in range(0,40):

            index2=indexpbl+j

            #to define the index of cloud base from the pbltop 
            #if (ex.QCL[i][index2].values > lim_qc) :
            if (ex.QC[i][index2].values > lim_qc) and (index2 > indexpbl):

                indexbase=index2

                break

            else:
                indexbase=indexpbl+1


        indexlfc=indexpbl
        for j in range(0,20):

            #index3=indexbase+j
            index3=indexpbl+j

            #Were the buoyancy flux begins positive 
            if ex.TVFLUX[i][index3].values>0:

                indexlfc=index3

                break

        #for gomazon paper
        #for j in range(0,150):
        #300 maximum heigh level
        for j in range(-4,40):

            if indextop<0:

                index4=indexpbl+j+8 #começa de 2 acima de pbl

            else: 
                index4=indextop+j#+10+1
            #index4=indexpbl+j

            if ( ex.QC[i][index4].values < lim_qc2):

                indextop=index4

                break

        if indextop-indexpbl<0:
            ctop.append(np.nan)
            indextop=-1
        else:
            ctop.append(ex.z[indextop].values/1000.0)

        #if indexbase-indexpbl<0:
        #    cbase.append(ex.z[indexpbl].values/1000.0)

        #else:
        cbase.append(ex.z[indexbase].values/1000.0)

        pblh.append(ex.z[indexpbl].values/1000.0)
        clfc.append(ex.z[indexlfc].values/1000.0)
        #append the height of the maximum mf and cf
        mmf.append(ex.z[indexmf].values/1000.0)
        mcf.append(ex.z[indexcf].values/1000.0)

    step=1


    idi2=dt.datetime.strptime('%s-%s-%sT%s'%(year,month,day,plotime[0]), date_format)
    idf2=dt.datetime.strptime('%s-%s-%sT%s'%(year,month,day,plotime[1]), date_format)
    time1 = np.datetime64(idi2) 
    time2 = np.datetime64(idf2) 

    ni2,nf2= down.data_n(time1,time2,ex.time[:].values)

    # To find 13 and 14 hours
    i13=dt.datetime.strptime('%s-%s-%sT13:00'%(year,month,day), date_format)
    i14=dt.datetime.strptime('%s-%s-%sT14:00'%(year,month,day), date_format)
    i3 = np.datetime64(i13) 
    i4 = np.datetime64(i14) 
    n13,n14= down.data_n(i3,i4,ex.time[:].values)

    i15=dt.datetime.strptime('%s-%s-%sT15:00'%(year,month,day), date_format)
    i16=dt.datetime.strptime('%s-%s-%sT16:00'%(year,month,day), date_format)
    i5 = np.datetime64(i15) 
    i6 = np.datetime64(i16) 
    n15,n16= down.data_n(i5,i6,ex.time[:].values)

    #"""
    #maximum cloud base
    cbi        =np.argmax(cbase)
    base_max   =cbase[cbi]
    top_max    =ctop[cbi]
    #ZCB:long_name = "GCSS Mean Cloud-base Height"
    #ZCBMIN:long_name = "GCSS Minimum Cloud-base Height" ;
    #ZCTMAX:long_name = "GCSS Maximum Cloud-top Height" ;
    #ZCT:long_name = "GCSS Mean Cloud-top Height" ;
    base_sam   =ex.ZCB[cbi]/1000.0
    top_sam    =ex.ZCT[cbi]/1000.0
    basem_sam   =ex.ZCBMIN[cbi]/1000.0
    topm_sam    =ex.ZCTMAX[cbi]/1000.0
    
    #cloud base at n14 and n15 hours
    cbmax14 =cbase[n14]
    cbmax15 =cbase[n15]
    top_14  =ctop[n14]
    top_15  =ctop[n15]

    #TO find  time of maximum mass flux max and cloud base
    imfmax =np.argmax(mmf)
    icfmax =np.argmax(mcf)

    cb_mcf =cbase[imfmax]
    cb_mmf =cbase[icfmax]

    top_mcf  =ctop[icfmax]
    top_mmf  =ctop[imfmax]


    #############
    # Open the file safely using 'with'
    with open(
        "/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/SCM_IOPS_LEV_p0/python/table_days.tex",
        "a",
    ) as file1: 

        file1.write(
        f"# &{str(ex.name.values)}& {base_max:.3f}& {top_max:.3f} & {top_max - base_max:.3f} &\\\\ \n")

    with open(
        "/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/SCM_IOPS_LEV_p0/python/table_days_14.tex",
        "a",
    ) as file2: 

        file2.write(
        f"# &{str(ex.name.values)}& {cbmax14:.3f}& {top_14:.3f} & {top_14 - cbmax14:.3f} &\\\\ \n")

    with open(
        "/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/SCM_IOPS_LEV_p0/python/table_days_15.tex",
        "a",
    ) as file3: 

        file3.write(
        f"# &{str(ex.name.values)}& {cbmax15:.3f}& {top_15:.3f} & {top_15 - cbmax15:.3f} &\\\\ \n")

    print(
    f"# &{str(ex.name.values)}& {base_max:.3f}({cbmax14:.3f})& {top_max:.3f}({top_14:.3f}) & {top_max - base_max:.3f}({top_14 - cbmax14:.3f}) \\\\ "
    )
    ##print( 
    ##       f'{str(ex.name.values)}
    ##       & {base_max:.3f}({cbmax14:.3f})-{base_sam:.3f}({basem_sam:.3f})
    ##       & {top_max:.3f}({top_14:.3f})-{top_sam:.3f}({topm_sam:.3f}) 
    ##       & {top_max:.3f-base_max:.3f}({top_14:.3f-cbmax14:.3f})-{base_sam:.3f-top_sam:.3f}({basem_sam:.3f-topm_sam:.3f})
    ##       &\\\\ '
    ##       )
    ##print('Base Top, Deep 15') 
    ##print( f'{str(ex.name.values)}
    ##       & {base_max:.3f}({cbmax15:.3f})-{base_sam:.3f}({basem_sam:.3f})
    ##       & {top_max:.3f}({top_15:.3f})-{top_sam:.3f}({topm_sam:.3f}) 
    ##       & {top_max:.3f-base_max:.3f}({top_15:.3f-cbmax15:.3f})-{base_sam:.3f-top_sam:.3f}({basem_sam:.3f-topm_sam:.3f})
    ##       &\\\\ ")
    

    n = 2#nf2-ni2  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1.0


    cbasef = lfilter(b, a, cbase)

    #lfcbf  = lfilter(b, a, clfc)

    pblhf = lfilter(b, a, pblh)

    #try:
    ctopf = lfilter(b, a, ctop)
    #except:
    #    ctopf = ctop 

    #try:
    lfcbf  = lfilter(b, a, clfc)
    #except:
    #    lfcbf  = clfc

    #n = 1#nf2-ni2  # the larger n is, the smoother curve will be
    #b = [1.0 / n] * n
    #a = 1

    ytex,ytex2= down.data_n(time1,time2,time[:].values)


    if color[0]:

        ax.plot( time[ni2:nf2:step]     , pblh[ni2:nf2:step]  ,color=color[0]     ,linewidth=1.0,alpha=1.0,marker='')

        #pblh
        text1=r'$\mathrm{Z_i}$'
        idtex1    = idf2-timedelta(hours=0, minutes=0)

        ax.text(idtex1,pblhf[ytex2] -0.3 , r' %s'%(text1), fontsize=6, color=color[0])

    if color[1]:

        ax.plot( time[ni2:nf2:step]     , cbase[ni2:nf2:step] ,color=color[1] ,dashes=[1,0]  ,linewidth=1.0,alpha=1.0,marker='')
        text2   =r'$\mathrm{h_{b}}$'
        idtex2    = idf2-timedelta(hours=0, minutes=0)
        ax.text(idtex2, cbasef[ytex2]+0.0 , r' %s'%(text2), fontsize=7, color=color[1])

    #ax.plot(time[ni2:nf2:step]     , lfcbf[ni2:nf2:step]  ,color='lime' ,  dashes=[1,0]  ,linewidth=1.0,alpha=1.0,marker='')

    if color[2]:

        ax.plot( time[ni2:nf2:step]     , ctopf[ni2:nf2:step]  ,color=color[2] ,  dashes=[1,1]  ,linewidth=1.0,alpha=1.0,marker='')

        text4=r'$\mathrm{h_{t}}$'
        #text3='$\mathrm{h_{topo}}$'
        idtex4    = idf2-timedelta(hours=0, minutes=00)
        ax.text(idtex4,ctopf[ytex2]+0.2 , r' %s'%(text4), fontsize=7, color=color[2])


    text3='LFC'
    ##text1='NCL'
    idtex3  = idf2-timedelta(hours=2, minutes=30)
    #ax.text(idtex3,cbase2[ytex2]+0.1 , r' %s'%(text3), fontsize=6, color='lime')


    return fig,ax

def label_plots(time,ax,legend,explabel1,explabel2,tama): 

    #leg_loc      =  ( [ 0.5,4.2],[ 0.5,4.2],[vertical,True],[xlabel,'True'],[ylabel,'True'],[size_wg,size_hf])

    xlabel=legend[3][0]

    ylabel=legend[4][0]

    date_format = '%Y-%m-%dT%H:%M'

    if legend[0]:

        ti = str_to_noleap(legend[0][0], date_format)
        #print(ti)
        #exit()

        ax.text(
            ti,
            legend[0][1],
            r' %s' % explabel1,
            fontsize=tama-1,
            color='black'
        )

    if legend[1]:
 
        ax.text(ti, legend[1][1], r' %s'%(explabel2), fontsize=tama-1, color='black')
 
    if( legend[3][1]==True):

        plt.xlabel(r'%s'%(xlabel), fontsize=tama-1) 
 
    if( legend[4][1]==True):
        plt.ylabel(r'%s'%(ylabel), fontsize=tama-1) 

    return ax

def str_to_noleap(date_string, date_format):

    d = dt.datetime.strptime(date_string, date_format)

    return cftime.DatetimeNoLeap(
        d.year,
        d.month,
        d.day,
        d.hour,
        d.minute,
        d.second
    )

    return

def base_top_cloud_ghost_old(fig,ax,ex,color):

    size= ex.time.shape[0]
    tam = ex.MCUP.shape[0]

    #max heigh points
    #ex: resolution (50m)*30
    #for gomazon paper 
    #maxl=30

    #for arm paper 
    maxl=100

    ctop  =[]
    ctop2 =[]
    clfc  =[]
    cbase =[]
    cbase2=[]
    pblh  =[]
    cmflx =[]

    #lim_qc=0.0025
    lim_qc=0.0001

    for i in range(0,tam):

        index1  =  np.argmin(ex.TVFLUX[i][0:maxl].values)
        #print(index1,ex.TVFLUX[i][index1].values)

        indexmc =  np.max(  ex.MCUP[i][:].values)
        indexc  =  np.argmax(   ex.CLD[i][0:maxl].values)

        for j in range(0,20):

            index2=index1+j

            if (ex.QC[i][index2].values > lim_qc) and (index1>5):

                indexbase=index2

                break

            else:
                indexbase=index1


        indexmin=index1
        for j in range(0,20):

            #index3=indexbase+j
            index3=index1+j

            if ex.TVFLUX[i][index3].values>0:

                #print(ex.TVFLUX[i][index1].values,ex.TVFLUX[i][index3].values)
                
                indexmin=index3

                break

            #else:
            #    indexmin=index1

        #for gomazon paper
        for j in range(0,80):

            index4=indexbase+j
            #index4=index1+j

            if (ex.QC[i][index4].values < lim_qc):

                indexmax=index4

                break

            #else:
            #    indexmax=indexbase


        pblh.append(ex.z[index1].values/1000.0)
        clfc.append(ex.z[indexmin].values/1000.0)
        cmflx.append(ex.MCUP[i,indexmin].values)
        cbase.append(ex.z[indexbase].values/1000.0)
        cbase2.append(ex.z[indexc].values/1000.0)
        ctop.append(ex.z[indexmax].values/1000.0)

    step=1

    #Limits of time date
    #idi2     = datetime(ex.datei.year,ex.datei.month,ex.datei.day,10)#dt.datetime(2014, days[2] ,days[0], 10)
    #idf2     = datetime(ex.datef.year,ex.datef.month,ex.datef.day,18)#dt.datetime(2014, days[2] ,days[0], 10)
    ##idf2     = ex.datef#dt.datetime(2014, days[3] ,days[0], 18)

    year=ex.time[0].dt.year.values
    month=ex.time[0].dt.month.values
    day=ex.time[0].dt.day.values


    date_format = '%Y-%m-%dT%H:%M'
    idi2=dt.datetime.strptime('%s-%s-%sT10:20'%(year,month,day), date_format)
    idf2=dt.datetime.strptime('%s-%s-%sT17:00'%(year,month,day), date_format)
    time1 = np.datetime64(idi2) 
    time2 = np.datetime64(idf2) 

    ni2,nf2= down.data_n(time1,time2,ex.time[:].values)

    # To find 13 and 14 hours
    #i13     = datetime(ex.datef.year,ex.datef.month,ex.datef.day,13)#dt.datetime(2014, days[2] ,days[0], 10)
    #i14     = datetime(ex.datef.year,ex.datef.month,ex.datef.day,14)#dt.datetime(2014, days[2] ,days[0], 10)
    i13=dt.datetime.strptime('%s-%s-%sT13:20'%(year,month,day), date_format)
    i14=dt.datetime.strptime('%s-%s-%sT14:00'%(year,month,day), date_format)
    i3 = np.datetime64(i13) 
    i4 = np.datetime64(i14) 

    n13,n14= down.data_n(i3,i4,ex.time[:].values)


    #TO find the cloud fraction max
    cbi    =np.argmax(cbase)
    cbmax   =cbase[cbi]
    cbmax14 =cbase[n14]

    #TO find the mass flux max
    mfi   =np.argmax(cmflx)
    mfx   =np.argmax(idxmmf)
    cb_mf =cbase[mfx]

    mfmax =cmflx[mfi]
    cbmf  =cbase[mfi]

    #Tree ways to calculate the max 
    #topmax=np.max(ctop)

    top_cb  =ctop[cbi]
    top_14  =ctop[n14]
    top_mc  =ctop[mfi]
    top_mf  =ctop[mfx]

    ###print(ex.time[mfi],'mfmax')
    ###print(ex.time[cbi],'cbmax')
    ####print(ex.date[n14],'14')


    ################
    print('######')
    print('CB base='   ,cbmax)
    print('CB base 14=',cbmax14)
    print('MF base='   ,cbmf)

    #############
    print('######')
    print('CB top='   ,top_cb)
    print('CB top 14=',top_14)
    print('MF top='   ,top_mf)

    #############
    print('######')
    print('CB    Deep=',top_cb-cbmax)
    print('CB 14 Deep=',top_14-cbmax14)
    print('MF Deep=',top_mf-cbmf)
    

    n = 4#nf2-ni2  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1


    cbasef = lfilter(b, a, cbase)

    #lfcbf  = lfilter(b, a, clfc)

    pblhf = lfilter(b, a, pblh)

    ctopf = lfilter(b, a, ctop)

    n = 10#nf2-ni2  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1

    lfcbf  = lfilter(b, a, clfc)


    ax.plot( ex.time[ni2:nf2:step]     , pblhf[ni2:nf2:step]  ,color=color[0]     ,linewidth=1.0,alpha=1.0,marker='')

    ax.plot( ex.time[ni2:nf2:step]     , cbasef[ni2:nf2:step] ,color=color[1] ,dashes=[1,0]  ,linewidth=1.0,alpha=1.0,marker='')

    #ax.plot( ex.time[ni2:nf2:step]     , lfcbf[ni2:nf2:step]  ,color='lime' ,  dashes=[1,0]  ,linewidth=1.0,alpha=1.0,marker='')

    ax.plot( ex.time[ni2:nf2:step]     , ctopf[ni2:nf2:step]  ,color=color[2] ,  dashes=[1,1]  ,linewidth=1.0,alpha=1.0,marker='')



    ytex,ytex2= down.data_n(time1,time2,ex.time[:].values)


    #pblh
    text1=r'$\mathrm{Z_i}$'
    idtex1    = idf2-timedelta(hours=0, minutes=0)
    ax.text(idtex1,pblhf[ytex2] -0.3 , r' %s'%(text1), fontsize=6, color=color[0])

    text2   =r'$\mathrm{h_{b}}$'
    #text2   =''#'$\mathrm{h_{b}}$'
    idtex2    = idf2-timedelta(hours=0, minutes=0)
    ax.text(idtex2, cbasef[ytex2]+0.0 , r' %s'%(text2), fontsize=7, color=color[1])

    text3='LFC'
    ##text1='NCL'
    #idtex3  = idf2-timedelta(hours=2, minutes=30)
    #ax.text(idtex3,cbase2[ytex2]+0.1 , r' %s'%(text3), fontsize=6, color='lime')

    text4=r'$\mathrm{h_{t}}$'
    #text3='$\mathrm{h_{topo}}$'
    idtex4    = idf2-timedelta(hours=0, minutes=00)
    ax.text(idtex4,ctopf[ytex2]+0.2 , r' %s'%(text4), fontsize=7, color=color[1])

    #if ex.name=='m_w_l' or  ex.name=='large':
    #    ax.text(idtex3,ctopf[ytex2]-0.4 , r' %s'%(text3), fontsize=7, color='black')
    #else :

    return fig,ax
