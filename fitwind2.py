#! /usr/bin/env python
import numpy as np
from scipy.io import readsav
import ppplot
import ppcompute
import netCDF4
import math
import os

writefile=False
writefile=True

## READ VASAVADA DATA. CIRS 2006.
## "beyond the scope of this paper to determine"
## "if they are located within a tropospheric"
## "haze (tens to hundreds of mbar) or ammonia cloud (1-2 bars) layer"
vasa = readsav("ashwin05_uprof.sav")
vasawind = np.array( vasa['ashwin05_uprof']['U'][0] )
vasalat = np.array( vasa['ashwin05_uprof']['GRA_LAT'][0] )

## READ SANCHEZ-LAVEGA DATA (Voyager)
## Cloud tracers are expected to be located somewhere
## between 0.5 and 1 bar outside of stormy epochs. 
## Most Voyager wind measurements were performed 
## at a wavelength of 566 nm (green filter)
## that senses altitudes deeper than 1 bar 
## in the absence of particles
sanch = readsav("sanchez-lavega00_data.sav")
sanchwind = np.array( sanch['lavega_data']['field3'][0] )
sanchlat = np.array( sanch['lavega_data']['field2'][0] )

## READ CHOI DATA. A BIT SPARSER. somewhat deep say 2-3 bars.
choi = readsav("all_data2.sav")
listlist = ['s23_003_ab','s23_003_ac','s23_003_bc','s23_004_ab_highlat_vel','s23_004_ab_midlat_vel',\
's27_ab','s27_bc','s27_cd','s27_de','s27_ef','s27_fg','s27_gh','s27_hi','s27_mn',\
's36_ab_vel_edit','s36_cd_vel','s36_ef_vel','s27_003_ab_vel','s27_003_bc_vel']
listlist2 = ['s23_003_lat','s23_003_lat','s23_003_lat','s23_004_ab_highlat_lat','s23_004_ab_midlat_lat',\
's27_lat','s27_lat','s27_lat','s27_lat','s27_lat','s27_lat','s27_lat','s27_lat','s27_lat',\
's36_ab_lat_edit','s36_cd_lat','s36_ef_lat','s27_003_lat','s27_003_lat']
choiwind = []
for yy in listlist:
 for val in choi[yy]:
  choiwind.append(val)
choiwind = np.array(choiwind)
choilat = []
for yy in listlist2:
 for val in choi[yy]:
  choilat.append(val)
choilat = np.array(choilat)

## READ GARCIA-MELENDO DATA (CB 350-700 mbar)
gmcb = np.loadtxt("Table_1_Cassini_CB_Data.txt",skiprows=8,usecols=(1,2))
gmcblat = np.squeeze(gmcb[:,0]) ; gmcbwind = np.squeeze(gmcb[:,1])

## READ GARCIA-MELENDO DATA (MT 60-250 mbar)
gmmt = np.loadtxt("Table_2_Cassini_MT_Data.txt",skiprows=8,usecols=(1,2))
gmmtlat = np.squeeze(gmmt[:,0]) ; gmmtwind = np.squeeze(gmmt[:,1])

## GATHER 
y = np.append(vasawind,sanchwind) ; x = np.append(vasalat,sanchlat)
y = np.append(y,choiwind) ; x = np.append(x,choilat)
	
## OPEN NETCDF start.nc and GET LATITUDES -- and LONGITUDE/ALTITUDE shape
if writefile:
  try:    startnc = netCDF4.Dataset("start.nc") ; dafile = "start.nc"
  except: print "no start.nc"
  try:    startnc = netCDF4.Dataset("restart.nc") ; dafile = "restart.nc"
  except: print "no restart.nc"
  lats = startnc.variables["latitude"][:] ; lats = np.array(lats) ; nlat = lats.shape[0]
  cu = startnc.variables["cu"][:]
  nlon = cu.shape[1]
  press = startnc.variables["presnivs"][:]
else:
  lats = np.linspace(-90,90)
  nlon = 50
  press = np.logspace(-3,3)
  

## BINNING ! 
## -- method 1
#meanwind = ppcompute.meanbin(y,x,lats)
## -- method 2 (each dataset has same weight)
choi = ppcompute.meanbin(choiwind,choilat,lats)
sanch = ppcompute.meanbin(sanchwind,sanchlat,lats)
vasa = ppcompute.meanbin(vasawind,vasalat,lats)
gmcb = ppcompute.meanbin(gmcbwind,gmcblat,lats)
gmmt = ppcompute.meanbin(gmmtwind,gmmtlat,lats)
meanwind = []
for iii in range(len(choi)):
    #tab = [choi[iii],sanch[iii]]
    #tab = [choi[iii],sanch[iii],vasa[iii]]
    #tab = [choi[iii],sanch[iii],vasa[iii],gmcb[iii]]
    tab = [choi[iii],sanch[iii],vasa[iii],gmcb[iii],gmmt[iii]]
    comp = ppcompute.mean(tab)
    if np.abs(lats[iii]) >= 85.: comp = 0.
    if np.abs(lats[iii]) >= 80.: comp = comp/5.
    if np.abs(lats[iii]) >= 78.: comp = comp/2.
    if math.isnan(comp): meanwind.append(0.)
    else: meanwind.append(comp)

## smooth a little bit    
meanwind = ( np.roll(meanwind,-1) + meanwind + np.roll(meanwind,1) ) / 3.

## ADD LONGITUDE DIMENSION and ALTITUDE DIMENSION
unat = np.tile(meanwind,(nlon,1)).transpose()
nz = press.shape[0]
unat = np.tile(unat,(nz,1,1)).transpose()

if writefile:
   
   ## CALCULATE COVARIANT WIND
   cu = np.tile(cu,(nz,1,1)).transpose()
   ucov = unat*cu
   
#   ## VERTICAL VARIATIONS
#   p0 = 2.e5 # pressure above which constant wind is set
#   #p0 = 5.e4
#   #p0 = 2.e4
#   presscalc = np.tile(press,(nlon,nlat,1))
#   ucov[np.where(presscalc < p0)] = -2.e20
   unat = ucov / cu
   
   ## MODIFY FIELDS IN start FILE
   startnc.close()
   os.system("cp "+dafile+" relax.nc")
   startncmod = netCDF4.Dataset("relax.nc",'a')
   ucov_infile = startncmod.variables["ucov"]
   ucov_infile[0,:,:,:] = ucov.transpose()[:,::-1,:]
   startncmod.close()


## PLOT PLOT PLOT
###################################
ppplot.figuref(x=8,y=6)
r = ppplot.plot2d()
r.f = np.squeeze(unat[0,:,:])
r.x = lats
r.y = press
r.invert = True
r.logy = True
r.vmin = -100.
r.vmax = 400.
r.xmin = -90.
r.xmax = 90.
r.colorbar = "spectral"
r.fmt = "%.0f"
r.swaplab = False
r.xlabel = "Latitude ($^{\circ}$N)"
r.ylabel = "Pressure (Pa)"
r.units = "m s$^{-1}$"
r.make()
ppplot.save(mode="png",filename="section",includedate=False)
ppplot.close()

###################################
ppplot.figuref(x=12,y=8)
##
r = ppplot.plot1d()
r.f = gmcbwind
r.x = gmcblat
r.marker = '.'
r.linestyle = ''
r.color = 'p'
r.legend = "Cassini ISS CB (GM11)"
r.make()
##
r = ppplot.plot1d()
r.f = gmmtwind
r.x = gmmtlat
r.marker = '.'
r.linestyle = ''
r.color = 'm'
r.legend = "Cassini ISS MT (GM11)"
r.make()
##
r = ppplot.plot1d()
r.f = choiwind
r.x = choilat
r.marker = '.'
r.linestyle = ''
r.color = 'y'
r.legend = "Cassini CIRS (C09)"
r.make()
##
r = ppplot.plot1d()
r.f = vasawind
r.x = vasalat
r.marker = '.'
r.linestyle = ''
r.color = 'g'
r.legend = "Cassini ISS (V06)"
r.make()
##
r = ppplot.plot1d()
r.f = sanchwind
r.x = sanchlat
r.marker = '.'
r.linestyle = ''
r.color = 'c'
r.legend = "Voyager (SL00)"
r.make()
##
r = ppplot.plot1d()
r.f = meanwind
r.x = lats
r.marker = 'o'
r.linestyle = '-'
r.color = 'k'
r.ylabel = "Zonal wind (m s$^{-1}$)"
r.xlabel = "Latitude ($^{\circ}$N)"
r.xmin = -90.
r.xmax = 90.
r.ymin = -150.
r.div = 36
r.legend = "Binning on GCM grid"
r.make()
##
ppplot.save(mode="png",filename="zonalwinds",includedate=False)
