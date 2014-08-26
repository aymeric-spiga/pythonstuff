#!/usr/bin/env python

##########################################################################
var = ["151","146","167"]
var = ["167"]
var = ["78"]
var = ["137"]
#var = ["174"] albedo marche pas.
lev = ["700.","850."]
tim = ["00"]
date = ['10','08','2010','10','08','2010']
date = ['01','09','2009','01','09','2009']
#date = ['01','09','2010','01','09','2010']
dataset = ["an","pl","0"]
dataset = ["fc","sfc","3"]
##########################################################################
proj = "cyl"  #"moll" "ortho" "lcc"
#proj = "ortho"
#proj = "moll"
area = "Europe"
area = "Africa"
area = "Central_America"
#area = "Southern_Hemisphere"
#area = "Northern_Hemisphere"
#area = "Whole_No_High"
area = "Whole"
back="blue"
#back="bw"
#back="moc"
##########################################################################


##########################################################################
import 	numpy 				as np
import 	matplotlib.pyplot 		as plt
import  myplot				as myp
import  myecmwf				as mye
##########################################################################
if dataset[1] == "sfc": lev = [9999.]
[wlon,wlat] = myp.latinterv(area)
nc = mye.get_ecmwf (var, dataset, wlat, wlon, lev, date, tim) 
##########################################################################
[lon2d,lat2d] = myp.getcoord2d (nc,nlat='lat',nlon='lon',is1d=True)
step=10.
##########################################################################
ntime = 0
for i in range( np.array(var).size ):
	for z in range( np.array(lev).size ):
		for t in range( np.array(tim).size ):

                    field, error = myp.reducefield( myp.getfield(nc,'var'+var[i]), d4=t, d3=z )
                    if not error:
                        ### Map projection
                        m = myp.define_proj(proj,wlon,wlat,back=back)
                        x, y = m(lon2d, lat2d)
		        zeplot = m.contour(x, y, field, 10) #15
		        plt.clabel(zeplot, inline=1, inline_spacing=1, fontsize=7, fmt='%0i')
		        #plt.colorbar(fraction=0.05,pad=0.1)
		        plt.title(mye.ecmwf_title_field(var[i]))
                        myp.makeplotres(str(var[i])+str(lev[z])+str(tim[t]),res=100.,pad_inches_value=0.35)
