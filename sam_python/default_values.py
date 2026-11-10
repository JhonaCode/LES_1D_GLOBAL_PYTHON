import  numpy               as np

# Python standard library datetime  module
import  datetime as dt  
##################################

##################################
def default_values_sam_box(ex,vname,limx,limy,var_to,color,explabel1,explabel2,leg_loc,show,k,j): 


    #name    =   str(ex.name.values)#+'_'+dates[0]

    maxv=np.min(ex[vname].values)#.max
    minv=np.max(ex[vname].values)#.min

    minh=np.min(ex.time[:].values)
    maxh=np.max(ex.time[:].values)

    limx.append([minv,maxv,10])
    limy.append([minh,maxh])         

    var_to.append(1)

    color.append('coolwarm')

    exl1=0
    exl2=0

    if not explabel1:
        exl1=''
        #exl1=[]
    else: 
        exl1=explabel1[k][j]
        #if k==-1:
        #    exl1=explabel1[j]
        #else:
        #    exl1=explabel1[k][j]


    if not explabel2:
        exl2=[]
    else: 
        if k==-1:
            exl2=explabel2[j]
        else:
            exl2=explabel2[k][j]

    if not leg_loc:

        ll1=[(maxv-minv)/4.0+minv,maxh*0.90]
        #legent loc
        l1         = (ll1,ll1,['vertical',True,'[%s]'%ex[vname].units],['%s'%vname,True],['z',True],[False],[1,1])

    else:
        leg_loc=leg_loc[k][j]

    if not show:
        show='True'


    return limx[j],limy[j],var_to[j],color[j],exl1,exl2,leg_loc,show


##################################
def default_values_2d(exp,varst,lim,alt,var_to,color,explabel1,explabel2,axis_on,show,k): 

    el=len(exp) 
    vl=len(varst)

    ex=exp[k]

    name=ex.name


    a1          =  [(True,True,True ,True,0.35,1.34)]

    lim1=[]
    alt1=[]
    var_to1=[]
    label1=[]
    label2=[]
    color1=[]
    ax1=[]
    show1=[]


    for i in range(0, vl):

        var=varst[i]
        #Getting the Defaul values
        maxv=np.max(ex.nc_f[var])
        minv=np.min(ex.nc_f[var])

        minh=np.min(ex.z[:]/1000.0)
        maxh=np.max(ex.z[:]/1000.0)

        lim1.append([minv,maxv])
        alt1.append([minh,maxh])         

        var_to1.append(1)

        color1.append('RdBu_r')

        label1.append(var+'_'+ex.name)
        label2.append('')

        ####bar ,x,y axis, top_lfc_pbl,size,cm a mais do grafico
        ax1.append(a1)

        show1.append('True')

    lim.append(lim1)
    var_to.append(var_to1)
    color1.append(color1)
    explabel1.append(label1)
    explabel2.append(label2)
    axis_on.append(ax1)
    show.append(show1)

    return lim,alt,var_to,color,explabel1,explabel2,axis_on,show

#######################

def default_values_diff(exp,varst,lim,alt,var_to,color,explabel1,explabel2,axis_on,show): 

    el=1#len(exp) 
    vl=len(varst)

    ex=exp

    name=ex.name


    a1          =  [(True,True,True ,True,0.35,1.34)]

    lim1=[]
    alt1=[]
    var_to1=[]
    label1=[]
    label2=[]
    color1=[]
    ax1=[]
    show1=[]


    for i in range(0, vl):

        var=varst[i]
        #Getting the Defaul values
        maxv=np.max(ex.nc_f[var])
        minv=np.min(ex.nc_f[var])

        minh=np.min(ex.z[:]/1000.0)
        maxh=np.max(ex.z[:]/1000.0)

        lim1.append([minv,maxv])
        alt1.append([minh,maxh])         

        var_to1.append(1)

        color1.append('RdBu_r')

        label1.append(var+'_'+ex.name)
        label2.append('')

        ####bar ,x,y axis, top_lfc_pbl,size,cm a mais do grafico
        ax1.append(a1)

        show1.append('True')

    lim.append(lim1)
    var_to.append(var_to1)
    color1.append(color1)
    explabel1.append(label1)
    explabel2.append(label2)
    axis_on.append(ax1)
    show.append(show1)

    return lim,alt,var_to,color,explabel1,explabel2,axis_on,show

def default_plot(plot_def,k): 

    a1          =  [0.5,1,0.0]

    if not plot_def:
        plot_def=a1
    else:
        plot_def=plot_def[k]

    return plot_def 

def default_values_1d_new(ex,vname,lim,alt,var_to,color,explabel1,explabel2,plot_def,show,k,j): 

    name    =   str(ex.name.values)#+'_'+dates[0]
    maxv=np.nanmin(ex[vname].values)#.max
    minv=np.nanmax(ex[vname].values)#.min

    maxh=np.nanmin(ex.time.values)#.max
    minh=np.nanmax(ex.time.values)#.min

    interval_x=4
    interval_y=int(maxv/4)

    #maxt=np.max(0)
    #mint=np.min(len(ex.nc_f[var]))
    #lim1.append([mint,maxt,interval_x])
    #print(lim[j][0],maxh,minh)

    if not lim:
        lim=[minh,maxh,interval_x]
    else:
        lim=[lim[0],lim[1],lim[2]] 

    if not alt:
        alt=[minv,maxv,interval_y]        
    else:
        alt=alt[j]


    if not var_to:
        var_to=1
    else:
        var_to=var_to[j]

    if not color:
        color='red'
    else:
        color=color[k]

    if not explabel1:
        explabel1=''
    else:
        explabel1=explabel1[k]

    if not explabel2:
        explabel=[]
        local2=[]
    else:
        explabel2=explabel2[k]



    if not plot_def:
        X="Time"#.format(ex.time.units)
        Y="{} {}".format(vname,ex[vname].units)
        a1          =  [ [X,Y],[X,0,0],[False,'upper left'],[0.5,1,0.0]]
        plot_def=a1
    else:
        plot_def=plot_def[j]

    if not show:
        show=True
    else:
        show=show

    return lim,alt,var_to,color,explabel1,explabel2,plot_def,show

def default_values_1d(exp,varst,lim,alt,var_to,color,explabel1,explabel2,plot_def,show,k): 

    el=len(exp) 
    vl=len(varst)

    ex=exp[k]

    name=ex.name

    X=''
    Y=''

    a1          =  ( [X,Y],[X,0,0],[False,'upper left'],[0.35,0])

    lim1=[]
    alt1=[]
    var_to1=[]
    label1=[]
    label2=[]
    color1=[]
    ax1=[]
    show1=[]


    interval_x=4


    for i in range(0, vl):

        var=varst[i]

        #Getting the Defaul values
        maxv=np.max(ex.nc_f[var])
        minv=np.min(ex.nc_f[var])

        interval_y=int(maxv/4)

        maxt=np.max(0)
        mint=np.min(len(ex.nc_f[var]))

        lim1.append([mint,maxt,interval_x])
        alt1.append([minv,maxv,interval_y])         


        var_to1.append([1])

        color1.append('blue')

        label1.append(var+'_'+ex.name)
        label2.append([''])

        ####bar ,x,y axis, top_lfc_pbl,size,cm a mais do grafico
        ax1.append([a1])

        show1.append('True')

    lim.append(lim1)
    alt.append(alt1)
    var_to.append(var_to1)
    color1.append(color1)
    explabel1.append(label1)
    explabel2.append(label2)
    plot_def.append(ax1)
    show.append(show1)

    return lim,alt,var_to,color,explabel1,explabel2,plot_def,show
        #return lim1,alt1,var_to1,color,label1,label2,ax1,show1

def default_temporal_mpas(ex,var,vname,hours,lim,var_to,color,explabel1,explabel2,leg_loc,diurnal,show): 

    name=ex.name.values

    maxv=np.min(var[vname].values)#.max
    minv=np.max(var[vname].values)#.min

    maxh=hours[0]
    minh=hours[len(hours)-1]

    lim.append([minh,maxh,minv,maxv])

    var_to.append(1)

    color.append('Red')

    explabel1.append('')
    explabel2.append('')
    #legent loc
    l1         = (['upper right',False],['%s'%vname,True],['hours',True],[1,1])

    leg_loc.append(l1)

    show.append('True')


    return lim,var_to,color,explabel1,explabel2,leg_loc,show

##################################
def default_values_sam_2d_kj(ex,vname,z,lim,alt,var_to,color,explabel1,explabel2,leg_loc,show,k,j): 


    name    =   str(ex.name.values)#+'_'+dates[0]

    maxv=np.min(ex[vname].values)#.max
    minv=np.max(ex[vname].values)#.min


    minh=np.min(z[:]/1000.0)
    maxh=np.max(z[:]/1000.0)

    lim.append([minv,maxv,10])
    alt.append([minh,maxh])         

    var_to.append(1)

    color.append('BuRd_r')

    exl1=0
    exl2=0

    if not explabel1:
        exl1=''
        #exl1=[]
    else: 
        exl1=explabel1[k][j]
        #if k==-1:
        #    exl1=explabel1[j]
        #else:
        #    exl1=explabel1[k][j]


    if not explabel2:
        exl2=[]
    else: 
        if k==-1:
            exl2=explabel2[j]
        else:
            exl2=explabel2[k][j]

    if not leg_loc:

        ll1=[(maxv-minv)/4.0+minv,maxh*0.90]
        #legent loc
        l1         = (ll1,ll1,['vertical',True,'[%s]'%ex[vname].units],['%s'%vname,True],['z',True],[False],[1,1])

    else:
        leg_loc=leg_loc[k][j]

    if not show:
        show='True'

    #print(show)
    #exit()

    return lim,alt,var_to,color,exl1,exl2,leg_loc,show


##################################
def default_values_sam_2d(ex,vname,z,lim,alt,var_to,color,explabel1,explabel2,leg_loc,show): 

    name    =   str(ex.name.values)#+'_'+dates[0]

    maxv=np.min(ex[vname].values)#.max
    minv=np.max(ex[vname].values)#.min


    minh=np.min(z[:]/1000.0)
    maxh=np.max(z[:]/1000.0)

    lim.append([minv,maxv,10])
    alt.append([minh,maxh])         

    var_to.append(1)

    color.append('BuRd_r')

    if not explabel1:
        explabel1.append(['',''])
    if not explabel2:
        explabel2.append(['',''])

    ll1=[(maxv-minv)/4.0+minv,maxh*0.90]
    #legent loc
    l1         = (ll1,ll1,['vertical',True,'[%s]'%ex[vname].units],['%s'%vname,True],['z',True],[1,1])

    leg_loc.append(l1)

    show.append('True')

    return lim,alt,var_to,color,explabel1,explabel2,leg_loc,show


##################################
def default_values_sam_diurnal(ex,vname,z,lim,alt,var_to,color,explabel1,explabel2,leg_loc,diurnal,show,k,j,line=[]): 

    name    =   str(ex.name.values)#+'_'+dates[0]

    maxv=np.min(ex[vname].values)#.max
    minv=np.max(ex[vname].values)#.min

    if not lim:
       lim=[minv,maxv]
    else:
        lim=lim[j]
        
    minh=np.min(z[:]/1000.0)
    maxh=np.max(z[:]/1000.0)


    if not alt:
        alt=[minh,maxh]        
    else:
        alt=alt[j]

    if not var_to:
        var_to=1
    else:
        var_to=var_to[j]

    if not color:
        color='Red'
    else:
        #if k==-1:
        color=color[j]

    if not line:
        line=[1,0]
    else:
        line=line[j]

    if not explabel1:
        explabel1=''
    else:
        if k==-1:
            explabel1=explabel1[j]
        else:
            explabel1=explabel1[k][j]


    if not explabel2:
        explabel=[]
        local2=[]
    else:
        if k==-1:
            explabel2=explabel2[j]
        else:
            explabel2=explabel2[k][j]

    if not leg_loc:
        ll1=[(maxv-minv)/4.0+minv,maxh*0.8]
        #legent loc
        l1         = (ll1,local2,['upper right',False],['%s'%vname,True],['z',True],[1,1,0])

        leg_loc=l1
    else:
        if k==-1:
            leg_loc=leg_loc[j]
        else:
            leg_loc=leg_loc[k][j]



    if not diurnal:
        diurnal=[1,'True',[]]
    else:
        diurnal=diurnal[j]

    if not show:
        show=True
    else:
        show=show

    return lim,alt,var_to,color,explabel1,explabel2,leg_loc,diurnal,show,line

def default_plot_diurnal(leg_loc,j): 

    if not leg_loc:
        l1         = [1,1,0]
        leg_loc=l1
    else:
        leg_loc=leg_loc[j][5]


    return leg_loc

##################################
def default_values_mpas(ex,var,vname,z,lim,alt,var_to,color,explabel1,explabel2,leg_loc,diurnal,show): 

    name=ex.name.values

    maxv=np.min(var[vname].values)#.max
    minv=np.max(var[vname].values)#.min

    minh=np.min(z[:]/1000.0)
    maxh=np.max(z[:]/1000.0)

    lim.append([minv,maxv])
    alt.append([minh,maxh])         

    var_to.append(1)

    color.append('Red')

    explabel1.append('')
    explabel2.append('')

    ll1=[(maxv-minv)/4.0+minv,maxh*0.90]
    #legent loc
    l1         = (ll1,ll1,['upper right',False],['%s'%vname,True],['z',True],[1,1])

    leg_loc.append(l1)

    diurnal.append('True')

    show.append('True')


    return lim,alt,var_to,color,explabel1,explabel2,leg_loc,diurnal,show

def default_values_horizontal(ex,var,lim,xlim,ylim,var_to,color,explabel1,explabel2,axis_on,leg_loc,show): 

    #Getting the Defaul values
    maxv=np.max(var)
    minv=np.min(var)

    minx=np.min(ex.x[:])/1000.0
    maxx=np.max(ex.x[:])/1000.0
                               
    miny=np.min(ex.y[:])/1000.0
    maxy=np.max(ex.y[:])/1000.0

    name=ex.name


    try:
        units=var.units
    except AttributeError:
        units ='' 

    lim.append([[minv,maxv,20,'%s'%units]])
    xlim.append([[minx,maxx,10]])         
    ylim.append([[miny,maxy,10]])         

    var_to.append([1])

    color.append('RdBu_r')

    explabel1.append([name])
    explabel2.append([''])

    ####bar ,x,y axis, top_lfc_pbl,size,cm a mais do grafico
    a1          =  [(True,True,True,0.35,1.34)]
    axis_on.append([a1])

    dx=(ex.x[1]-ex.x[0])/1000.0
    dy=(ex.y[1]-ex.y[0])/1000.0

    l1  =[True,minx+100*dx,maxy-100*dy]
    leg_loc.append([l1])


    show.append(['True'])

    return lim,xlim,ylim,var_to,color,explabel1,explabel2,axis_on,leg_loc,show
