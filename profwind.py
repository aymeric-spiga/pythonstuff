#! /usr/bin/env python
import numpy as np
import ppplot as ppp
phalf = 2.e5
transi = 3.
transi = 2.

press = np.logspace(6,0)
pl=ppp.plot1d()
pl.f = press
pl.x = 0.5*(1+np.tanh(transi*np.log(press/phalf)))
pl.fmt = "%2.e"
pl.logy = True
#pl.logx = True
pl.invert = True
pl.makeshow()
