#! /usr/bin/env python

from netCDF4 import Dataset
from myplot import getfield,reducefield, definesubplot
from mymath import writeascii
from numpy import array,transpose
from os import system
from matplotlib.pyplot import plot,show,title,subplot,figure

name = '/home/aymeric/Big_Data/TMPDIR/diagfired.nc'
nc = Dataset(name)
print nc.variables

zevar = ['temp','u','v','q02','q01','v']
zelon = 20
zelat = 20
zetime = 2

fig = figure()
num = len(zevar)
subv,subh = definesubplot( num, fig )

for i in range(num):
    zeprofile, error = reducefield ( getfield (nc,zevar[i]), d4=zetime, d2=zelon, d1=zelat) 
    writeascii(transpose(zeprofile),'profile'+str(i)+'.txt')
    subplot(subv,subh,i)
    plot(zeprofile)
    title(zevar[i])
show()

system("paste -d ' ' profile?.txt > profile.txt ; rm -f profile?.txt")
