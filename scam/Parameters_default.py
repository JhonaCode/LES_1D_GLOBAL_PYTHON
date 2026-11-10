import  os,sys
import cartopy.crs as ccrs

MODEL='SCAM'

plotdef='2d'

#Latex width 
wf=0.50
hf=1.0
cmmais=0.0

extend='both'

computer='/pesq'

UTC=-4

path =computer+"/dados/bamc/jhonatan.aguirre/git_repositories/SCAM_CESM" 

# Out figure folder
#out_fig=path+'/document/fig'
#out_fig=path+'/PRESSAO/document/fig_2014'
out_fig=path+'/document/figs'
#out_fig=path+'/pesq/dados/bamc/jhonatan.aguirre/git_repositories/relatorio_pci/pci_2026/fig'


out_table=path+'/python/'

#out python nc files
out_files= path+'/python/'


# Check if the directory exists
if not os.path.exists(out_fig):
    # If it doesn't exist, create it
    os.makedirs(out_fig)

# Check if the directory exists
if not os.path.exists(out_table):
    # If it doesn't exist, create it
    os.makedirs(out_table)

# Check if the directory exists
if not os.path.exists(out_files):
    # If it doesn't exist, create it
    os.makedirs(out_files)
