#!/usr/bin/env python

### A. Spiga -- LMD -- 30/06/2011 to 10/07/2011
### Thanks to A. Colaitis for the parser trick


####################################
####################################
### The main program to plot vectors
def winds (namefile,\
           nvert,\
           proj=None,\
           back=None,\
           target=None,
           stride=3,\
           numplot=2,\
           var=None,\
           colorb="def",\
           winds=True,\
           addchar=None,\
           interv=[0,1],\
           vmin=None,\
           vmax=None,\
           tile=False,\
           zoom=None,\
           display=True,\
           itstep=None,\
           hole=False,\
           save="gui",\
           anomaly=False,\
           var2=None,\
           ndiv=10,\
           first=1,\
           mult=1.,\
           zetitle="fill"):

    ####################################################################################################################
    ### Colorbars http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps?action=AttachFile&do=get&target=colormaps3.png

    #################################
    ### Load librairies and functions
    from netCDF4 import Dataset
    from myplot import getcoord2d,define_proj,makeplotres,simplinterv,vectorfield,ptitle,latinterv,getproj,wrfinterv,dumpbdy,\
                       fmtvar,definecolorvec,defcolorb,getprefix,putpoints,calculate_bounds,errormess,definesubplot,\
                       zoomset,getcoorddef,getwinddef,whatkindfile,reducefield,bounds,getstralt,getfield,smooth,nolow,\
                       getname,localtime,polarinterv
    from mymath import deg,max,min,mean
    from matplotlib.pyplot import contour,contourf, subplot, figure, rcParams, savefig, colorbar, pcolor, show
    from matplotlib.cm import get_cmap
    import numpy as np
    from numpy.core.defchararray import find

    ######################
    ### Load NETCDF object
    nc  = Dataset(namefile)  
    
    ##################################
    ### Initial checks and definitions
    typefile = whatkindfile(nc)                                  ## TYPEFILE
    if var not in nc.variables: var = False                      ## VAR
    if winds:                                                    ## WINDS
        [uchar,vchar,metwind] = getwinddef(nc)             
        if uchar == 'not found': winds = False
    if not var and not winds: errormess("please set at least winds or var",printvar=nc.variables)
    [lon2d,lat2d] = getcoorddef(nc)                              ## COORDINATES, could be moved below
    if proj == None:   proj = getproj(nc)                        ## PROJECTION

    ##########################
    ### Define plot boundaries
    ### todo: possible areas in latinterv in argument (ex: "Far_South_Pole")
    if proj in ["npstere","spstere"]: [wlon,wlat] = polarinterv(lon2d,lat2d)
    elif proj in ["lcc","laea"]:      [wlon,wlat] = wrfinterv(lon2d,lat2d)
    else:                             [wlon,wlat] = simplinterv(lon2d,lat2d)
    if zoom:                          [wlon,wlat] = zoomset(wlon,wlat,zoom) 

    #########################################
    ### Name for title and graphics save file
    basename = getname(var=var,winds=winds,anomaly=anomaly)
    basename = basename + getstralt(nc,nvert)  ## can be moved elsewhere for a more generic routine

    ##################################
    ### Open a figure and set subplots
    fig = figure()
    subv,subh = definesubplot( numplot, fig ) 
 
    #################################
    ### Time loop for plotting device
    found_lct = False
    nplot = 1
    itime = first
    error = False
    if itstep is None and numplot > 0: itstep = int(24./numplot)
    elif numplot <= 0:                 itstep = 1
    while error is False: 

       ### Which local time ?
       ltst = localtime ( interv[0]+itime*interv[1], 0.5*(wlon[0]+wlon[1]) )

       ### General plot settings
       #print itime, int(ltst), numplot, nplot
       if numplot >= 1: 
           if nplot > numplot: break
           if numplot > 1:     
               if typefile not in ['geo']:  subplot(subv,subh,nplot)
           found_lct = True
       ### If only one local time is requested (numplot < 0)
       elif numplot <= 0: 
           if int(ltst) + numplot != 0:	
                 itime += 1 
                 if found_lct is True: break     ## because it means LT was found at previous iteration
                 else:                 continue  ## continue to iterate to find the correct LT
           else: 
                 found_lct = True

       ### Map projection
       m = define_proj(proj,wlon,wlat,back=back)
       x, y = m(lon2d, lat2d)

       #### Contour plot
       if var2:
           what_I_contour, error = reducefield( getfield(nc,var2), d4=itime, d3=nvert )
           if not error:
               if typefile in ['mesoapi','meso']:    what_I_contour = dumpbdy(what_I_contour,6)
               zevmin, zevmax = calculate_bounds(what_I_contour)
               zelevels = np.linspace(zevmin,zevmax,num=20)
               if var2 == 'HGT':  zelevels = np.arange(-10000.,30000.,2000.)
               contour( x, y, what_I_contour, zelevels, colors='k', linewidths = 0.33 ) #colors='w' )# , alpha=0.5)
           else:
               errormess("There is an error in reducing field !")

       #### Shaded plot
       if var:
           what_I_plot, error = reducefield( getfield(nc,var), d4=itime, d3=nvert )
           what_I_plot = what_I_plot*mult
           if not error: 
               fvar = var
               ###
               if anomaly:
                   what_I_plot = 100. * ((what_I_plot / smooth(what_I_plot,12)) - 1.)
                   fvar = 'anomaly'
               #if mult != 1:     
               #    fvar = str(mult) + "*" + var
               ###
               if typefile in ['mesoapi','meso']:    what_I_plot = dumpbdy(what_I_plot,6)
               zevmin, zevmax = calculate_bounds(what_I_plot,vmin=vmin,vmax=vmax)
               if colorb in ["def","nobar"]:   palette = get_cmap(name=defcolorb(fvar))
               else:                           palette = get_cmap(name=colorb)
               if not tile:
                   if not hole: what_I_plot = bounds(what_I_plot,zevmin,zevmax)
                   #zelevels = np.linspace(zevmin*(1. + 1.e-7),zevmax*(1. - 1.e-7)) #,num=20)
                   zelevels = np.linspace(zevmin,zevmax)
                   contourf( x, y, what_I_plot, zelevels, cmap = palette )
               else:
                   if hole:  what_I_plot = nolow(what_I_plot) 
                   pcolor( x, y, what_I_plot, cmap = palette, \
                           vmin=zevmin, vmax=zevmax )
               if colorb != 'nobar' and var != 'HGT':              
                         colorbar(fraction=0.05,pad=0.03,format=fmtvar(fvar),\
                                           ticks=np.linspace(zevmin,zevmax,ndiv+1),\
                                           extend='neither',spacing='proportional')
                                           # both min max neither 
           else:
               errormess("There is an error in reducing field !")
 
       ### Vector plot
       if winds:
           vecx, error = reducefield( getfield(nc,uchar), d4=itime, d3=nvert )
           vecy, error = reducefield( getfield(nc,vchar), d4=itime, d3=nvert )
           if not error:
               if typefile in ['mesoapi','meso']:    
                   [vecx,vecy] = [dumpbdy(vecx,6,stag=uchar), dumpbdy(vecy,6,stag=vchar)]
                   key = True
               elif typefile in ['gcm']:            
                   key = False
               if metwind:  [vecx,vecy] = m.rotate_vector(vecx, vecy, lon2d, lat2d)
               if var == False:       colorvec = definecolorvec(back)
               else:                  colorvec = definecolorvec(colorb)
               vectorfield(vecx, vecy,\
                          x, y, stride=stride, csmooth=2,\
                          #scale=15., factor=300., color=colorvec, key=key)
                          scale=20., factor=250., color=colorvec, key=key)
                                            #200.         ## or csmooth=stride
               
       ### Next subplot
       plottitle = basename
       if typefile in ['mesoapi','meso']:
            if addchar:  plottitle = plottitle + addchar + "_LT"+str(ltst)
            else:        plottitle = plottitle + "_LT"+str(ltst)
       if mult != 1:           plottitle = str(mult) + "*" + plottitle
       if zetitle != "fill":   plottitle = zetitle
       ptitle( plottitle )
       itime += itstep
       nplot += 1

    ##########################################################################
    ### Save the figure in a file in the data folder or an user-defined folder
    if typefile in ['meso','mesoapi']:   prefix = getprefix(nc)   
    elif typefile in ['gcm']:            prefix = 'LMD_GCM_'
    else:                                prefix = ''
    ###
    zeplot = prefix + basename 
    if addchar:         zeplot = zeplot + addchar
    if numplot <= 0:    zeplot = zeplot + "_LT"+str(abs(numplot))
    ###
    if not target:      zeplot = namefile[0:find(namefile,'wrfout')] + zeplot
    else:               zeplot = target + "/" + zeplot  
    ###
    if found_lct:     
        pad_inches_value = 0.35
        if save == 'png': 
            if display: makeplotres(zeplot,res=100.,pad_inches_value=pad_inches_value) #,erase=True)  ## a miniature
            makeplotres(zeplot,res=200.,pad_inches_value=pad_inches_value,disp=False)
        elif save in ['eps','svg','pdf']:
            makeplotres(zeplot,         pad_inches_value=pad_inches_value,disp=False,ext=save)
        elif save == 'gui':
            show()
        else: 
            print "save mode not supported. using gui instead."
            show()
    else:   print "Local time not found"

    ###############
    ### Now the end
    return zeplot

##############################
### A specific stuff for below
def adjust_length (tab, zelen):
    from numpy import ones
    if tab is None:
        outtab = ones(zelen) * -999999
    else:
        if zelen != len(tab):
            print "not enough or too much values... setting same values all variables"
            outtab = ones(zelen) * tab[0]
        else:
            outtab = tab
    return outtab

###########################################################################################
###########################################################################################
### What is below relate to running the file as a command line executable (very convenient)
if __name__ == "__main__":
    import sys
    from optparse import OptionParser    ### to be replaced by argparse
    from api_wrapper import api_onelevel
    from netCDF4 import Dataset
    from myplot import getlschar
    from os import system

    #############################
    ### Get options and variables
    parser = OptionParser()
    parser.add_option('-f', '--file',   action='append',dest='namefile', type="string",  default=None,  help='[NEEDED] name of WRF file (append)')
    parser.add_option('-l', '--level',  action='store',dest='nvert',     type="float",   default=0,     help='level (def=0)(-i 2: p,mbar)(-i 3,4: z,km)')
    parser.add_option('-p', '--proj',   action='store',dest='proj',      type="string",  default=None,  help='projection')
    parser.add_option('-b', '--back',   action='store',dest='back',      type="string",  default=None,  help='background image (def: None)')
    parser.add_option('-t', '--target', action='store',dest='target',    type="string",  default=None,  help='destination folder')
    parser.add_option('-s', '--stride', action='store',dest='stride',    type="int",     default=3,     help='stride vectors (def=3)')
    parser.add_option('-v', '--var',    action='append',dest='var',      type="string",  default=None,  help='variable color-shaded (append)')
    parser.add_option('-n', '--num',    action='store',dest='numplot',   type="int",     default=2,     help='plot number (def=2)(<0: plot LT -*numplot*)')
    parser.add_option('-i', '--interp', action='store',dest='interp',    type="int",     default=None,  help='interpolation (2: p, 3: z-amr, 4:z-als)')
    parser.add_option('-c', '--color',  action='store',dest='colorb',    type="string",  default="def", help='change colormap (nobar: no colorbar)')
    parser.add_option('-x', '--no-vect',action='store_false',dest='winds',               default=True,  help='no wind vectors')
    parser.add_option('-m', '--min',    action='append',dest='vmin',     type="float",   default=None,  help='bounding minimum value (append)')    
    parser.add_option('-M', '--max',    action='append',dest='vmax',     type="float",   default=None,  help='bounding maximum value (append)') 
    parser.add_option('-T', '--tiled',  action='store_true',dest='tile',                 default=False, help='draw a tiled plot (no blank zone)')
    parser.add_option('-z', '--zoom',   action='store',dest='zoom',      type="float",   default=None,  help='zoom factor in %')
    parser.add_option('-N', '--no-api', action='store_true',dest='nocall',               default=False, help='do not recreate api file')
    parser.add_option('-d', '--display',action='store_false',dest='display',             default=True,  help='do not pop up created images')
    parser.add_option('-e', '--itstep', action='store',dest='itstep',    type="int",     default=None,  help='stride time (def=4)')
    parser.add_option('-H', '--hole',   action='store_true',dest='hole',                 default=False, help='holes above max and below min')
    parser.add_option('-S', '--save',   action='store',dest='save',      type="string",  default="gui", help='save mode (png,eps,svg,pdf or gui)(def=gui)')
    parser.add_option('-a', '--anomaly',action='store_true',dest='anomaly',              default=False, help='compute and plot relative anomaly in %')
    parser.add_option('-w', '--with',   action='store',dest='var2',      type="string",  default=None,  help='variable contoured')
    parser.add_option('--div',          action='store',dest='ndiv',      type="int",     default=10,    help='number of divisions in colorbar (def: 10)')
    parser.add_option('-F', '--first',  action='store',dest='first',     type="int",     default=1,     help='first subscript to plot (def: 1)')
    parser.add_option('--mult',         action='store',dest='mult',      type="float",   default=1.,    help='a multiplicative factor to plotted field')
    parser.add_option('--title',        action='store',dest='zetitle',   type="string",  default="fill",help='customize the whole title')
    #parser.add_option('-V', action='store', dest='comb',        type="float",   default=None,  help='a defined combination of variables')
    (opt,args) = parser.parse_args()
    if opt.namefile is None: 
        print "I want to eat one file at least ! Use winds.py -f name_of_my_file. Or type winds.py -h"
        exit()
    if opt.var is None and opt.anomaly is True:
        print "Cannot ask to compute anomaly if no variable is set"
        exit()    
    print "Options:", opt

    listvar = '' 
    if opt.var is None:
        zerange = [-999999]
    else:
        zelen = len(opt.var)
        zerange = range(zelen)
        #if zelen == 1: listvar = opt.var[0] + ','
        #else         : 
        for jjj in zerange: listvar += opt.var[jjj] + ','
        listvar = listvar[0:len(listvar)-1]
        vmintab = adjust_length (opt.vmin, zelen)  
        vmaxtab = adjust_length (opt.vmax, zelen)

    for i in range(len(opt.namefile)):

        zefile = opt.namefile[i]
        print zefile    
        zelevel = opt.nvert   
        stralt = None
        [lschar,zehour,zehourin] = getlschar ( zefile )  ## getlschar from wrfout (or simply return "" if another file)
    
        #####################################################
        ### Call Fortran routines for vertical interpolations
        if opt.interp is not None:
            if opt.nvert is 0 and opt.interp is 4:  zelevel = 0.010
            ### winds or no winds
            if opt.winds            :  zefields = 'uvmet'
            else                    :  zefields = ''
            ### var or no var
            #if opt.var is None      :  pass
            if zefields == ''       :  zefields = listvar 
            else                    :  zefields = zefields + "," + listvar 
            if opt.var2 is not None : zefields = zefields + "," + opt.var2  
            print zefields
            zefile = api_onelevel (  path_to_input   = '', \
                                     input_name      = zefile, \
                                     fields          = zefields, \
                                     interp_method   = opt.interp, \
                                     onelevel        = zelevel, \
                                     nocall          = opt.nocall )
            print zefile
            zelevel = 0 ## so that zelevel could play again the role of nvert

        if opt.var is None: zerange = [-999999]
        else:               zerange = range(zelen) 
        for jjj in zerange:
            if jjj == -999999: 
                argvar  = None
                argvmin = None
                argvmax = None
            else:
                argvar = opt.var[jjj]
                if vmintab[jjj] != -999999:  argvmin = vmintab[jjj]
                else:                        argvmin = None
                if vmaxtab[jjj] != -999999:  argvmax = vmaxtab[jjj] 
                else:                        argvmax = None
            #############
            ### Main call
            name = winds (zefile,int(zelevel),\
                proj=opt.proj,back=opt.back,target=opt.target,stride=opt.stride,var=argvar,\
                numplot=opt.numplot,colorb=opt.colorb,winds=opt.winds,\
                addchar=lschar,interv=[zehour,zehourin],vmin=argvmin,vmax=argvmax,\
                tile=opt.tile,zoom=opt.zoom,display=opt.display,\
                itstep=opt.itstep,hole=opt.hole,save=opt.save,\
                anomaly=opt.anomaly,var2=opt.var2,ndiv=opt.ndiv,first=opt.first,\
                mult=opt.mult,zetitle=opt.zetitle)
            print 'Done: '+name
            system("rm -f to_be_erased")
  
        #########################################################
        ### Generate a .sh file with the used command saved in it
        command = ""
        for arg in sys.argv: command = command + arg + ' '
        f = open(name+'.sh', 'w')
        f.write(command)
