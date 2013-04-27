#! /usr/bin/env python

from netCDF4 import Dataset
import matplotlib.pyplot as mpl
import numpy as np
from myplot import reducefield,getfield,getcoorddef,calculate_bounds,bounds,fmtvar,ptitle,makeplotres
from matplotlib.pyplot import contourf,colorbar,show,xlabel,ylabel
from matplotlib.cm import get_cmap

name = "wrfout_d01_9999-09-09_09:00:00_z"
itime = 12
#itime = 1
ndiv = 10
zey = 0
var = "W"
vmin = -1.
vmax = 1.
title = "Vertical velocity"
var = "Um"
vmin = -2.
vmax = 18.
title = "Horizontal velocity"
#var = "tk"
#vmin = 150.
#vmax = 170.
#title = "Atmospheric temperature"

name = "wrfout_d01_2024-03-22_01:00:00_z"
itime = 12
ndiv = 10
zey = 120
var = "VMR_ICE"
title = "Volume mixing ratio of water ice [ppm]"
vmin = -0.5
vmax = 400.

nc = Dataset(name)

what_I_plot, error = reducefield( getfield(nc,var), d4=itime, d2=zey )


y = nc.variables["vert"][:]

horinp = len(what_I_plot[0,:])
x = np.linspace(0.,horinp*500.,horinp) / 1000.
xlabel("Horizontal coordinate (km)")

horinp = len(what_I_plot[0,:])
x = np.linspace(0.,horinp,horinp) 
xlabel("x grid points")


zevmin, zevmax = calculate_bounds(what_I_plot,vmin=vmin,vmax=vmax)
#if colorb in ["def","nobar"]:   palette = get_cmap(name=defcolorb(fvar))
#else:                           palette = get_cmap(name=colorb)
palette = get_cmap(name="jet")
what_I_plot = bounds(what_I_plot,zevmin,zevmax)
zelevels = np.linspace(zevmin,zevmax)
contourf( x, y, what_I_plot, zelevels, cmap = palette )
colorbar(fraction=0.05,pad=0.03,format=fmtvar(var),\
                       ticks=np.linspace(zevmin,zevmax,ndiv+1),\
                       extend='neither',spacing='proportional')
ptitle(title)
ylabel("Altitude (m)")
makeplotres(var+str(itime),res=200.,disp=False)
#show()
