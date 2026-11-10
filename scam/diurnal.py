#Python standard library datetime  module

import  numpy               as np

import  datetime            as dt

import  cftime              #as cf

import  matplotlib.pyplot   as plt

import  matplotlib          as mpl

from    matplotlib.ticker   import MultipleLocator,AutoMinorLocator, FormatStrFormatter


import importlib

import subprocess, sys

import xarray as xr

import  scam.data_own            as down

import  scam.figure_own_xr       as fown

import  scam.campain_data        as cd

import  scam.plotparameters      as pp

import  scam.forcing_file_common as ffc

import  scam.default_values as df

#to cp the parametres defaul 
subprocess.run('cp Parameters_default.py /pesq/dados/bamc/jhonatan.aguirre/git_repositories/MAPS_python/scam/', shell = True, executable="/bin/bash")

#used the user parameter to plot(plotparameter.py) if para:
#pars=__import__('source.Parameters_default',globals())
pars=importlib.import_module('.Parameters_default','scam',)


def label_plots(ax,legend,explabel1,explabel2,tama): 

#leg_loc      =  ( [ 0.5,4.2],[ 0.5,4.2],'center right',[xlabel,'True'],[ylabel,'True'],[size_wg,size_hf])

    xlabel=legend[3][0]

    ylabel=legend[4][0]

    ax.text(legend[0][0], legend[0][1], r' %s'%(explabel1), fontsize=tama, color='black')


    if  legend[1]:

        ax.text(legend[1][0], legend[1][1], r' %s'%(explabel2), fontsize=tama, color='black')

    #plt.grid(color = 'gray', linestyle = '--', linewidth = 0.25)
    plt.grid(color = 'gray',axis='y',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0])
    plt.grid(color = 'gray',axis='x',linewidth=0.5,alpha=0.5,dashes=[1,1,0,0])

    if( legend[3][1]==True):
        plt.xlabel(r'%s'%(xlabel)) 

    if( legend[4][1]==True):
        plt.ylabel(r'%s'%(ylabel)) 

    if( legend[2][1]==True):
    	plt.legend(frameon=False,loc=legend[2][0])


    return ax

def diurnal_tke_budget_xr(exp,hour,date,name=[],explabel1=[],explabel2=[],alt=[],lim=[],var_to=[],color=[],leg_loc=[],diurnal=[],show=[]): 

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
        #ni,nf=down.data_n(datei,datef,ex.time.values) 

        tovar= ex.sel(time=slice(ex.time[ni],ex.time[nf]))

        #if name:
        name    =   str(ex.name.values)#+'_'+dates[0]

        print("_les__%s__"%(name))

        #Its no necessary to calculate de height
        z=ex.z.values

        limu,altu,var_tou,coloru,explabel1u,explabel2u,leg_locu,diurnalu,showu,lineu=df.default_values_sam_diurnal(ex,'BUOYA',z,lim,alt,var_to,color,explabel1,explabel2,leg_loc,diurnal,show,-1,k)

        #data1 = tovar[var][:,:]*var_tou
        data2 = tovar['SHEAR'][:]*var_tou   #+ex.SHEARS[:]
        data3 = tovar['BUOYA'][:]*var_tou   #+ex.BUOYAS[:]
        data4 = tovar['ADVTR'][:]*var_tou   #+ex.ADVTRS[:]
        data5 = tovar['PRESSTR'][:]*var_tou
        data6 = tovar['DISSIP'][:]*var_tou  #+ex.DISSIPS[:]

        size_wg = leg_locu[5][0]
        size_hf = leg_locu[5][1]
        tama=pp.plotsize(size_wg,size_hf, 0.0,'diurnal')

        #To plot 
        fig  = plt.figure()
        ax   = plt.axes()

        figs,ax = main_plot_hour(fig,ax,data3,hour,z,altu,['orange' ,[1,0]]        , 'B' )
        figs,ax = main_plot_hour(fig,ax,data5,hour,z,altu,['green',[2,1] ], 'P' )
        figs,ax = main_plot_hour(fig,ax,data4,hour,z,altu,['purple',[1,0]      ]  , 'T' )
        figs,ax = main_plot_hour(fig,ax,data6,hour,z,altu,['blue',[2,1]     ]  , 'D' )
        figs,ax = main_plot_hour(fig,ax,data2,hour,z,altu,['black',[1,0]]        , 'S' )

        plt.axis([limu[0],limu[1],altu[0],altu[1]])

        #plt.ticklabel_format(axis='x',style='sci',scilimits=(0,0),useMathText=True)

        
        #locatormax = interval=10)
        #locatormin = interval=1)
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.xaxis.set_major_locator(MultipleLocator(limu[2]))


        ax=label_plots(ax,leg_locu,explabel1u,explabel2u,tama-1)

        label="%s_%s"%(name,hour)

        plt.savefig('%s/tke_buget_%sh.pdf'%(pars.out_fig,label),bbox_inches='tight',dpi=200, format='pdf')

        k+=1

    if show:

        plt.show()

    plt.close('all')

    return 


def diurnal_var_sam_xr(exp,variables,date,name=[],explabel1=[],explabel2=[],explabel3=[],alt=[],lim=[],var_to=[],color=[],line=[],leg_loc=[],diurnal=[],show=[]): 

    j=0
    for var in variables:
    
        print("___________________")
        print("%s"%(var))
        print("___________________")


        plot_defu=df.default_plot_diurnal(leg_loc,j)

        size_wg = plot_defu[0]
        size_hf = plot_defu[1]
        cmm     = plot_defu[2]

        tama=pp.plotsize(size_wg,size_hf,cmm,'diurnal')

        #To plot 
        fig  = plt.figure()
        ax   = plt.axes()


        lim,altu,var_tou,coloru,explabel1u,explabel3u,leg_locu,diurnalu,showu,lineu=df.default_values_sam_diurnal(exp[0],var,exp[0].z,lim,alt,var_to,color,explabel1,explabel3,leg_loc,diurnal,show,-1,j,line)


        name='%s_hr_%s'%(diurnal[j][2][0],var)

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
            #ni,nf=down.data_n(datei,datef,ex.time.values) 

            tovar= ex.sel(time=slice(ex.time[ni],ex.time[nf]))

            #print(tovar.time[0].values,ni,nf)

            #if name:
            name    =   name+'_'+str(ex.name.values)#+'_'+dates[0]

            #Its no necessary to calculate de height
            z=ex.z.values

            data=tovar[var][:,:]*var_tou

            hours=[datei,datef]

            
            #lines per hour
            ch=diurnalu[0]

            try:
                #hour to plot
                htp=diurnalu[2]
            except:
                htp=[]

            fig,ax = main_plot_var(fig,ax,data,ch,htp,hours,z,altu,limu,coloru[k],lineu[k],name,explabel2[k],leg_locu,diurnalu[1])

            k+=1

        ax=label_plots(ax,leg_locu,explabel1u,explabel3u,tama)

        plt.savefig('%s/diurnal_%s.pdf'%(pars.out_fig,name),bbox_inches='tight',dpi=200, format='pdf')


        plt.show()

        j+=1

    if show:

        plt.show()

    plt.close('all')

    return 

def diurnal_hours_exps_sam(exp,variables,date,name=[],explabel1=[],explabel2=[],alt=[],lim=[],var_to=[],color=[],leg_loc=[],diurnal=[],show=[],plotpara=None): 
    
    #plotparameters
    if plotpara==None:
        plotpara=[]

    k=0
    for ex in exp:

        print("___________________")
        print("__%s__"%(ex.name))
        print("___________________")

        #date_format = '%Y%m%d%H%M%S'
        date_format = '%Y-%m-%dT%H:%M'
        datei=dt.datetime.strptime(date[k][0], date_format)
        datef=dt.datetime.strptime(date[k][1], date_format)

        time1 = cftime.DatetimeNoLeap(

        datei.year, datei.month, datei.day, datei.hour
        )

        time2 = cftime.DatetimeNoLeap(
            datef.year, datef.month, datef.day, datef.hour
        )


        ni,nf=down.data_n(time1,time2,ex.time.values) 
        #ni,nf=down.data_n(datei,datef,ex.time.values) 

        tovar= ex.sel(time=slice(ex.time[ni],ex.time[nf]))

        #if name:
        name    =   str(ex.name.values)#+'_'+dates[0]

        print("_scam__%s__"%(name))

        j=0
        for var in variables:

        
            print("___________________")
            print("%s"%(var))
            print("___________________")

            #Its no necessary to calculate de height
            z=ex.z.values

            limu,altu,var_tou,coloru,explabel1u,explabel2u,leg_locu,diurnalu,showu,lineu=df.default_values_sam_diurnal(ex,var,z,lim,alt,var_to,color,explabel1,explabel2,leg_loc,diurnal,show,k,j)

            data=tovar[var][:,:]*var_tou

            hours=[datei,datef]

            name2='scam_'+name+'_'+var
            
            #lines per hour
            ch=diurnalu[0]


            try:
                #hour to plot
                htp=diurnalu[2]
            except:
                htp=[]

            figs,axis = main_plot_diurnal_new(data,ch,htp,hours,z,altu,limu,coloru,name2,[explabel1u,explabel2u],leg_locu,diurnalu[1],plotpara)

            j+=1

        k+=1

    if show:

        plt.show()

    plt.close('all')

    return 


def main_plot_hour(fig,ax,data,hour,z,alt,color,explabel):

    #mean diurnal function 
    meanvar,time_h = diurnal_main(data,z,hour,hour,ch=1)

    plt.plot(meanvar[0,:] ,z[:]/1000.0,label='%s'%(explabel),color=color[0],linewidth=1.5,alpha=1.0,dashes=color[1])
    #plt.plot(meanvar[0,:] ,z[:]/1000.0,color=color,linewidth=1.0,alpha=1.0,dashes=[1,0])



    return fig,ax

def main_plot_var(fig,ax,data,ch,hours,date,z,alt,lim,color,line,name,explabel,leg_loc,diurnal):

    hi=date[0].hour
    hf=date[1].hour

    #ni,nf= down.data_n(ex.datei_diurnal,ex.datef_diurnal,ex.date[:])
    ##interval hour
    ch      = ch

    #mean diurnal function 
    meanvar,hour = diurnal_main(data,z,hi,hf,ch=1)

    jj=0

    if diurnal:
         
        if hours:

            for j in range(0,len(hour)):                                
                
                for jj in range(0,len(hours)):                          
                    
                    if hour[j]==hours[jj]:
            
                        plt.plot(meanvar[j,:] ,z[:]/1000.0,label=r'%s'%(explabel),color=color,linewidth=1.5,alpha=1.0,dashes=line)

        else:
                
            j=0
            for h in range(0,hf-hi,ch):
            
                plt.plot(meanvar[j,:] ,z[:]/1000.0,label=r'%s'%(explabel),color=color,linewidth=1.5,alpha=1.0,dashes=line)
                j+=1

    if lim:

        #plt.axis([lim[0],lim[1],alt[0],alt[1]])
        ax.set_xlim(lim[0],lim[1])
        ax.xaxis.set_major_locator(MultipleLocator(lim[2]))

    ax.set_ylim(alt[0],alt[1])
    #def label_plots(ax,legend,explabel,xlabel): 
    ax.xaxis.set_minor_locator(AutoMinorLocator(3))


    return fig,ax

def main_plot_diurnal_new(data,ch,hours,date,z,alt,lim,color,name,explabel,leg_loc,diurnal,plotpara):

    hi=date[0].hour
    hf=date[1].hour

    #ni,nf= down.data_n(ex.datei_diurnal,ex.datef_diurnal,ex.date[:])
    ##interval hour
    ch      = ch

    #mean diurnal function 
    meanvar,hour = diurnal_main(data,z,hi,hf,ch=1)

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
        tama,figsize=pp.plotsize(size_wg,size_hf,cm_plus,'diurnal')


    #To plot 
    fig  = plt.figure()
    ax   = plt.axes()


    jj=0


    if diurnal:
         
        if hours:

            for j in range(0,len(hour)):                                
                
                for jj in range(0,len(hours)):                          
                    
                    if hour[j]==hours[jj]:
            
                        line,col =color_hours(hour[j])
                        #plt.plot(meanvar[j,::-1] ,z[j,:]/1000.0,label='%d'%(hour[j]),color=col,linewidth=1.0,alpha=1.0,dashes=line)
                        plt.plot(meanvar[j,::-1] ,z[:]/1000.0,label='%d'%(hour[j]),color=col,linewidth=1.0,alpha=1.0,dashes=line)

        else:
                
            j=0
            for h in range(0,hf-hi,ch):
            
                line,col =color_hours(hour[h])
                #plt.plot(meanvar[h,::-1] ,z[j,:]/1000.0,label='%d'%(hour[h]),color=col,linewidth=1.0,alpha=1.0,dashes=line)
                plt.plot(meanvar[h,::-1] ,z[:]/1000.0,label='%d'%(hour[h]),color=col,linewidth=1.0,alpha=1.0,dashes=line)
                j+=1
            
    #if( name=='buoyancyflux'):

    #    ax.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    #    ax.xaxis.get_offset_text().set_visible(False)

    #elif( name=='relh' or name=='cld' or name=='qtflux'or name=='thetalflux'):
    #    xFormatter = FormatStrFormatter('%.f')
    #    ax.xaxis.set_major_formatter(xFormatter)

    label=['mean',False]

    #z_mean=np.mean(z,axis=0)
    #fn,ax=shade_plot(fig,ax,data[:,::-1].values,z_mean/1000.0,color,label)

    fn,ax=shade_plot(fig,ax,data[:,::-1].values,z/1000.0,color,label)

    ax=label_plots(ax,leg_loc,explabel[0],explabel[1],tama)


    if lim:

        #plt.axis([lim[0],lim[1],alt[0],alt[1]])
        ax.set_xlim(lim[0],lim[1])
        ax.xaxis.set_major_locator(MultipleLocator(lim[2]))

    ax.set_ylim(alt[0],alt[1])
    #def label_plots(ax,legend,explabel,xlabel): 
    ax.xaxis.set_minor_locator(AutoMinorLocator(3))

    label="%s"%(name)

    plt.savefig('%s/diurnal_%s.pdf'%(pars.out_fig,label),bbox_inches='tight',dpi=200, format='pdf')

    return fig,ax

#todo
#colocar num unico lugar esta funcao
def shade_plot(fig,ax,data,z,cor,label):

    ####################################
    est =  np.mean(data, axis=0)
    sd  =   np.std(data, axis=0)

    cis =   (est[:] - sd[:]/2.0, est[:] + sd[:]/2.0)

    #cis =   (est - sd, est + sd)
    #cis =   (est*0.90, est*1.10)

    ax.fill_betweenx(z,cis[0],cis[1],alpha=0.2,color=cor)# **kw)


    if label[1]:
        ax.plot(est[:],z,color=cor,label=label[0])
    else:
        ax.plot(est[:],z,color=cor)

    return fig,ax


def diurnal_main(var,z,hi,hf,ch): 


    #number of levels
    nl      = z.shape[0]
    #as z depends on time, the 0 dimension is time.
    #nl      = z.shape[1]

    #Lengh of the time array to search
    ndtp        =   len(var.time) 

    nh=int(hf+1-hi+ch)

    #Hour array
    #+ch to reach the final hour in the loop
    hour    = np.zeros(nh)

    #Sum variable to the mean 
    varsum  = np.zeros([nh,nl])

    meanvar = np.zeros([nh,nl])

    #var     = np.zeros([nl])
    meanvar = np.zeros([nh,nl])

    #Number of  time thar variable was sum 
    cont    = np.zeros(nh)
    
    for i in range(0,ndtp):
    
        for j in range(0,nh,ch):

            if int(var[i].time.dt.hour)==j+hi: 

                hour[j]     =   j+hi

                varsum[j,:] =   varsum[j,:]+var[i,:]

                cont[j]     =   cont[j]+1


    for j in range(0,nh-ch,ch):
        
        meanvar[j,:] = varsum[j,:]/cont[j]


    return meanvar,hour

def color_exp(hour):
    line=[1,0]
    color='k'

    if hour==0:
          #line=[3,2,1,2]
          line=[1,0]
          color='darkcyan'

    elif  hour==1:

          line=[2,2,1,2]
          color='blue'

    elif  hour==2:
          #line=[2, 1]
          line=[1,0]
          color='cyan'

    elif  hour==3:

          line=[3, 1]
          color='green'

    elif  hour==4:

          color='r'

    elif  hour==5:

          color='tab:orange'

    elif  hour==6:

          line=[1,2,1,2]
          color='tab:brown'

    elif  hour==7:

          line=[2,1,1,3]
          color='m'

    elif  hour==8:

          line=[2,1,5,3]
          color='tab:purple'

    elif  hour==9:

          #line=[4,2,1,2]
          line=[1,0]
          color='y'

    elif  hour==10:

          line=[1,2,4,2]
          color='peru'
    
    return line,color

def color_hours(hour):
    line=[1,0]
    color='k'

    if hour==7:
          line=[3,2,1,2]
          color='darkcyan'

    elif  hour==8:

          line=[2,2,1,2]
          color='green'

    elif  hour==9:

          line=[1,0]
          color='blue'

    elif  hour==10:

          #line=[3, 1]
          line=[1,0]
          color='cyan'

    elif  hour==11:

          line=[2, 1]
          #line=[1,2,1,2]
          color='tab:purple'

    elif  hour==12:

          color='tab:brown'

    elif  hour==13:

          line=[1,0]
          color='r'

    elif  hour==14:

          line=[1,0]
          color='tab:orange'

    elif  hour==15:

          line=[2,1,1,1]
          color='limegreen'

    elif  hour==16:

          line=[1,0]
          color='m'

    elif  hour==17:

          #line=[1,2,4,2]
          line=[1,0]
          color='darkblue'
    
    return line,color

def color_hours_2(hour):
    line=[1,0]
    color='k'

    if hour==9:
          #line=[3,2,1,2]
          line=[1,0]
          color='darkcyan'

    elif  hour==10:

          line=[2,2,1,2]
          color='blue'

    elif  hour==11:
          #line=[2, 1]
          line=[1,0]
          color='cyan'

    elif  hour==12:

          #line=[3, 1]
          line=[3, 1]
          color='green'

    elif  hour==13:

          color='r'

    elif  hour==14:

          color='tab:orange'

    elif  hour==15:

          line=[1,2,1,2]
          color='tab:brown'

    elif  hour==16:

          line=[2,1,1,3]
          color='m'

    elif  hour==17:

          line=[2,1,5,3]
          color='tab:purple'

    elif  hour==18:

          #line=[4,2,1,2]
          line=[1,0]
          color='y'

    elif  hour==19:

          line=[1,2,4,2]
          color='peru'
    
    return line,color

def get_figsize(columnwidth, wf=0.24, hf=(5.**0.5-1.0)/2.0, ):

      """
        Parameters:
        - wf [float]:  width fraction in columnwidth units
        - hf [float]:  height fraction in columnwidth units.
                       Set by default to golden ratio.
        - columnwidth [float]: width of the column in latex. Get this from LaTeX
                            using show the columnwidth
      Returns:  [fig_width,fig_height]: that should be given to matplotlib
      """
      fig_width_pt = columnwidth*wf
      inches_per_pt = 1.0/72.27               # Convert pt to inch
      fig_width = fig_width_pt*inches_per_pt  # width in inches
      fig_height = fig_width*hf      # height in inches
      return [fig_width, fig_height]
