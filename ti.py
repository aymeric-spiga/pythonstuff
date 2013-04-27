#! /usr/bin/env python

from netCDF4 import Dataset
import matplotlib.pyplot as mpl
import numpy as np

nc = Dataset("geo_em.d01.nc")
#ti = np.ravel(nc.variables["THERMAL_INERTIA"][:,:])
#alb = np.ravel(nc.variables["ALBEDO_GCM"][:,:])

#lat = np.ravel(nc.variables["XLAT_M"][:,:])

#alb = alb[ lat < 80.]
#ti = ti[ lat < 80. ] 

#alb = np.log(alb)
#ti = np.log(ti)

#mpl.plot(ti,alb,'b.')
#mpl.plot(ti,lat,'b.')


limalb = 0.28
limti = 800.
icealb = 0.45

ti = nc.variables["THERMAL_INERTIA"][0,:,:]
alb = nc.variables["ALBEDO_GCM"][0,:,:]
ti [ alb > limalb ] = limti
ti [ ti > limti ] = limti
alb [ alb > limalb ] = icealb

mpl.figure()
mpl.subplot(121)
mpl.contourf(ti,100)
mpl.colorbar()
mpl.subplot(122)
mpl.contourf(alb,100)
mpl.colorbar()

mpl.show()
