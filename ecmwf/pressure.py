#!/usr/bin/env python
from myecmwf import get_ecmwf
from ppclass import pp
from ppplot import plot2d
import numpy as np

##########################################################################
var = ["151"]
fieldtype = "2d"
lev = ["9999."]
tim = ["00"]
date = ['01','09','2009','01','09','2009']
#area = "Whole"



date = ['01','04','2011','01','04','2011']


##########################################################################
nc = get_ecmwf (var, fieldtype, [-90.,90.], [-180.,180.], lev, date, tim) 
press = pp(file="output.nc",var="var"+var[0]).getf()



press = press / 1e2

pl = plot2d()
pl.f = press
#pl.trans = 0.0
pl.colorbar = "RdBu_r"
pl.c = press
pl.x = np.linspace(-180.,180.,press.shape[1])
pl.y = np.linspace(-90.,90.,press.shape[0])
pl.mapmode = True

pl.vmin = 950.
pl.vmax = 1050.
pl.div = 20

pl.back = "coast"
pl.makeshow()







