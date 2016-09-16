from __future__ import division
import matplotlib
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d
from scipy.interpolate import Rbf
import matplotlib as mpl
from pylab import *
import datetime as DT
import matplotlib.dates
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator
import math
plt.ion()


class AER():
        
        def __init__(self,filename):
            self.filename = filename
            self.arraypicker(filename)

	def ncdump(self, nc_fid, verb=True): 
            '''
	    ncdump outputs dimensions, variables and their attribute information.
	    The information is similar to that of NCAR's ncdump utility.
	    ncdump requires a valid instance of Dataset.

	    Parameters
	    ----------
	    nc_fid : netCDF4.Dataset
		A netCDF4 dateset object
	    verb : Boolean
		whether or not nc_attrs, nc_dims, and nc_vars are printed

	    Returns
	    -------
	    nc_attrs : list
		A Python list of the NetCDF file global attributes
	    nc_dims : list
		A Python list of the NetCDF file dimensions
	    nc_vars : list
		A Python list of the NetCDF file variables
	    '''
	    def print_ncattr(key):
		"""
		Prints the NetCDF file attributes for a given key

		Parameters
		----------
		key : unicode
		    a valid netCDF4.Dataset.variables key
		"""
		try:
		    print "\t\ttype:", repr(self.nc_fid.variables[key].dtype)
		    for ncattr in self.nc_fid.variables[key].ncattrs():
			print '\t\t%s:' % ncattr,\
			      repr(self.nc_fid.variables[key].getncattr(ncattr))
		except KeyError:
		    print "\t\tWARNING: %s does not contain variable attributes" % key

	    # NetCDF global attributes
	    nc_attrs = nc_fid.ncattrs()
	    if verb:
		print "NetCDF Global Attributes:"
		for nc_attr in nc_attrs:
		    print '\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr))
	    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
	    # Dimension shape information.
	    if verb:
		print "NetCDF dimension information:"
		for dim in nc_dims:
		    print "\tName:", dim 
		    print "\t\tsize:", len(nc_fid.dimensions[dim])
		    print_ncattr(dim)
	    # Variable information.
	    nc_vars = [var for var in self.nc_fid.variables]  # list of nc variables
	    if verb:
		print "NetCDF variable information:"
		for var in nc_vars:
		    if var not in nc_dims:
			print '\tName:', var
			print "\t\tdimensions:", self.nc_fid.variables[var].dimensions
			print "\t\tsize:", self.nc_fid.variables[var].size
			print_ncattr(var)
	    return nc_attrs, nc_dims, nc_vars




	def arraypicker(self,filename):
             self.nc_f = str(filename)
	     self.nc_fid = Dataset(self.nc_f, 'r') 
	     self.latitude = self.nc_fid.variables['latitude'][:]
	     self.latitude_edges = self.nc_fid.variables['latitude_edges'][:]
	     self.level = self.nc_fid.variables['level'][:]
	     self.level_edges = self.nc_fid.variables['level_edges'][:]
	     self.aerosol_bin = self.nc_fid.variables['aerosol_bin'][:]
	     self.bin_edges = self.nc_fid.variables['bin_edges'][:]
	#     date_charlength = self.nc_fid.variables['date_charlength'][:]
	     self.time = self.nc_fid.variables['time'][:]
	     self.day = self.nc_fid.variables['day'][:]
	     self.trop_height = self.nc_fid.variables['trop_height'][:]
	     self.date = self.nc_fid.variables['date'][:]
	     self.O1D = self.nc_fid.variables['O1D'][:]
	     self.O = self.nc_fid.variables['O'][:]
	     self.O2D = self.nc_fid.variables['O2D'][:]
	     self.H = self.nc_fid.variables['H'][:]
	     self.OH = self.nc_fid.variables['OH'][:]
	     self.HO2 = self.nc_fid.variables['HO2'][:]
	     self.H2O2 = self.nc_fid.variables['H2O2'][:]
	     self.MeO2 = self.nc_fid.variables['MEO2'][:]
	     self.MeOH = self.nc_fid.variables['MEOH'][:]
	     self.CH2O = self.nc_fid.variables['CH2O'][:]
	     self.I = self.nc_fid.variables['I'][:]
	     self.IO = self.nc_fid.variables['IO'][:]
	     self.I2 = self.nc_fid.variables['I2'][:]
	     self.I2O2 = self.nc_fid.variables['I2O2'][:]
	     self.HI = self.nc_fid.variables['HI'][:]
	     self.HOI = self.nc_fid.variables['HOI'][:]
	     self.INO = self.nc_fid.variables['INO'][:]
	     self.INO2 = self.nc_fid.variables['INO2'][:]
	     self.INO3 = self.nc_fid.variables['INO3'][:]
	     self.Cl = self.nc_fid.variables['CL'][:]
	     self.ClO= self.nc_fid.variables['CLO'][:]
	     self.HCl = self.nc_fid.variables['HCL'][:]
	     self.HOCl = self.nc_fid.variables['HOCL'][:]
	     self.ClONO2 = self.nc_fid.variables['CLNO3'][:]
	     self.ClO3 = self.nc_fid.variables['CLO3'][:]
	     self.OClO = self.nc_fid.variables['OCLO'][:]
	     self.ClOO = self.nc_fid.variables['CLOO'][:]
	     self.ClOOCl = self.nc_fid.variables['CL2O2'][:]
	     self.Cl2 = self.nc_fid.variables['CL2'][:]
	     self.ClNO2 = self.nc_fid.variables['CLNO2'][:]
	     self.N = self.nc_fid.variables['N'][:]
	     self.NO = self.nc_fid.variables['NO'][:]
	     self.NO2 = self.nc_fid.variables['NO2'][:]
	     self.NO3 = self.nc_fid.variables['NO3'][:]
	     self.N2O5 = self.nc_fid.variables['N2O5'][:]
	     self.HO2NO2 = self.nc_fid.variables['HO2NO2'][:]
	     self.HONO = self.nc_fid.variables['HONO'][:]
	     self.Br = self.nc_fid.variables['BR'][:]
	     self.BrO = self.nc_fid.variables['BRO'][:]
	     self.HBr = self.nc_fid.variables['HBR'][:]
	     self.HOBr = self.nc_fid.variables['HOBR'][:]
	     self.BrNO3 = self.nc_fid.variables['BRNO3'][:]
	     self.BrNO2 = self.nc_fid.variables['BRNO2'][:]
	     self.Br2 = self.nc_fid.variables['BR2'][:]
	     self.BrCl = self.nc_fid.variables['BRCL'][:]
	     self.EtHO2 = self.nc_fid.variables['ETHO2'][:]
	     self.EtHOH = self.nc_fid.variables['ETHOH'][:]
	     self.CH3CHO = self.nc_fid.variables['CH3CHO'][:]
	     self.CH3CO3H = self.nc_fid.variables['CH3CO3H'][:]
	     self.EtHO2NO2 = self.nc_fid.variables['ETHO2NO2'][:]
	     self.N2O = self.nc_fid.variables['N2O'][:]
	     self.CH4 = self.nc_fid.variables['CH4'][:]
	     self.C2H6 = self.nc_fid.variables['C2H6'][:]
	     self.H2 = self.nc_fid.variables['H2'][:]
	     self.CO = self.nc_fid.variables['CO'][:]
	     self.CH3Cl = self.nc_fid.variables['CH3CL'][:]
	     self.CCl4 = self.nc_fid.variables['CCL4'][:]
	     self.CFCl3 = self.nc_fid.variables['CFCL3'][:]
	     self.CF2Cl2  = self.nc_fid.variables['CF2CL2'][:]
	     self.CH3CCl3 = self.nc_fid.variables['CH3CCL3'][:]
	     self.CF2O = self.nc_fid.variables['CF2O'][:]
	     self.CH3Br = self.nc_fid.variables['CH3BR'][:]
	     self.CH2Br2 = self.nc_fid.variables['CH2BR2'][:]
	     self.CHBr3 = self.nc_fid.variables['CHBR3'][:]
	     self.CHClF2 = self.nc_fid.variables['CHCLF2'][:]
	     self.C2Cl3F3 = self.nc_fid.variables['C2CL3F3'][:]
	     self.C2Cl2F4 = self.nc_fid.variables['C2CL2F4'][:]
	     self.C2ClF5 = self.nc_fid.variables['C2CLF5'][:]
	     self.C2H3FCl2 = self.nc_fid.variables['C2H3FCL2'][:]
	     self.C2H3F2Cl = self.nc_fid.variables['C2H3F2CL'][:]
	     self.C2HF3Cl2 = self.nc_fid.variables['C2HF3CL2'][:]
	     self.CBrClF2 = self.nc_fid.variables['CBRCLF2'][:]
	     self.CBrF3 = self.nc_fid.variables['CBRF3'][:]
	     self.CBr2F2 = self.nc_fid.variables['CBR2F2'][:]
	     self.C2Br2F4 = self.nc_fid.variables['C2BR2F4'][:]
	     self.CH3I = self.nc_fid.variables['CH3I'][:]
	     self.CF3I = self.nc_fid.variables['CF3I'][:]
	     self.O3 = self.nc_fid.variables['O3'][:]
	     self.NOx = self.nc_fid.variables['NOX'][:]
	     self.Clx = self.nc_fid.variables['CLX'][:]
	     self.Brx = self.nc_fid.variables['BRX'][:]
	     self.Fx = self.nc_fid.variables['FX'][:]
	     self.Ix = self.nc_fid.variables['IX'][:]
	     self.PAN = self.nc_fid.variables['PAN'][:]
	     self.NOz = self.nc_fid.variables['NOZ'][:]
	     self.SHNO3 = self.nc_fid.variables['SHNO3']
	     self.HNO3 = self.nc_fid.variables['HNO3'][:]
	     self.H2O = self.nc_fid.variables['H2O'][:]
	     self.SH2O = self.nc_fid.variables['SH2O'][:]
	     self.ODP = self.nc_fid.variables['ODP'][:]
	     self.CS2 = self.nc_fid.variables['CS2'][:]
	     self.DMS = self.nc_fid.variables['DMS'][:]
	     self.H2S = self.nc_fid.variables['H2S'][:]
	     self.MSA = self.nc_fid.variables['MSA'][:]
	     self.OCS = self.nc_fid.variables['OCS'][:]
	     self.SO2 = self.nc_fid.variables['SO2'][:]
	     self.SO3 = self.nc_fid.variables['SO3'][:]
	     self.H2SO4 = self.nc_fid.variables['H2SO4'][:]
	     self.CH3CN = self.nc_fid.variables['CH3CN'][:]
	     self.HCN = self.nc_fid.variables['HCN'][:]
	     self.CO2 = self.nc_fid.variables['CO2'][:]
	     self.N2OPROD = self.nc_fid.variables['N2OPROD'][:]
	     self.N2OLLOS = self.nc_fid.variables['N2OLLOS'][:]
	     self.CH4PROD = self.nc_fid.variables['CH4PROD'][:]
	     self.CH4LLOS = self.nc_fid.variables['CH4LLOS'][:]
	     self.C2H6PROD = self.nc_fid.variables['C2H6PROD'][:]
	     self.C2H6LLOS = self.nc_fid.variables['C2H6LLOS'][:]
	     self.H2PROD = self.nc_fid.variables['H2PROD'][:]
	     self.H2LLOS = self.nc_fid.variables['H2LLOS'][:]
	     self.COPROD = self.nc_fid.variables['COPROD'][:]
	     self.COLLOS = self.nc_fid.variables['COLLOS'][:]
	     self.CH3ClPROD = self.nc_fid.variables['CH3CLPROD'][:]
	     self.CH3ClLLOS = self.nc_fid.variables['CH3CLLLOS'][:]
	     self.CCl4PROD = self.nc_fid.variables['CCL4PROD'][:]
	     self.CCl4LLOS = self.nc_fid.variables['CCL4LLOS'][:]
	     self.CFCl3PROD = self.nc_fid.variables['CFCL3PROD'][:]
	     self.CFCl3LLOS = self.nc_fid.variables['CFCL3LLOS'][:]
	     self.CF2Cl2PROD = self.nc_fid.variables['CF2CL2PROD'][:]
	     self.CF2Cl2LLOS = self.nc_fid.variables['CF2CL2LLOS'][:]
	     self.CH3CCl3PROD = self.nc_fid.variables['CH3CCL3PROD'][:]
	     self.CH3CCl3LLOS = self.nc_fid.variables['CH3CCL3LLOS'][:]
	     self.CF2OPROD = self.nc_fid.variables['CF2OPROD'][:]
	     self.CF2OLLOS = self.nc_fid.variables['CF2OLLOS'][:]
	     self.CH3BrPROD = self.nc_fid.variables['CH3BRPROD'][:]
	     self.CH3BrLLOS = self.nc_fid.variables['CH3BRLLOS'][:]
	     self.CH2Br2PROD = self.nc_fid.variables['CH2BR2PROD'][:]
	     self.CH2Br2LLOS = self.nc_fid.variables['CH2BR2LLOS'][:]
	     self.CHBr3PROD = self.nc_fid.variables['CHBR3PROD'][:]
	     self.CHBr3LLOS = self.nc_fid.variables['CHBR3LLOS'][:]
	     self.CHClF2LLOS = self.nc_fid.variables['CHCLF2LLOS'][:]
	     self.C2Cl3F3PROD = self.nc_fid.variables['C2CL3F3PROD'][:]
	     self.C2Cl3F3LLOS = self.nc_fid.variables['C2CL3F3LLOS'][:]
	     self.C2Cl2F4PROD = self.nc_fid.variables['C2CL2F4PROD'][:]
	     self.C2Cl2F4LLOS = self.nc_fid.variables['C2CL2F4LLOS'][:]
	     self.C2ClF5PROD = self.nc_fid.variables['C2CLF5PROD'][:]
	     self.C2ClF5LLOS = self.nc_fid.variables['C2CLF5LLOS'][:]
	     self.C2H3FCl2PROD = self.nc_fid.variables['C2H3FCL2PROD'][:]
	     self.C2H3FCl2LLOS = self.nc_fid.variables['C2H3FCL2PROD'][:]
	     self.C2H3F2ClPROD = self.nc_fid.variables['C2H3F2CLPROD'][:]
	     self.C2H3F2ClLLOS = self.nc_fid.variables['C2H3F2CLLLOS'][:]
	     self.C2HF3Cl2PROD = self.nc_fid.variables['C2HF3CL2PROD'][:]
	     self.C2HF3Cl2LLOS = self.nc_fid.variables['C2HF3CL2LLOS'][:]
	     self.CBrClF2PROD = self.nc_fid.variables['CBRCLF2PROD'][:]
	     self.CBrClF2LLOS = self.nc_fid.variables['CBRCLF2LLOS'][:]
	     self.CBrF3PROD = self.nc_fid.variables['CBRF3PROD'][:]
	     self.CBrF3LLOS = self.nc_fid.variables['CBRF3LLOS'][:]
	     self.CBr2F2PROD = self.nc_fid.variables['CBR2F2PROD'][:]
	     self.CBr2F2LLOS = self.nc_fid.variables['CBR2F2LLOS'][:]
	     self.C2Br2F4PROD = self.nc_fid.variables['C2BR2F4PROD'][:]
	     self.C2Br2F4LLOS = self.nc_fid.variables['C2BR2F4LLOS'][:]
	     self.CH3IPROD = self.nc_fid.variables['CH3IPROD'][:]
	     self.CHEILLOS = self.nc_fid.variables['CH3ILLOS'][:]
	     self.CH3IPROD = self.nc_fid.variables['CH3IPROD'][:]
	     self.CH3ILLOS = self.nc_fid.variables['CH3ILLOS'][:]
	     self.CF3IPROD = self.nc_fid.variables['CH3IPROD'][:]
	     self.CF3ILLOS = self.nc_fid.variables['CF3ILLOS'][:]
	     self.O3PROD = self.nc_fid.variables['O3PROD'][:]
	     self.O3LLOS = self.nc_fid.variables['O3LLOS'][:]
	     self.O3QLOS = self.nc_fid.variables['O3QLOS'][:]
	     self.NOxPROD = self.nc_fid.variables['NOXPROD'][:]
	     self.NOxLLOS = self.nc_fid.variables['NOXLLOS'][:]
	     self.ClxPROD = self.nc_fid.variables['CLXPROD'][:]
	     self.ClxLLOS = self.nc_fid.variables['CLXLLOS'][:]
	     self.BrxPROD = self.nc_fid.variables['BRXPROD'][:]
	     self.BrxLLOS = self.nc_fid.variables['BRXLLOS'][:]
	     self.FxPROD = self.nc_fid.variables['FXPROD'][:]
	     self.FxLLOS = self.nc_fid.variables['FXLLOS'][:]
	     self.IxPROD = self.nc_fid.variables['IXPROD'][:]
	     self.IxLLOS = self.nc_fid.variables['IXLLOS'][:]
	     self.PANPROD = self.nc_fid.variables['PANPROD'][:]
	     self.PANLLOS = self.nc_fid.variables['PANLLOS'][:]
	     self.NOzPROD = self.nc_fid.variables['NOZPROD'][:]
	     self.NOzLLOS = self.nc_fid.variables['NOZLLOS'][:]
	     self.NOzQLOS = self.nc_fid.variables['NOZQLOS'][:]
	     self.SHNO3PROD = self.nc_fid.variables['SHNO3PROD'][:]
	     self.SHNO3LLOS = self.nc_fid.variables['SHNO3LLOS'][:]
	     self.HNO3PROD = self.nc_fid.variables['HNO3PROD'][:]
	     self.HNO3LLOS = self.nc_fid.variables['HNO3LLOS'][:]
	     self.H2OPROD = self.nc_fid.variables['H2OPROD'][:]
	     self.H2OLLOS = self.nc_fid.variables['H2OLLOS'][:]
	     self.H2OQLOS = self.nc_fid.variables['H2OQLOS'][:]
	     self.SH2OPROD = self.nc_fid.variables['SH2OPROD'][:]
	     self.SH2OLLOS = self.nc_fid.variables['SH2OLLOS'][:]
	     self.ODPPROD = self.nc_fid.variables['ODPPROD'][:]
	     self.ODPLLOS = self.nc_fid.variables['ODPLLOS'][:]
	     self.CS2PROD = self.nc_fid.variables['CS2PROD'][:]
	     self.CS2LLOS = self.nc_fid.variables['CS2LLOS'][:]
	     self.DMSPROD = self.nc_fid.variables['DMSPROD'][:]
	     self.DMSLLOS = self.nc_fid.variables['DMSLLOS'][:]
	     self.H2SPROD = self.nc_fid.variables['H2SPROD'][:]
	     self.H2SLLOS = self.nc_fid.variables['H2SLLOS'][:]
	     self.MSAPROD = self.nc_fid.variables['MSAPROD'][:]
	     self.MSALLOS = self.nc_fid.variables['MSALLOS'][:]
	     self.OCSPROD = self.nc_fid.variables['OCSPROD'][:]
	     self.OCSLLOS = self.nc_fid.variables['OCSLLOS'][:]
	     self.SO2PROD = self.nc_fid.variables['SO2PROD'][:]
	     self.SO2LLOS = self.nc_fid.variables['SO2LLOS'][:]
	     self.SO3PROD = self.nc_fid.variables['SO3PROD'][:]
	     self.SO3LLOS = self.nc_fid.variables['SO3LLOS'][:]
	     self.H2SO4PROD = self.nc_fid.variables['H2SO4PROD'][:]
	     self.H2SO4LLOS = self.nc_fid.variables['H2SO4LLOS'][:]
	     self.CH3CNPROD = self.nc_fid.variables['CH3CNPROD'][:]
	     self.CH3CNLLOS = self.nc_fid.variables['CH3CNLLOS'][:]
	     self.HCNPROD = self.nc_fid.variables['HCNPROD'][:]
	     self.O3COLUMN = self.nc_fid.variables['O3COLUMN'][:]
	     self.AEROSOL = self.nc_fid.variables['AEROSOL'][:]
	     self.TEMPERATURE = self.nc_fid.variables['TEMPERATURE'][:]
	     self.SURFACE_AREA = self.nc_fid.variables['SURFACE_AREA'][:]
	     self.AEROSOL_MASS = self.nc_fid.variables['AEROSOL_MASS'][:]
	     self.AEROSOL_SULFATE = self.nc_fid.variables['AEROSOL_SULFATE'][:]
	     self.TOTAL_PARTICLES = self.nc_fid.variables['TOTAL_PARTICLES'][:]
	     self.PARTICLES_001um = self.nc_fid.variables['PARTICLES_0.01um'][:]
	     self.PARTICLES_015um = self.nc_fid.variables['PARTICLES_0.15um'][:]
	     self.EFFECTIVE_RADIUS = self.nc_fid.variables['EFFECTIVE_RADIUS'][:]
	     self.BVP = self.nc_fid.variables['BVP'][:]
	     self.WEIGHT_PERCENT = self.nc_fid.variables['WEIGHT_PERCENT'][:]
	     self.DENSITY = self.nc_fid.variables['DENSITY'][:]
	     self.AIRVD = self.nc_fid.variables['AIRVD'][:]
             for x in range(len(self.day)):
                  self.day[x] = self.day[x] + 365*math.floor(x/13)
             self.template = np.zeros((int(len(self.day)/13),14))
             self.template = self.template.tolist()
             self.dayz = self.template
 	     for x in range(int(len(self.day)/13)):
                  for y in range(14):
                       self.dayz[x][y] = self.day[np.add(range(14),x*13)[y]]
             
        def  varmulator(self, var): #returns array of dimensions [year][14]
             varz = np.zeros_like(self.template)
             varz = varz.tolist()
             for x in range(int(len(var)/13)):
                 for y in range(14):
                     varz[x][y] = var[np.add(range(14),x*13)[y]]
             return varz

        def  differencecalculator(self, vara, varb): #will return the difference array between given variables (varb - vara)/ vara * 100
             difference = np.zeros_like(self.template)
             difference = np.multiply(np.divide(np.subtract(varb,vara),vara),100)
             return difference
                  
        def  columnator(self, var):  #returns column matrix of dimensions (daybins, latbins)         
#             columns = np.zeros_like(self.O3COLUMN)
#             tropheights = np.zeros_like(self.O3COLUMN)
#             pressure = np.zeros_like(self.level)
#             midpressure = np.zeros_like(self.level)
#             temperature = np.zeros_like(self.O3COLUMN)
#             airvd = np.zeros_like(self.O3COLUMN)
#             columns = columns.tolist()
#             tropheights = tropheights.tolist()
#             pressure = pressure.tolist()
#             temperature = temperature.tolist()
#             airvd = airvd.tolist()
#       
#             for x in range(len(self.trop_height)):
#                 for y in range(len(self.trop_height[x])):
#                     tropheights[x][y] = self.trop_height[x][y]
#             for x in range(len(self.temperature)):
#                 for y in range(len(self.temperature)):             




#             for x in range(len(var)):
 #                for y in range(len(var[x][0])):
  #                   columns[x][y] =var[x][y][(tropheights[x][y] ):].sum() 
  #           return columns
              return 0

        def comparator(self,var, varstring, year1, year2, x1=0, x2=18, y1=0,y2=13, yr = 1991):
	     dayt = [self.day[x] for x in range(int(y1),int(y2))]
	     if dayt[-1] == 0:
		  dayt[-1] = 365
             varz = self.columnator(var)
             varz = self.varmulator(varz)
             o3diff = self.differencecalculator(varz[year2],varz[year1])
#             o3diff = np.multiply(np.divide(np.subtract(varz[year1], varz[year2]),varz[year1]),100)
             o3col = np.zeros(((int(x2)-int(x1)),(int(y2)-int(y1))))
             for x in range(int(x2) - int(x1)):
                  o3col[x] = [o3diff[y][x+int(x1)] for y in range(int(y1),int(y2))]
	     numcolors = len(range(0, (int(x2)-int(x1)+1)))
	     colors = get_cmap('coolwarm')
	     colorlevels = []
	     for i in range(numcolors):
		  colorlevels.append(colors(1.*i/numcolors))
	     fig= plt.figure()
	     gs = gridspec.GridSpec(2,1, height_ratios=[5,1])
	     ax = plt.subplot(gs[0])
	     ax1 = plt.subplot(gs[1])
	     ax.set_color_cycle(colorlevels)
	     fig.set_facecolor('white')
	     f = []
	     f.append( [interp1d(dayt, o3col[x], kind = 'cubic') for x in range(int(x2) - int(x1))])
	     xnew = np.linspace(dayt[0],dayt[-1],100)
	     o3colnew = np.zeros(((int(x2)-int(x1)),100))
	     dayyt = xnew
	     dayyt = np.divide(dayyt,365)
	     dayyt = np.add(dayyt, int(yr))
	     datte = []
	     for x in range(len(dayyt)):
		  datte.append(at2dt(dayyt[x]))

	     for x in range(0, len(f[0])):
		  o3colnew[x] = f[0][x](xnew)
	     [ax.plot(datte,o3colnew[x], linewidth = 2) for x in range(0,len(o3colnew))]
	     ax.set_ylabel('%change - total stratospheric column ', fontsize = 20)
	     labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']     
	     labels = labels[int(y1):int(y2)+1]
	     ax.set_xticklabels(labels,rotation=30, ha='right') # ha is the same as horizontalalignment
	     ax.set_title('Variation in'+ varstring + ' Column', fontsize = 25)
	#     ax.set_xlim(datte[int(y1)],datte[int(y2)])
	     ax.grid(which='both')
	     ax.yaxis.set_minor_locator(AutoMinorLocator(5))
	     vals = ax.get_yticks()
	     ax.set_yticklabels(['{:.0%}'.format(x/100) for x in vals])
	#     fig.autofmt_xdate()i
	     cmap = mpl.colors.ListedColormap(colorlevels)
	     bounds = []
	     bounds.append([self.latitude_edges[x] for x in range(int(x1),int(x2)+2)])
	     bounds = bounds[0]
	     boundsy=[]
	     boundsy.append([myround(x,5) for x in bounds])
	     bounds = boundsy[0] 
	     vmin = self.latitude_edges[int(x1)]
	     vmax = self.latitude_edges[int(x2)+1]
	     norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	     cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm,ticks = bounds,spacing = 'uniform', orientation = 'horizontal')
	     cb1.set_label('Latitude (degrees)', fontsize = 20)


        def o3comparator(self, year1, year2, x1=0, x2=18, y1=0,y2=13, yr = 1991):
	     dayt = [self.day[x] for x in range(int(y1),int(y2))]
	     if dayt[-1] == 0:
		  dayt[-1] = 365
             varz = self.varmulator(self.O3COLUMN)
#             for x in range(int(len(self.O3COLUMN)/13)):
#                 for y in range(14):
#                      varz[x][y] = self.O3COLUMN[nip.add(range(14),x*13)[y]] 
#             o3diff = np.multiply(np.divide(np.subtract(varz[year1], varz[year2]),varz[year1]),100)
             o3diff = self.differencecalculator(varz[year2],varz[year1])
             o3col = np.zeros(((int(x2)-int(x1)),(int(y2)-int(y1))))
             for x in range(int(x2) - int(x1)):
                  o3col[x] = [o3diff[y][x+int(x1)] for y in range(int(y1),int(y2))]
	     numcolors = len(range(0, (int(x2)-int(x1)+1)))
	     colors = get_cmap('coolwarm')
	     colorlevels = [] 
	     for i in range(numcolors):
		  colorlevels.append(colors(1.*i/numcolors))
	     fig= plt.figure()
	     gs = gridspec.GridSpec(2,1, height_ratios=[5,1])
	     ax = plt.subplot(gs[0])
	     ax1 = plt.subplot(gs[1])
	     ax.set_color_cycle(colorlevels)
	     fig.set_facecolor('white')
	     f = []
	     f.append( [interp1d(dayt, o3col[x], kind = 'cubic') for x in range(int(x2) - int(x1))])
	     xnew = np.linspace(dayt[0],dayt[-1],100)
	     o3colnew = np.zeros(((int(x2)-int(x1)),100))
	     dayyt = xnew
	     dayyt = np.divide(dayyt,365)
	     dayyt = np.add(dayyt, int(yr))
	     datte = []
	     for x in range(len(dayyt)):
		  datte.append(at2dt(dayyt[x]))

	     for x in range(0, len(f[0])):
		  o3colnew[x] = f[0][x](xnew)
	     [ax.plot(datte,o3colnew[x], linewidth = 2) for x in range(0,len(o3colnew))]
	     ax.set_ylabel('%change - total column ozone (DU)', fontsize = 20)
	     labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']     
	     labels = labels[int(y1):int(y2)+1]
	     ax.set_xticklabels(labels,rotation=30, ha='right') # ha is the same as horizontalalignment
	     ax.set_title('Variation in Column Ozone: ' + str(year1) +  ' vs ' + str(year2) + ' - ' +str(self.filename), fontsize = 25)
	#     ax.set_xlim(datte[int(y1)],datte[int(y2)])
	     ax.grid(which='both')
	     ax.yaxis.set_minor_locator(AutoMinorLocator(5))
	     vals = ax.get_yticks()
	     ax.set_yticklabels(['{:.0%}'.format(x/100) for x in vals])
	#     fig.autofmt_xdate()i
	     cmap = mpl.colors.ListedColormap(colorlevels)
	     bounds = []
	     bounds.append([self.latitude_edges[x] for x in range(int(x1),int(x2)+2)])
	     bounds = bounds[0]
	     boundsy=[]
	     boundsy.append([myround(x,5) for x in bounds])
	     bounds = boundsy[0] 
	     vmin = self.latitude_edges[int(x1)]
	     vmax = self.latitude_edges[int(x2)+1]
	     norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	     cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm,ticks = bounds,spacing = 'uniform', orientation = 'horizontal')
	     cb1.set_label('Latitude (degrees)', fontsize = 20)


	def  contourplotter(self, var,dayt,year,num,flag =0, varstring = '' ):
	     global ax, fig, CS, CS2 
	     fig, ax = plt.subplots()
	     plt.yscale('log', nonposy='clip')
	     #x , y = np.meshgrid(latitude, level)
	     #latnew = np.linspace(latitude[0],latitude[-1],100)
	     #levnew = np.logspace(np.log(level[0]), np.log(level[-1]), 100,base= np.e)
	     #X,Y = np.meshgrid(latnew, levnew)
	     #f = Rbf(x,y, var[int(day)], function='gaussian') 
	     #Z = f(X,Y)
	     X,Y = np.meshgrid(self.latitude, self.level)
             varz = self.varmulator(var)
#             varz = self.template
#             varz = varz.tolist()
#             for x in range(int(len(var)/13)):
#                 for y in range(14):
#                     varz[x][y] = var[np.add(range(14),x*13)[y]]
	     Z = varz[int(year)][int(dayt)]
	     levels = np.linspace(Z.min()-(Z.min() /10), Z.max()+(Z.max()/10), int(num))
	     if flag == 1:
		   CS = plt.contourf(X,Y,Z,levels ,cmap = plt.cm.bone_r)
	     if flag == 2: 
		   CS = plt.contourf(X,Y,Z,levels ,cmap = plt.cm.bone_r)
		   CS2 = plt.contour(CS,levels=CS.levels[::2], colors = 'k', hold='on')
	     if flag == 0:
		   CS = plt.contour(X,Y,Z,levels, colors = 'k')
	     
	     ax.invert_yaxis()
	     ax.set_xlabel('latitude (degrees)', fontsize = 20)
	     ax.set_ylabel('pressure (hPa)', fontsize = 20)
	     ax.set_title(varstring + ' Contour Plot - Day:  ' + str(int(self.dayz[year][dayt])), fontsize = 25)
	     ax.grid(which='both', color = 'black', linewidth = 0.5)
	     f = interp1d(self.latitude, self.level[self.trop_height[int(dayt)]], kind = 'cubic')
	     xnew = np.linspace(self.latitude[0], self.latitude[-1],1000)
	     ynew = f(xnew)
	#     l, = ax.plot(xnew,ynew,'k-', dashes=[8,4,2,4,2,4],lw=2)
	#     ll, = ax.plot(xnew[320:-1],ynew[320:-1],'y', dashes=[8,4,2,4,2,4],lw=8)
	#     line_string= 'tropopause'
	#     pos = [(xnew[-200]+xnew[-1])/2., (ynew[-200]+ynew[-1])/2.]
	#     xscreen = ax.transData.transform(zip(xnew[-200::],ynew[-200::]))
	#     rot = np.rad2deg(np.arctan2(*np.abs(np.gradient(xscreen)[0][0][::-1])))
	#     rot = 0
	#     ltex = plt.text(pos[0]-10, pos[1]+45, line_string, size=20, rotation=rot, verticalalignment='center', color = l.get_color(), ha="center", va="center",bbox = dict(ec='none' ,fc='none'))
	     fig.set_facecolor('white')
	     plt.yticks([900,800,700,600,500,400,300,200,100,50, 10, 5, 1, 0.5])
	     plt.gca().set_yticklabels([900,800,700,600,500,400,300,200,100,50, 10 ,5, 1, 0.5])
	     plt.xticks([-85, -55, -25, 0, 25, 55, 85 ])
	     plt.gca().set_xticklabels([-90, -60, -30, 0, 30, 60, 90])
	     if flag ==1:
		  cbar = plt.colorbar(CS, format='%.0e')
		  cbar.ax.set_ylabel('mixing ratio')
		  l, = ax.plot(xnew,ynew,'y-', dashes=[8,4,2,4,2,4],lw=2)

	     if flag ==2:
		  cbar = plt.colorbar(CS, format='%.0e')
		  cbar.ax.set_ylabel('mixing ratio')
		  cbar.add_lines(CS2)
		  l, = ax.plot(xnew,ynew,'y-', dashes=[8,4,2,4,2,4],lw=2)

	     if flag ==0:
		  plt.clabel(CS, inline=1, inline_spacing=6 , colors = 'k', fmt = '%.0e', fontsize = 20) 
		  l, = ax.plot(xnew,ynew,'k-', dashes=[8,4,2,4,2,4],lw=2)
	 #     ll, = ax.plot(xnew[320:-1],ynew[320:-1],'y', dashes=[8,4,2,4,2,4],lw=8)
	     line_string= 'tropopause'
	     pos = [(xnew[-200]+xnew[-1])/2., (ynew[-200]+ynew[-1])/2.]
	     xscreen = ax.transData.transform(zip(xnew[-200::],ynew[-200::]))
	#     rot = np.rad2deg(np.arctan2(*np.abs(np.gradient(xscreen)[0][0][::-1])))
	     rot = 0
	     ltex = plt.text(pos[0]-10, pos[1]+45, line_string, size=20, rotation=rot, verticalalignment='center', color = l.get_color(),ha="center", va="center",bbox = dict(ec='none' ,fc='none'))



	def o3columns(self,year, x1=0,x2=18,y1=0,y2=13): #x values are latitude, y values are day

	     dayt = [self.day[x] for x in range(int(y1),int(y2))]
	     if dayt[-1] == 0:
		  dayt[-1] = 365
             varz = self.varmulator(self.O3COLUMN) 
#             varz = self.template
#             varz = varz.tolist()
#             for x in range(int(len(self.O3COLUMN)/13)):
#                  for y in range(14):
#                      varz[x][y] = self.O3COLUMN[np.add(range(14),x*13)[y]]	     
	     o3col = np.zeros(((int(x2)-int(x1)),(int(y2)-int(y1))))
	     for x in range(int(x2) - int(x1)):
	          o3col[x] = [varz[year][y][x+int(x1)] for y in range(int(y1),int(y2))]
	     numcolors = len(range(0, (int(x2)-int(x1)+1)))
	     colors = get_cmap('coolwarm')
	     colorlevels = [] 
	     for i in range(numcolors):
		  colorlevels.append(colors(1.*i/numcolors))
	     fig= plt.figure()
	     gs = gridspec.GridSpec(2,1, height_ratios=[5,1])
	     ax = plt.subplot(gs[0])
	     ax1 = plt.subplot(gs[1])
	     ax.set_color_cycle(colorlevels)
	     fig.set_facecolor('white')
	     f = []
	     f.append( [interp1d(dayt, o3col[x], kind = 'cubic') for x in range(int(x2) - int(x1))])
	     xnew = np.linspace(dayt[0],dayt[-1],100)
	     o3colnew = np.zeros(((int(x2)-int(x1)),100))
	     dayyt = xnew
	     dayyt = np.divide(dayyt,365)
	     dayyt = np.add(dayyt, 2004)
	     datte = []
	     for x in range(len(dayyt)):
		  datte.append(self.t2dt(dayyt[x]))

	     for x in range(0, len(f[0])):
		  o3colnew[x] = f[0][x](xnew)
	     [ax.plot(datte,o3colnew[x], linewidth = 2) for x in range(0,len(o3colnew))]
	     ax.set_ylabel('total column ozone (DU)', fontsize = 20)
	     labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
             labels = labels[int(y1):int(y2)+1]     
	     ax.set_xticklabels(labels,rotation=30, ha='right') # ha is the same as horizontalalignment
	     ax.set_title('Seasonal Variation in Column Ozone', fontsize = 25)
#	     ax.set_xlim(datte[int(y1)],datte[int(y2)])
	#     fig.autofmt_xdate()
             ax.set_ylim(0,400)
	     cmap = mpl.colors.ListedColormap(colorlevels)
	     bounds = []
	     bounds.append([self.latitude_edges[x] for x in range(int(x1),int(x2)+2)])
	     bounds = bounds[0]
	     boundsy=[]
	     boundsy.append([self.myround(x,5) for x in bounds])
	     bounds = boundsy[0] 
	     vmin = self.latitude_edges[int(x1)]
	     vmax = self.latitude_edges[int(x2)+1]
	     norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	     cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm,ticks = bounds,spacing = 'uniform', orientation = 'horizontal')
	     cb1.set_label('Latitude (degrees)', fontsize = 20)
	     cb1.ax.set_xticklabels(bounds, rotation=90)
	def t2dt(self, atime):
	    """
	    Convert atime (a float) to DT.datetime
	    This is the inverse of dt2t.
	    assert dt2t(t2dt(atime)) == atime
	    """
	    year = int(atime)
	    remainder = atime - year
	    boy = DT.datetime(year, 1, 1)
	    eoy = DT.datetime(year + 1, 1, 1)
	    seconds = remainder * (eoy - boy).total_seconds()
	    return boy + DT.timedelta(seconds=seconds)

	def dt2t(self, adatetime):
	    """
	    Convert adatetime into a float. The integer part of the float should
	    represent the year.
	    Order should be preserved. If adate<bdate, then d2t(adate)<d2t(bdate)
	    time distances should be preserved: If bdate-adate=ddate-cdate then
	    dt2t(bdate)-dt2t(adate) = dt2t(ddate)-dt2t(cdate)
	    """
	    year = adatetime.year
	    boy = DT.datetime(year, 1, 1)
	    eoy = DT.datetime(year + 1, 1, 1)
	    return year + ((adatetime - boy).total_seconds() / ((eoy - boy).total_seconds()))


        def myround(self, n, m):
		r = n % m
		return n + m - r if r + r >= m else n - r
        
#        def o3comparator(self, year1, year2, x1=0, x2=18, y1=0,y2=13, yr = 1991):
#	     dayt = [self.day[x] for x in range(int(y1),int(y2))]
#	     if dayt[-1] == 0:
#		  dayt[-1] = 365
#             varz = self.template
#             varz = self.varmulator(self.O3COLUMN) 
#             o3diff = self.differencecalculator(varz[year2],varz[year1])
#             o3col = np.zeros(((int(x2)-int(x1)),(int(y2)-int(y1))))
#             for x in range(int(x2) - int(x1)):
#                  o3col[x] = [o3diff[y][x+int(x1)] for y in range(int(y1),int(y2))]
#	     numcolors = len(range(0, (int(x2)-int(x1)+1)))
#	     colors = get_cmap('coolwarm')
#	     colorlevels = [] 
#	     for i in range(numcolors):
#		  colorlevels.append(colors(1.*i/numcolors))
#	     fig= plt.figure()
#	     gs = gridspec.GridSpec(2,1, height_ratios=[5,1])
#	     ax = plt.subplot(gs[0])
#	     ax1 = plt.subplot(gs[1])
#	     ax.set_color_cycle(colorlevels)
#	     fig.set_facecolor('white')
#	     f = []
#	     f.append( [interp1d(dayt, o3col[x], kind = 'cubic') for x in range(int(x2) - int(x1))])
#	     xnew = np.linspace(dayt[0],dayt[-1],100)
#	     o3colnew = np.zeros(((int(x2)-int(x1)),100))
#	     dayyt = xnew
#	     dayyt = np.divide(dayyt,365)
#	     dayyt = np.add(dayyt, int(yr))
#	     datte = []
#	     for x in range(len(dayyt)):
#		  datte.append(at2dt(dayyt[x]))
#
#	     for x in range(0, len(f[0])):
#		  o3colnew[x] = f[0][x](xnew)
#	     [ax.plot(datte,o3colnew[x], linewidth = 2) for x in range(0,len(o3colnew))]
#	     ax.set_ylabel('%change - total column ozone (DU)', fontsize = 20)
#	     labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']     
#	     labels = labels[int(y1):int(y2)+1]
#	     ax.set_xticklabels(labels,rotation=30, ha='right') # ha is the same as horizontalalignment
#	     ax.set_title('Variation in Column Ozone', fontsize = 25)
#	#     ax.set_xlim(datte[int(y1)],datte[int(y2)])
#	     ax.grid(which='both')
#	     ax.yaxis.set_minor_locator(AutoMinorLocator(5))
#	     vals = ax.get_yticks()
#	     ax.set_yticklabels(['{:.0%}'.format(x/100) for x in vals])
#	#     fig.autofmt_xdate()i
#	     cmap = mpl.colors.ListedColormap(colorlevels)
#	     bounds = []
#	     bounds.append([self.latitude_edges[x] for x in range(int(x1),int(x2)+2)])
#	     bounds = bounds[0]
#	     boundsy=[]
#	     boundsy.append([myround(x,5) for x in bounds])
#	     bounds = boundsy[0] 
#	     vmin = self.latitude_edges[int(x1)]
#	     vmax = self.latitude_edges[int(x2)+1]
#	     norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
#	     cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm,ticks = bounds,spacing = 'uniform', orientation = 'horizontal')
#	     cb1.set_label('Latitude (degrees)', fontsize = 20)



def no3comparator(moda,modb,year1,x1=0,x2=18,y1=0,y2=13,yr=1991): #x values are latitude, y values are day
     varz = np.zeros((int(len(moda.day)/13),14))
     dayt = [moda.day[x] for x in range(int(y1),int(y2))]
     if dayt[-1] == 0:
	  dayt[-1] = 365
     vara = varz.tolist()
     varb = varz.tolist()
     for x in range(int(len(moda.day)/13)):
         for y in range(14):
             vara[x][y] = moda.O3COLUMN[np.add(range(14),x*13)[y]]
             varb[x][y] = modb.O3COLUMN[np.add(range(14),x*13)[y]]
     o3diff = np.multiply(np.divide(np.subtract(vara[year1], varb[year1]),vara[year1]),100)
     o3col = np.zeros(((int(x2)-int(x1)),(int(y2)-int(y1))))
     for x in range(int(x2)-int(x1)):
	  o3col[x] = [o3diff[y][x+int(x1)] for y in range(int(y1),int(y2))]
     numcolors = len(range(0, (int(x2)-int(x1)+1)))
     colors = get_cmap('coolwarm')
     colorlevels = [] 
     for i in range(numcolors):
	  colorlevels.append(colors(1.*i/numcolors))
     fig= plt.figure()
     gs = gridspec.GridSpec(2,1, height_ratios=[5,1])
     ax = plt.subplot(gs[0])
     ax1 = plt.subplot(gs[1])
     ax.set_color_cycle(colorlevels)
     fig.set_facecolor('white')
     f = []
     f.append( [interp1d(dayt, o3col[x], kind = 'cubic') for x in range(int(x2) - int(x1))])
     xnew = np.linspace(dayt[0],dayt[-1],100)
     o3colnew = np.zeros(((int(x2)-int(x1)),100))
     dayyt = xnew
     dayyt = np.divide(dayyt,365)
     dayyt = np.add(dayyt, int(yr))
     datte = []
     for x in range(len(dayyt)):
	  datte.append(at2dt(dayyt[x]))

     for x in range(0, len(f[0])):
	  o3colnew[x] = f[0][x](xnew)
     [ax.plot(datte,o3colnew[x], linewidth = 2) for x in range(0,len(o3colnew))]
     ax.set_ylabel('%change - total column ozone (DU)', fontsize = 20)
     labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']     
     labels = labels[int(y1):int(y2)+1]
     ax.set_xticklabels(labels,rotation=30, ha='right') # ha is the same as horizontalalignment
     ax.set_title('Variation in Column Ozone', fontsize = 25)
#     ax.set_xlim(datte[int(y1)],datte[int(y2)])
     ax.grid(which='both')
     ax.yaxis.set_minor_locator(AutoMinorLocator(5))
     vals = ax.get_yticks()
     ax.set_yticklabels(['{:.0%}'.format(x/100) for x in vals])
#     fig.autofmt_xdate()i
     cmap = mpl.colors.ListedColormap(colorlevels)
     bounds = []
     bounds.append([moda.latitude_edges[x] for x in range(int(x1),int(x2)+2)])
     bounds = bounds[0]
     boundsy=[]
     boundsy.append([myround(x,5) for x in bounds])
     bounds = boundsy[0] 
     vmin = moda.latitude_edges[int(x1)]
     vmax = moda.latitude_edges[int(x2)+1]
     norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
     cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm,ticks = bounds,spacing = 'uniform', orientation = 'horizontal')
     cb1.set_label('Latitude (degrees)', fontsize = 20)
     cb1.ax.set_xticklabels(bounds, rotation=90)
def at2dt(atime):
    """
    Convert atime (a float) to DT.datetime
    This is the inverse of dt2t.
    assert dt2t(t2dt(atime)) == atime
    """
    year = int(atime)
    remainder = atime - year
    boy = DT.datetime(year, 1, 1)
    eoy = DT.datetime(year + 1, 1, 1)
    seconds = remainder * (eoy - boy).total_seconds()
    return boy + DT.timedelta(seconds=seconds)

def adt2t(adatetime):
    """
    Convert adatetime into a float. The integer part of the float should
    represent the year.
    Order should be preserved. If adate<bdate, then d2t(adate)<d2t(bdate)
    time distances should be preserved: If bdate-adate=ddate-cdate then
    dt2t(bdate)-dt2t(adate) = dt2t(ddate)-dt2t(cdate)
    """
    year = adatetime.year
    boy = DT.datetime(year, 1, 1)
    eoy = DT.datetime(year + 1, 1, 1)
    return year + ((adatetime - boy).total_seconds() / ((eoy - boy).total_seconds()))


def myround(n, m):
	r = n % m
	return n + m - r if r + r >= m else n - r

def  contourcomparator(a,moda,modb,dayt,num,flag =0, varstring = '' ): 
     global Z
     fig, ax = plt.subplots()
     plt.yscale('log', nonposy='clip')
     #x , y = np.meshgrid(latitude, level)
     #latnew = np.linspace(latitude[0],latitude[-1],100)
     #levnew = np.logspace(np.log(level[0]), np.log(level[-1]), 100,base= np.e)
     #X,Y = np.meshgrid(latnew, levnew)
     #f = Rbf(x,y, var[int(day)], function='gaussian') 
     #Z = f(X,Y)
     X,Y = np.meshgrid(a.latitude, a.level)
     Z =np.dot(np.divide(np.subtract(modb[int(dayt)],moda[int(dayt)]),moda[(dayt)]),100)
     levels = np.linspace(Z.min()-(Z.min() /10), Z.max()+(Z.max()/10), int(num))
     if flag == 1:
	   CS = plt.contourf(X,Y,Z,levels ,cmap = plt.cm.bone_r)
     if flag == 2: 
	   CS = plt.contourf(X,Y,Z,levels ,cmap = plt.cm.bone_r)
	   CS2 = plt.contour(CS,levels=CS.levels[::2], colors = 'k', hold='on')
     if flag == 0:
	   CS = plt.contour(X,Y,Z,levels, colors = 'k')
     
     ax.invert_yaxis()
     ax.set_xlabel('latitude (degrees)', fontsize = 20)
     ax.set_ylabel('pressure (hPa)', fontsize = 20)
     ax.set_title(varstring + ' Contour Plot - Day:  ' + str(a.day[dayt]), fontsize = 25)
     ax.grid(which='both', color = 'black', linewidth = 0.5)
     f = interp1d(a.latitude, a.level[a.trop_height[int(dayt)]], kind = 'cubic')
     xnew = np.linspace(a.latitude[0],a.latitude[-1],1000)
     ynew = f(xnew)
#     l, = ax.plot(xnew,ynew,'k-', dashes=[8,4,2,4,2,4],lw=2)
#     ll, = ax.plot(xnew[320:-1],ynew[320:-1],'y', dashes=[8,4,2,4,2,4],lw=8)
#     line_string= 'tropopause'
#     pos = [(xnew[-200]+xnew[-1])/2., (ynew[-200]+ynew[-1])/2.]
#     xscreen = ax.transData.transform(zip(xnew[-200::],ynew[-200::]))
#     rot = np.rad2deg(np.arctan2(*np.abs(np.gradient(xscreen)[0][0][::-1])))
#     rot = 0
#     ltex = plt.text(pos[0]-10, pos[1]+45, line_string, size=20, rotation=rot, verticalalignment='center', color = l.get_color(), ha="center", va="center",bbox = dict(ec='none' ,fc='none'))
     fig.set_facecolor('white')
     plt.yticks([900,800,700,600,500,400,300,200,100,50, 10, 5, 1, 0.5])
     plt.gca().set_yticklabels([900,800,700,600,500,400,300,200,100,50, 10 ,5, 1, 0.5])
     plt.xticks([-85, -55, -25, 0, 25, 55, 85 ])
     plt.gca().set_xticklabels([-90, -60, -30, 0, 30, 60, 90])
     if flag ==1:
	  cbar = plt.colorbar(CS, format='%.0f')
	  cbar.ax.set_ylabel('percent change')
	  l, = ax.plot(xnew,ynew,'y-', dashes=[8,4,2,4,2,4],lw=2)

     if flag ==2:
	  cbar = plt.colorbar(CS, format=':.0%')
	  cbar.ax.set_ylabel('percent change')
	  cbar.add_lines(CS2)
	  l, = ax.plot(xnew,ynew,'y-', dashes=[8,4,2,4,2,4],lw=2)

     if flag ==0:
	  plt.clabel(CS, inline=1, inline_spacing=6 , colors = 'k', fmt = '%.0%', fontsize = 20) 
	  l, = ax.plot(xnew,ynew,'k-', dashes=[8,4,2,4,2,4],lw=2)
 #     ll, = ax.plot(xnew[320:-1],ynew[320:-1],'y', dashes=[8,4,2,4,2,4],lw=8)
     line_string= 'tropopause'
     pos = [(xnew[-200]+xnew[-1])/2., (ynew[-200]+ynew[-1])/2.]
     xscreen = ax.transData.transform(zip(xnew[-200::],ynew[-200::]))
#     rot = np.rad2deg(np.arctan2(*np.abs(np.gradient(xscreen)[0][0][::-1])))
     rot = 0
     ltex = plt.text(pos[0]-10, pos[1]+45, line_string, size=20, rotation=rot, verticalalignment='center', color = l.get_color(),ha="center", va="center",bbox = dict(ec='none' ,fc='none'))


