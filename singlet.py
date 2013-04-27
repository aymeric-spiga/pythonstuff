#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as mpl
from scipy import integrate 

def singlet(rel_rho,z):

        ###### z MUST BE IN km
        z = np.array(z)
        rel_rho = np.array(rel_rho)

	alpha = 1.7e-3    	##sec^(-1)= ozone photolysis rate constant - from Nair et al. 1994, scaled at the considered LS
	k =  2.0e-20   		##cm^(-3)molecules^(-1) sec^(-1) = co2 quenching rate constant - upper limit from 
	tau = 3880       	##sec = O2(a1Delatg) molecules life time
	gamma = 1.4 		##;= ratio of specific heats
	zh_o3 = 10		##; *** km = peak altitude of the O3 layer 
	H = 11.0 		##;scale eight
        H = 8.3
        H = 9.5
	co2_0 = 2e17
	exponent = - z / H
	co2p_u = co2_0 * np.exp(exponent) 
	#;analytical expression for the O3 unperturbed vertical profile 
	zo3 = 26.
	H1 = 5.4
	H2 = 15.
	f = 1.17e9

        #### COMPUTE g0
	exponent = -(z-zo3)/H2
	g0 = (gamma*H-H1)/((gamma-1.)*H1) -(gamma*H)/(H2*(gamma-1.))*np.exp(exponent)

        ### OZONE PERTURBED AND UNPERTURBED
        exponent1 = -(z-zo3)/H1
        exponent2 = -(z-zo3)/H2
        o3p_u = f * np.exp( exponent1 - np.exp(exponent2) )
	o3p_p = o3p_u*np.power(rel_rho,g0)

        ### CO2 STUFF
	co2p_p = co2p_u*rel_rho

        ### SINGLET PROFILE
        o2p_p = (0.9*alpha*o3p_p)/(1.+tau*k*co2p_p)     
        o2p_u = (0.9*alpha*o3p_u)/(1.+tau*k*co2p_u) 
        rel  = 100. * ( o2p_p  / o2p_u  - 1. )

        ### SINGLET INTEGRATED
        o2p_pi = integrate.trapz(o2p_p,x=z)
        o2p_ui = integrate.trapz(o2p_u,x=z)
        reli = 100. * ( o2p_pi / o2p_ui - 1. )

        #mpl.plot(rel,z)
        #mpl.show()

	return reli, rel
