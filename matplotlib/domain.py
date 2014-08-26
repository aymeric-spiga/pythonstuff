#!/usr/bin/env python

### A. Spiga -- LMD -- 30/06/2011 -- slight modif early 07/2011

def domain (namefile,proj=None,back="vishires",target=None): 
    from netCDF4 import Dataset
    from myplot import getcoord2d,define_proj,makeplotres,simplinterv,getprefix,dumpbdy,getproj,latinterv,wrfinterv,simplinterv
    from mymath import max,min
    from matplotlib.pyplot import contourf,rcParams,pcolor
    from numpy.core.defchararray import find
    from numpy import arange
    ###
    nc  = Dataset(namefile)
    ###
    if proj == None:  proj = "ortho" #proj = getproj(nc)
    ###
    prefix = namefile[0] + namefile[1] + namefile[2]
    if prefix == "geo":   
        [lon2d,lat2d] = getcoord2d(nc,nlat='XLAT_M',nlon='XLONG_M')
        var = 'HGT_M'
        zeplot = "domain" 
    else:                 
        [lon2d,lat2d] = getcoord2d(nc)
        var = "HGT"
        zeplot = getprefix(nc) + "domain"
    ###
    lon2d = dumpbdy(lon2d,5)
    lat2d = dumpbdy(lat2d,5)
    if proj == "npstere":             [wlon,wlat] = latinterv("North_Pole")
    elif proj in ["lcc","laea"]:      [wlon,wlat] = wrfinterv(lon2d,lat2d)
    else:                             [wlon,wlat] = simplinterv(lon2d,lat2d)
    ###
    m = define_proj(proj,wlon,wlat,back=back)
    x, y = m(lon2d, lat2d)
    ###
    what_I_plot = dumpbdy(nc.variables[var][0,:,:], 5)
    #levinterv = 250.
    #zelevels = arange(min(what_I_plot)-levinterv,max(what_I_plot)+levinterv,levinterv)
    zelevels = 30
    contourf(x, y, what_I_plot, zelevels)
    #pcolor(x,y,what_I_plot)  ## on voit trop les lignes !
    ###
    if not target:   zeplot = namefile[0:find(namefile,'wrfout')] + zeplot
    else:            zeplot = target + "/" + zeplot          
    ###
    pad_inches_value = 0.35
    makeplotres(zeplot,res=100.,pad_inches_value=pad_inches_value) #,erase=True)  ## a miniature
    makeplotres(zeplot,res=200.,pad_inches_value=pad_inches_value,disp=False)
    #makeplotpng(zeplot,pad_inches_value=0.35)
    #rcParams['savefig.facecolor'] = 'black'
    #makeplotpng(zeplot+"b",pad_inches_value=0.35)

if __name__ == "__main__":
    import sys
    ### to be replaced by argparse
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-f', action='store', dest='namefile',    type="string",  default=None,       help='name of WRF file [NEEDED]')
    parser.add_option('-p', action='store', dest='proj',        type="string",  default=None,       help='projection')
    parser.add_option('-b', action='store', dest='back',        type="string",  default="vishires", help='background')
    parser.add_option('-t', action='store', dest='target',      type="string",  default=None,       help='destination folder')
    (opt,args) = parser.parse_args()
    if opt.namefile is None:
        print "I want to eat one file at least ! Use domain.py -f name_of_my_file. Or type domain.py -h"
        exit()
    print "Options:", opt
    domain (opt.namefile,proj=opt.proj,back=opt.back,target=opt.target)
