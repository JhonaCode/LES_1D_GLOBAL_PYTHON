######################## import  numpy as np

import  matplotlib.pyplot as plt

from    netCDF4         import num2date, date2num

#To work with date in plots 
import matplotlib.dates as mdates

#Color map
from   matplotlib.colors import LinearSegmentedColormap

import matplotlib as mpl

import sam_python.data_own as down

# To change the plot parameter 
from   sam_python.plotparameters 	import 	*
############################


# My color  map
#########
cmap0 = LinearSegmentedColormap.from_list('mycmap', ['skyblue','blue','navy','steelblue','lightskyblue','white'])
cmap  = LinearSegmentedColormap.from_list('mycmap', ['white','lightblue','skyblue','RoyalBlue','blue','darkblue'])

cmap2 = LinearSegmentedColormap.from_list('mycmap', ['white','red','OrangeRed','yellow','Lime','cyan','steelblue','blue'])

cmap3 = LinearSegmentedColormap.from_list('mycmap', ['white','blue','green','yellow'], N=256, gamma=1.0)
#########

def figure_sam_two_ax():

    #fig, ax1 = plt.subplots(fign)
    fig =   plt.figure()
    ###New axis
    ax1  =   plt.axes()

    color1 = 'tab:red'

    # instantiate a second axes that shares the same x-axis
    ax2 = ax1.twiny() 
    
    color2 = 'tab:blue'
    
    return fig,ax1,ax2,color1,color2 

def  splot_own(fig,ax,DATA,z,time,cor,label):


    #size of the data
    shapsam     =   DATA.shape

    data        =   np.zeros((shapsam[0],shapsam[1]))
        
    #rearrange the data, eliminit the ncformat
    for i in range(0,shapsam[0]):
    
        data[i,:] =DATA[i][:]

    #my own plot  
    fig,ax = shade_plot(fig,ax,data,z,time,cor,label)

    return fig,ax


def shade_plot(fig,ax,DATA,z,time,cor,label,**kw):

    #size of the data
    shapsam     =   DATA.shape

    data       =   np.zeros((shapsam[0],shapsam[1]))

    #rearrange the data, eliminit the ncformat
    for i in range(0,shapsam[0]):
    
        data[i,:] = DATA[i][:]

    am  = np.amax(data,axis=0)

    ax  = lplot(ax,data,z,cor,label)

    return fig,ax 

def lplot(ax,data,z,cor,label,**kw):

    ####################################
    est =   np.mean(data, axis=0)
    sd  =   np.std(data, axis=0)

    cis =   (est - sd/2.0, est + sd/2.0)
    #cis =   (est - sd, est + sd)
    #cis =   (est*0.90, est*1.10)

    ax.fill_betweenx(z,cis[0],cis[1],alpha=0.3,color=cor)# **kw)

    if label[1]:

        ax.plot(est,z,color=cor,label=label[0])
    else:
        ax.plot(est,z,color=cor)

    return ax

def  splot_own_ax(fig,ax,DATA,z,time,cor):

    #size of the data
    shapsam     =   DATA.shape

    data        =   np.zeros((shapsam[0],shapsam[1]))
        
    #rearrange the data, eliminit the ncformat
    for i in range(0,shapsam[0]):
    
        data[i,:] =DATA[i][:]

    fig,ax = shade_plot(fig,ax,DATA,z,time,cor,label,)

    
    return fig


def plot_temp(fign,data,time,color,axis,label):

    #used user parameter to plot(plotparameter.py
    mpl.rcparams.update(params)

    #new figure
    fig =   plt.figure(fign)
    ###new axis
    ax  =   plt.axes()

    #plot domain 
    plt.axis(axis)
    #plot label
    plt.xlabel(r"%s"%(label[0])) 
    plt.ylabel(r"%s"%(label[1])) 

    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 1.0, box.height])
    #ax.legend(loc='left', bbox_to_anchor=(1.0, 1.0),frameon=false)

    ax.legend(loc='left',frameon=false)
    #ax.grid(true)
    
    locatormax = mdates.hourlocator(interval=1)
    locatormin = mdates.minutelocator(interval=30)
    
    #locator.maxticks = 5 
    
    ax.xaxis.set_minor_locator(locatormin)
    ax.xaxis.set_major_locator(locatormax )
    
    majorformatter = mpl.dates.dateformatter('%h') #majorformatter = mpl.dates.dateformatter('%m-%d %h:%m:%s')
    ax.xaxis.set_major_formatter(majorformatter)

    #subplots
    #fig,ax = plt.subplots(fign)

    plot= plt.plot(time,data,color=color)
    

    return plot,fig 


def plot_mean(fign,data,time,cor,**kw):

    ######################################################
    fig =   plt.figure(fign)
    ###New axis
    ax  =   plt.axes()

    #With legends 
    ax.legend(frameon=False)

    ####################################
    est =   np.mean(data, axis=0)

    ax.plot(est,time,cor)


    return fig,ax

def plot_std(fign,data,time,cor,**kw):

    ######################################################
    fig =   plt.figure(fign)
    ###New axis
    ax  =   plt.axes()

    #With legends 
    ax.legend(frameon=False)

    ####################################
    est =   np.std(data, axis=0)

    ax.plot(est,time,cor)


    return fig,ax


def color_hours(hour):

    line=[1,0]
    color='k'

    if hour==9:

        line=[3,2,1,2]
        color='magenta'
        
    elif hour==10:
    
        line=[2,2,1,2]
        color='cyan'
    
    elif  hour==11:
    
    	line=[2, 1]
    	color='b'
    
    elif  hour==12:
    
        line=[3, 1]
        color='g'
    
    elif  hour==13:
    
        line=[4, 1]
        color='r'
    
    elif  hour==14:
    
        line=[1,1]
        color='tab:orange'
    
    elif  hour==15:
    
        line=[1,2,1,2]
        color='m'
    
    elif  hour==16:
    
        line=[2,1,1,3]
        color='tab:brown'
    
    elif  hour==17:
    
        line=[2,1,5,3]
        color='tab:purple'
    
    elif  hour==18:
    
        line=[4,2,1,2]
        color='y'
    
    elif  hour==19:

        line=[1,2,4,2]
        color='c'

    return line,color

