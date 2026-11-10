import  os,sys

import cartopy.crs as ccrs
plotdef='mapa2'
#Latex width 
wf=1.5
hf=0.5
cmmais=0.0
#plot size of the figures
#cmmais are the cm to put the cbbar  without modified the size of the fig
projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)
#############plot formated
# make the map global rather than have it zoom in to
# the extents of any plotted data
###################################3
#skip poitnt in vector plot
npp=10

temporal={
          'plotdef':'temporal',
          'wf'     :0.7,
          'hf'     :0.5,
          'cmmais' :0.0,
          }

profile={
          'plotdef':'temporal',
          'wf'     :0.35,
          'hf'     :1.5,
          'cmmais' :0.0,
          'fontsize':6, 
          }

epf={
          'plotdef':'temporal',
          'wf'     :0.7,
          'hf'     :1.5,
          'cmmais' :0.0,
          'fontsize':6, 
          }

egeon='/pesq'

path='/home/jhonatan.aguirre/Modal_Energetics/Version_4.0/document_ss/figs'

extend='both'


# Out figure folder
out_fig=path

#out python nc files
out_files= path+'/python_nc'


# Check if the directory exists
if not os.path.exists(out_fig):
    # If it doesn't exist, create it
    os.makedirs(out_fig)

# Check if the directory exists
if not os.path.exists(out_files):
    # If it doesn't exist, create it
    os.makedirs(out_files)
