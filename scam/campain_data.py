#####################################################
#Campain data
from    metpy.units import units
#       To change the plot parameter 
import  metpy.calc

import  numpy as np 

def campain_goa(goamz):

    maxit   = len(goamz.time)
    maxlv   = len(goamz.lev)

    q_ls_goa    =   units.Quantity(goamz.q_adv_h[:][:],'g/kg/hour')
    q_ls_goa    =   q_ls_goa.to('kg/kg/s')
    #Horizontal advection tendency of air temperature
    t_ls_goa        =   units.Quantity(goamz.T_adv_h[:][:],'k/hour')
    t_ls_goa        =   t_ls_goa.to('k/s')
    #Temperature 
    T_goa           =   goamz.T
    Tu_goa          =   units.Quantity(T_goa[:][:],'kelvin')
    #Humidity 
    q_goa           =   goamz.q
    qu_goa          =   units.Quantity(q_goa[:][:],'gr/kg')
    #Velocities 
    u_goa           =   goamz.u
    v_goa           =   goamz.v
    #w           =   bomex.w_subsidence(bomex._z)
    omega_goa       =   units.Quantity(goamz.omega[:],'mbar/hour')
    z_goa           =   np.zeros(maxlv)
    pressureu_goa   =   units.Quantity(goamz.lev[:], 'mbar')
    pressureu_goa   =   pressureu_goa.to('hPa')
    #########
    theta_goa       =   metpy.calc.potential_temperature(pressureu_goa, Tu_goa)
    ######
    w_goa           =   metpy.calc.vertical_velocity(omega_goa, pressureu_goa, Tu_goa, mixing=0)
    
    #Parameters to transform units 
    g      = 9.81 *units('m/s^2')   # [m/s^2]
    R_d    = 287.0*units('J/kg/K')   # [J/kg/K]
    
    Tv_goa  =   metpy.calc.virtual_temperature(Tu_goa, qu_goa).to('kg*K/kg')
    
    alt_goa         =   units.Quantity(goamz.alt[:],'m')
    
    #Lengh of the time array to search
    ndtp    = len(goamz.time) 
    
    #Lengh of the time array to search
    ndlev   = len(goamz.lev) 
    
    
    z_goa   = np.zeros((ndtp,ndlev))*units('m')
    
    z_goa[:,0]   =   alt_goa   
    
    for k in range(0,ndtp):
    
        for i in range(1,ndlev):
    
            #z[k,i]   = metpy.calc.add_pressure_to_height(z[k,i-1], pressureu[i])
            z_goa[k,i]   =    R_d*Tv_goa[k,0]/g*np.log(pressureu_goa[i-1]/pressureu_goa[i])+z_goa[k,i-1]    


    p_goa   =   pressureu_goa.to('mbar')

    return theta_goa,q_goa,u_goa,v_goa,w_goa,z_goa,p_goa
    



