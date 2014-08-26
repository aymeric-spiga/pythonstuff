#! /usr/bin/env python
import numpy as np
import ppplot as ppp
phalf = 100.
press = np.logspace(6,-6)
pl=ppp.plot1d()
pl.f = press
pl.x = 0.5*(1+np.tanh(np.log(press/phalf)))
pl.fmt = "%2.e"
pl.logy = True
pl.logx = True
pl.invert = True
pl.makeshow()
