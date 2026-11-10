import matplotlib as mpl

# \showthe\columnwidth overleaf!
#columnwidth = 397.495# value given by Latex


def plotsize(para_name,wf=1,hf=1,cmmais=0): 

    columnwidth = 397.495 #value given by Latex

    figsize     = get_figsize(columnwidth, wf=wf, hf=hf, cmmais=cmmais)

    params =parameters(para_name,figsize)

    mpl.rcParams.update(params)

    return params


def get_figsize(columnwidth, wf=0.5, hf=(5.**0.5-1.0)/2.0, cmmais=0.0):

      """Parameters:
        - wf [float]:  width fraction in columnwidth units
        - hf [float]:  height fraction in columnwidth units.
                       Set by default to golden ratio.
        - columnwidth [float]: width of the column in latex. Get this from LaTeX
                               using \showthe\columnwidth
      Returns:  [fig_width,fig_height]: that should be given to matplotlib

      """

      fig_width_pt  = columnwidth*wf
      #1pt=0.3515
      inches_per_pt = 1.0/72.27               # Convert pt to inch
      fig_width     = fig_width_pt*inches_per_pt  # width in inches
      fig_height    = fig_width*hf           # height in inches

      if cmmais>0.0:

        hfcm= wf*hf*(397.495*(1/72.27)*(2.54))
        #2cm a mais para colocar a barra e a figura ficar do mesmo tamano 
        lcm=cmmais/(397.495*(1/72.27)*(2.54))

        wf = wf+lcm 

        hf = hfcm/((397.495*(1/72.27)*(2.54))*wf)

        fig_width_pt  = columnwidth*wf

        #1pt=0.3515
        inches_per_pt = 1.0/72.27               # Convert pt to inch
        fig_width     = fig_width_pt*inches_per_pt  # width in inches
        fig_height    = fig_width*hf           # height in inches


      #print('Fig size in',fig_width,fig_height)
      #print('Fig size mm',fig_width*2.54*2.0,fig_height*2.54*2.0,wf,hf)

      return [fig_width, fig_height]

def parameters(name,figsize):

    if name=='diurnal':
    
        parame = {
              'figure.figsize'  : figsize,
              'font.family'     : 'serif',
              'font.sans-serif' : 'Helvetica',
              'font.size'       : 8,
              'font.weight'     : '400',
              'lines.linewidth' : 1,
              'legend.fontsize' : 'small',
              'axes.labelsize'  : 'small',
              'axes.labelweight': '300',
              'xtick.labelsize' : 'small',
              'ytick.labelsize' : 'small',
              'xtick.direction' : 'out',   
        }

    if name=='diurnal2':
    
        parame = {
              'figure.figsize'  : figsize,
              'font.family'     : 'serif',
              'font.sans-serif' : 'Helvetica',
              'font.size'       : 8,
              'font.weight'     : '400',
              'lines.linewidth' : 1,
              'legend.fontsize' : 7.0,
              'axes.labelsize'  : 'small',
              'axes.labelweight': '300',
              'xtick.labelsize' : 'small',
              'ytick.labelsize' : 'small',
              'xtick.direction' : 'out',   
        }

    if name=='2d':

        parame = {
              'figure.figsize'   : figsize,
              'font.family'      : 'serif',
              'font.sans-serif'  : 'Helvetica',
              'font.size'        : 6,
              'font.weight'      : '500',
              'lines.linewidth'  :  2,
              'legend.fontsize'  : 'medium',
              'axes.labelsize'   : 'medium',
              'axes.labelweight' : '500',
              'xtick.labelsize'  : 'medium',
              'ytick.labelsize'  : 'medium',
              'xtick.direction'  : 'out', 
                    }
    
    if name=='temporal':

        parame= {
             	  'figure.figsize':figsize,
            	  'font.family' : 'serif',
            	  'font.sans-serif'    : 'Helvetica',
                  'font.size' : 8,
            	  'font.weight' : '400',
            	  'lines.linewidth':1.0,
             	  'legend.fontsize': 'small',
             	  'axes.labelsize' : 'small',
             	  'axes.labelweight' :'400',
             	  'xtick.labelsize': 'x-small',
             	  'ytick.labelsize': 'small',
                  'xtick.direction': 'out',   
        }

    if name=='mapa1':

        parame= {
             	  'figure.figsize'  : figsize,
            	  'font.family'     : 'serif',
            	  'font.sans-serif' : 'Helvetica',
                  'font.size'       : 7,
            	  'font.weight'     : '200',
            	  'lines.linewidth' :  1.0,
             	  'legend.fontsize' : 'small',
             	  'axes.labelsize'  : 'x-small',
             	  'axes.labelweight': '200',
             	  'xtick.labelsize' : 'small',
             	  'ytick.labelsize' : 'small',
                  'xtick.direction' : 'out',   
        }

    if name=='mapa2':

        parame= {
             	  'figure.figsize'  : figsize,
            	  'font.family'     : 'serif',
            	  'font.sans-serif' : 'Helvetica',
                  'font.size'       : 9,
            	  'font.weight'     : '300',
            	  'lines.linewidth' :  1.2,
             	  'legend.fontsize' : 'small',
             	  'axes.labelsize'  : 'small',
             	  'axes.labelweight': '300',
             	  'xtick.labelsize' : 'small',
             	  'ytick.labelsize' : 'small',
                  'xtick.direction' : 'out',   
        }

    return parame
