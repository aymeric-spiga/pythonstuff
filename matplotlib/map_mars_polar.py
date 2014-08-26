#!/usr/bin/env python

##########################################################################
import  numpy                           as np
import  myplot                          as myp
import  mymath				as mym
import  netCDF4
import  matplotlib.pyplot as plt
##########################################################################
namefile  = '/home/aslmd/POLAR/POLAR_APPERE_highres/wrfout_d01_2024-03-04_06:00:00_zabg'
namefile2 = '/home/aslmd/POLARWATERCYCLE/wrfout_d01_2024-05-03_01:00:00_zabg' 
nc  = netCDF4.Dataset(namefile)
[lon2d,lat2d] = myp.getcoord2d(nc)
##########################################################################
ntime = 5
nvert = 1
u   = nc.variables['Um'   ][ntime,nvert,:,:]
v   = nc.variables['Vm'   ][ntime,nvert,:,:]
##########################################################################
plt.figure(1)
##########################################################################
[lon2d,lat2d] = myp.getcoord2d(nc)
[wlon,wlat] = myp.latinterv("North_Pole")
#plt.title("Polar mesoscale domain")
m = myp.define_proj("ortho",wlon,wlat,back="vishires")
x, y = m(lon2d, lat2d)
m.pcolor(x, y, nc.variables['HGT'][0,:,:] / 1000.)
###########################################################################
myp.makeplotpng("mars_polar_mesoscale_1",folder="/u/aslmd/WWW/antichambre/",pad_inches_value=0.15)
###########################################################################
plt.figure(2)
plt.subplot(121)
[lon2d,lat2d] = myp.getcoord2d(nc)
[wlon,wlat] = myp.latinterv("Close_North_Pole")
plt.title("Near-surface winds at Ls=60"+mym.deg())
m = myp.define_proj("npstere",wlon,wlat,back="vishires")
x, y = m(lon2d, lat2d)
myp.vectorfield(u, v, x, y, stride=5, csmooth=6, scale=15., factor=200., color='darkblue')
###########################################################################
plt.subplot(122)
[wlon,wlat] = [[-180.,180.],[84.,90.]]
plt.title("+ sensible heat flux (W/m2)")
m = myp.define_proj("npstere",wlon,wlat,back="vishires")
x, y = m(lon2d, lat2d)
zeplot = m.contour(x, y, -nc.variables['HFX'][ntime,:,:],[-2.,0.,2.,4.,6.,8.,10.,12.],cmap=plt.cm.Reds)
plt.clabel(zeplot, inline=1, inline_spacing=1, fontsize=7, fmt='%0i')
myp.vectorfield(u, v, x, y, stride=2, scale=15., factor=200., color='darkblue')
#plt.colorbar(pad=0.1).set_label('Downward sensible heat flux [W/m2]')
###########################################################################
myp.makeplotpng("mars_polar_mesoscale_2",folder="/u/aslmd/WWW/antichambre/",pad_inches_value=0.35)
###########################################################################
nc = netCDF4.Dataset(namefile2)
[lon2d,lat2d] = myp.getcoord2d(nc)
##########################################################################
plt.figure(3)
###########################################################################
[wlon,wlat] = [[mym.min(lon2d),mym.max(lon2d)],[mym.min(lat2d)+7.,mym.max(lat2d)]]
#plt.figure(2)
#plt.title("Water vapor (pr.mic)")
#field = np.array(nc.variables['MTOT'])
#nnn = field.shape[2]
#ye = plt.contour(	np.arange(field.shape[0]),\
#			np.linspace(wlat[0],wlat[1],nnn),\
#			np.transpose(mym.mean(field,axis=1)),\
#			np.arange(0.,100.,5.))
#plt.clabel(ye, inline=1, inline_spacing=1, fontsize=7, fmt='%0i')
############################################################################
sub = 121
for i in range(3,23,12):
	print i,sub
	plt.subplot(sub)
	plt.title("H2Ovap (pr.mic) UTC "+str(i+1)+":00")
	m = myp.define_proj("npstere",wlon,wlat,back="vishires")
	x, y = m(lon2d, lat2d)
	yeah = m.contour(x, y, nc.variables['MTOT'][i,:,:],np.arange(30.,90.,10.),linewidths=1.0)
	plt.clabel(yeah, inline=1, inline_spacing=1, width=1.0, fontsize=7, fmt='%0i')
	sub += 1
	print sub
############################################################################
myp.makeplotpng("mars_polar_mesoscale_3",folder="/u/aslmd/WWW/antichambre/", pad_inches_value=0.15)
############################################################################

#yeah = m.contour(x, y, mym.mean(nc.variables['MTOT'],axis=0),np.arange(0.,75.,5.),cmap=plt.cm.gist_rainbow,linewidths=1.5)
