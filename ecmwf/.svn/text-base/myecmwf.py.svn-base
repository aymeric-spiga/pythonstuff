def ecmwf_title_field (var):
	### http://www.ecmwf.int/services/archive/d/table/grib_table_2_versions
	### http://www.ecmwf.int/services/archive/d/parameters/mars=1/order=grib_parameter/table=128/
	### http://www.atmos.albany.edu/facstaff/rmctc/ecmwfGrib/ecmwfgrib128.tbl
	if   var == "151": name="Mean Sea Level Pressure (Pa)"          # ["151", "fc", "3", "sfc"]
	elif var == "146": name="Sensible Heat Flux (W m^-2)"           # ["146", "fc", "3", "sfc"]
	elif var == "130": name="Atmospheric Temperature (K)"           # ["130", "an", "0", "pl" ]
	elif var == "167": name="2m Atmospheric Temperature (K)"        # ["167", "fc", "3", "sfc"]
        elif var == "78":  name="Total column liquid water (kg/kg)"
        elif var == "137": name="Total column water vapour (kg/m2)"
        elif var == "189": name="Sunshine duration (s)"
        elif var == "228": name="Total precipitation (m)"
        else:              name=""
	return name

def split_char_add (var,add):
	import  numpy as np
	varchar = ""
	for i in range( np.array(var).size ):
		varchar = varchar + str(var[i]) + add + "/"
	return varchar

def split_char (var):
	varchar = split_char_add (var,"")
	return varchar

def get_ecmwf (var, fieldtype, wlat, wlon, lev, date, tim):
	from ecmwf 	import ECMWFDataServer
	from os		import system
	from netCDF4	import Dataset
	gbfile = 'output.grib'
	#ncfile = str(date[2]) + str(date[1]) + str(date[0]) + str(date[5]) + str(date[4]) + str(date[3])+'.nc'
        ncfile = 'output.nc'
        ######
        if fieldtype == "3d":    
            dataset = ["an","pl","0"]
        elif fieldtype == "2d":  
            dataset = ["fc","sfc","3"]
            lev = [9999.]
	######
	timchar = split_char (tim)
	levchar = split_char (lev)
	varchar = split_char_add (var,".128")
	##########################################################################
	## First registrer at http://data-portal.ecmwf.int/data/d/license/interim/
	## Then get your token at http://data-portal.ecmwf.int/data/d/token/interim_daily/
	server = ECMWFDataServer('http://data-portal.ecmwf.int/data/d/dataserver/','6948746482e9e3e29d64211e06329a2e','spiga@lmd.jussieu.fr')
	server.retrieve({
		'dataset'  : "interim_daily",
		'date'     : date[2] + date[1] + date[0] + "/to/" + date[5] + date[4] + date[3],
		'time'     : timchar,
		'step'     : dataset[2],
		'levtype'  : dataset[1],
		'type'     : dataset[0],
		'param'    : varchar,
		'levelist' : levchar,   
		'area'     : str(wlat[0])+"/"+str(wlon[0])+"/"+str(wlat[1])+"/"+str(wlon[1]),
		'target'   : gbfile
	})
	system("cdo -f nc copy "+gbfile+" "+ncfile+" ; rm -f "+gbfile)
	nc = Dataset(ncfile)
	#system("rm -f "+ncfile)
	return nc
