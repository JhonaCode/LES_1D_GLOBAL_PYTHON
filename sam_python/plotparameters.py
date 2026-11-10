##https://matplotlib.org/stable/users/explain/customizing.html

import matplotlib as mpl

# \showthe\columnwidth overleaf!
#columnwidth = 397.495# value given by Latex

def plotsize(wf,hf,cmmais,para_name): 

    columnwidth = 397.495 #value given by Latex

    figsize     = get_figsize(columnwidth, wf=wf, hf=hf, cmmais=cmmais)

    params,tama =parameters(para_name,figsize)


    mpl.rcParams.update(params)

    return tama 


def get_figsize(columnwidth, wf=0.5, hf=(5.**0.5-1.0)/2.0, cmmais=0.0):

      r"""Parameters:
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

        tama=8
        #tama=6
    
        parame = {
              'mathtext.fontset': 'cm',
              'figure.figsize'   : figsize,
              'font.family'     : 'serif',
              'font.sans-serif' : 'Helvetica',
              'font.weight'     :   tama,
              'font.size'        :  tama,
              'lines.linewidth'  :  1.5,
              #'legend.fontsize'  :  tama-3,
              'legend.fontsize'  :  tama-1,
              'axes.labelsize'   :  tama,
              'axes.labelweight' :  tama,
              #size of the numbers
              'xtick.labelsize'  :  tama,
              'ytick.labelsize'  :  tama,
              'xtick.direction' : 'out',   
        }

    if name=='diurnal2':

        tama=9
    
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

        tama=8

        parame = {
              'mathtext.fontset': 'cm',
              'figure.figsize'   : figsize,
              'font.family'      : 'serif',
              'font.sans-serif'  : 'Helvetica',
              'font.weight'      :  11,
              #labelof cbbar
              'font.size'        :  tama,
              'lines.linewidth'  :  2,
              'legend.fontsize'  :  tama,
              'axes.labelsize'   :  11,
              'axes.labelweight' :  11,
              #size of the numbers
              'xtick.labelsize'  :  tama,
              'ytick.labelsize'  :  tama,
              'xtick.major.width':   0.5, # major tick width in points
              'xtick.minor.width':   0.05, # major tick width in points
              'ytick.major.width':   0.1, # major tick width in points
              'ytick.minor.width':   0.1, # major tick width in points
              #square of the fig
              'axes.linewidth':     0.5, 
              'xtick.direction'  : 'out', 
#              'text.usetex': 'True',

                    }
    
    if name=='temporal':

        #tama=9
        #parame= {
        #     	  'figure.figsize':figsize,
        #    	  'font.family' : 'serif',
        #    	  'font.sans-serif'    : 'Helvetica',
        #          'font.size' : 8,
        #    	  'font.weight' : '400',
        #    	  'lines.linewidth':1.0,
        #     	  'legend.fontsize': 'small',
        #     	  'axes.labelsize' : 'small',
        #     	  'axes.labelweight' :'400',
        #     	  'xtick.labelsize': 'small',
        #     	  'ytick.labelsize': 'small',
        #          'xtick.direction': 'out',   
        #tama=8
        #parame= {
        #     	  'figure.figsize':figsize,
        #    	  'font.family' : 'serif',
        #    	  'font.sans-serif'    : 'Helvetica',
        #          'font.size' : tama,
        #    	  'font.weight' : '400',
        #    	  'lines.linewidth':1.0,
        #     	  'legend.fontsize': tama-2,
        #     	  'axes.labelsize' : tama,
        #     	  'axes.labelweight': tama,
        #     	  'xtick.labelsize': tama,
        #     	  'ytick.labelsize': tama,
        #          'xtick.direction': 'out',
        #}

        #tama=6 
        tama=8 
        parame= {                                                   

                  #'text.usetex': False, # Ative o LaTeX real
                  #'text.usetex': True,
                  #'text.latex.preamble': r'\usepackage{amsmath}\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}', 
                  'mathtext.fontset': 'cm',
                  'font.family': 'serif',
                  'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
                  'figure.figsize':figsize,                         
                  #'font.family' : 'serif',                          
                  #'font.sans-serif'    : 'Helvetica',               
                  'font.size' : tama,                             
                  'font.weight' : '500',                            
                  'lines.linewidth':1.0,                            
                  'legend.fontsize': tama-1,                        
                  'axes.titlesize':tama,                          
                  'axes.labelsize' : tama-1,                        
                  #'axes.labelweight': tama,                         
                  'axes.labelweight': '500',
                  'xtick.labelsize': tama,                          
                  'ytick.labelsize': tama,                          
                  'xtick.direction': 'out',                         
        }                                                           
            


    return parame,tama
