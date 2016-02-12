
# coding: utf-8

# ### Lomb-Scargle
# 
# *Author: [Aymeric SPIGA](http://www.lmd.jussieu.fr/~aslmd)*
# 
# We perform a Lomb-Scargle periodogram on the TEXES measurements. We use the Lomb-Scargle algorithm [included in the `scipy.signal` library](http://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.signal.lombscargle.html). It has [known limitations](https://jakevdp.github.io/blog/2015/06/13/lomb-scargle-in-python/) but should [perform well](http://joseph-long.com/writing/recovering-signals-from-unevenly-sampled-data/) in the simple case we consider here. What follows has been tested on a simple combination of two cosines of distinct frequencies, before it was applied to the actual observed signal.

# Import scientific + plotting librairies

# In[1]:

import numpy as np
import scipy.signal as scisig
import matplotlib.pyplot as mpl
get_ipython().magic(u'matplotlib inline')


# Load measurements (ASCII file)

# In[2]:

level = "2Pa"
longi,temp = np.loadtxt("Temperature_"+level+".txt",unpack=True)


# <small>Sensitivity test: try will less points</small>

# In[3]:

#temp=temp[::2]
#longi=longi[::2]


# <small>Sensitivity test: try with periodically copy-pasting signal</small>

# In[4]:

#nt = temp.size
#temp2 = np.zeros(4*nt)
#temp2[0:nt] = temp[0:nt]
#temp2[nt:2*nt] = temp[0:nt]
#temp2[2*nt:3*nt] = temp[0:nt]
#temp2[3*nt:4*nt] = temp[0:nt]
#longi2 = np.zeros(4*nt)
#longi2[0:nt] = longi[0:nt]
#longi2[nt:2*nt] = longi[0:nt] + 360.
#longi2[2*nt:3*nt] = longi[0:nt] + 720.
#longi2[3*nt:4*nt] = longi[0:nt] + 1080.
#temp = temp2
#longi = longi2


# Remove zeros for missing values

# In[5]:

w = np.where(temp > 0)
longi = longi[w]
temp = temp[w]


# Make a plot to check what the signal looks like

# In[6]:

mpl.plot(longi,temp,'r.')
mpl.xlabel(u'longitude')
mpl.ylabel(u'temperature')


# Convert longitudes in radians

# In[7]:

longi = longi * np.pi/180.


# <small>Uncomment what follows to perform a simple test of the Lomb-Scargle procedure</small>

# In[8]:

#temp = np.cos(3.*longi) + np.cos(5.*longi)
#mpl.plot(longi,temp,'r.')


# Prepare the grid for angular frequencies (starting from wavenumbers)

# In[9]:

wn_min, wn_max, npoints = 0.75,15,2000
periods = np.linspace(wn_min, wn_max, npoints)
ang_freqs = 2 * np.pi / periods


# Compute the unnormalized Lomb-Scargle periodogram on the centered values

# In[10]:

power = scisig.lombscargle(longi, temp - temp.mean(), ang_freqs)


# Normalize the power

# In[11]:

N = len(longi)
power *= 2 / (N * temp.std() ** 2)


# Convert back periods $[2\pi,\pi,2\pi/3,\ldots]$ to wavenumbers $[1,2,3,\ldots]$

# In[12]:

wavenumber = 2.*np.pi / periods


# Check the dominant modes

# In[13]:

from scipy.ndimage.measurements import maximum_position
nmodes = 5
dominant_wn = np.zeros(nmodes)
search = power
zelab = search > 0 # (all elements)
itit = 1
# -- while loop
while itit <= nmodes:
  # -- find dominant mode
  ij = maximum_position(search,labels=zelab)
  dominant_wn[itit-1] = 2.*np.pi / periods[ij[0]]
  spower = search[ij]
  # -- print result
  print("%2i %8.2f %8.2f" % (itit,dominant_wn[itit-1],spower))
  # -- iterate
  zelab = search < spower # remove maximum found
  itit += 1


# Display Lomb-Scargle periodogram with a vertical line for the dominant mode. Save figure.

# In[17]:

mpl.plot(wavenumber, power)
mpl.xlabel("Zonal wavenumber")
mpl.ylabel("Normalized spectral power")
mpl.title("Lomb-Scargle periodogram for temperature at "+level)
mpl.axvline(dominant_wn[0], lw=2, color='red', alpha=0.4, label="dominant WN = %4.1f" % (dominant_wn[0]))
mpl.legend()
mpl.savefig("periodogram.pdf", bbox_inches='tight')

