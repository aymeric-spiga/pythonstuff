#! /usr/bin/env python

##http://docs.enthought.com/mayavi/mayavi/mlab.html

from enthought.mayavi import mlab
from numpy import ogrid

from netCDF4 import Dataset
from myplot import getfield,reducefield, definesubplot

x, y, z = ogrid[-10:10:100j, -10:10:100j, -10:10:100j]


name = '/home/aymeric/Big_Data/DATAPLOT/diagfired.nc'
nc = Dataset(name)
zefield, error = reducefield ( getfield (nc,"q01"), d4=9 )
help, zefield

zeu, error = reducefield ( getfield (nc,"u"), d4=9 )
zev, error = reducefield ( getfield (nc,"v"), d4=9 )
zew, error = reducefield ( getfield (nc,"w"), d4=9 )

#
#mlab.quiver3d(zeu,zev,zew)

#
src = mlab.pipeline.vector_field(zeu, zev, zew)
mlab.pipeline.vectors(src, mask_points=20, scale_factor=3.)

#
#mlab.pipeline.volume(mlab.pipeline.scalar_field(zefield))

#data, error = reducefield ( getfield (nc,"q01"), d4=9, d3=2 )
#mlab.surf(data, colormap='gist_earth') #, warp_scale=0.2,
            #vmin=1200, vmax=1610)

mlab.show()


zez = 1
yeah, error = reducefield ( getfield (nc,"phisinit"), d3=zez )
help, yeah
ctr = mlab.surf(yeah)

#ctr = mlab.contour3d(0.5*x**2 + y**2 + 2*z**2)
#ctr = mlab.contour3d(zefield)

mlab.show()
