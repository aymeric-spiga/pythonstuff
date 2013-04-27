#! /usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

vvv = np.array([ 8.9, 7.3, 3.9, 2.0])
rrr = np.array([ 2.0, 5.0, 8.0,11.0])

logv = np.log(vvv)
logr = np.log(rrr)

vvv1 = 1./rrr
vvv2 = 1./np.sqrt(rrr)

logv1 = 3. + np.log(vvv1)
logv2 = 3. + np.log(vvv2)

plt.plot(logv,logr,'bo',logv1,logr,'r',logv2,logr,'y')
plt.show()
