#!/usr/bin/env python
# coding: utf-8

# In[1]:


# I.
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

import pandas as pd
import geopandas as gpd
from shapely import wkt
import numpy as np

# II
# Download reference table
w_land = pd.read_csv('../data/w_land.csv')

#  wlands Backup
w_land = w_land.copy()


# In[3]:


# III Histogram 

plt.style.use('seaborn-darkgrid') 

plt.rcParams.update({'xtick.labelsize':12,
                     'ytick.labelsize':12,
                     'ytick.labelleft':'on',
                     'ytick.labelright':'off',
                     'xtick.labelbottom':'off',
                     'axes.spines.left': False,
                     'axes.spines.bottom' : False,
                     'axes.spines.top': False,
                     'axes.spines.right':False,
                     'ytick.left':False,
                     'xtick.bottom':False,
                     'xtick.top': False,
                     'axes.labelsize':14,
                     'axes.edgecolor':'slategrey',
                     'grid.linewidth':0.5
                    })

fig = plt.figure(figsize=(15,8))

### Graph 5
a_bins = 36
ax5, bins, patches5 = plt.hist(w_land['density_CL'],  orientation='horizontal', bins= a_bins,
                            range= (0, 12), rwidth=0.9) 

plt.ylabel('Number Families per Hectare ')
plt.xlabel('Country Frecuency')
plt.title('III Country distribution by Density of Cultivable Lands', weight='bold', size=15)
plt.yticks(np.arange(0, 12, 0.5))

count_width = 0
for f in range(3,36):
    patches5[f].set_fc('orangered'),
    count_width += int(patches5[f].get_width())

# # Adding the value of each bar 
high = 0.03
texto = lambda t: plt.text(3.5, high + t.xy[1], int(t.get_width()),size=13, 
                            fontstyle='oblique', color='rebeccapurple', fontweight='bold')
vfunc = np.vectorize(texto)

p = [patches5[i] for i in range(len(patches5)) if patches5[i].get_width() > 0]
## Filter the 0 width columns 
vfunc(p)

# Adding the text box
for n in range(3):
    if n==0:
        coc = (100*ax5[n])/170
    else:
        coc = (100*(ax5[n]+ax5[n-1]+ax5[n-2])/170)
    
    plt.text(5*n+6, 1.5+n/0.6, # XY pos
                 (str(int(coc))+'% - '+str(ax5[n])+' countries - '+ str(format(bins[n+1],".2f"))+' F.Dens'),
                 fontsize=12, fontstyle='oblique',
                 bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='green'))

# Additional styling
plt.axhline(y=1, color='green') # Adding the reference line

# Adding the arrows
plt.annotate("", xy=(7, 1.5), xytext=(7, 0.15),  arrowprops=dict(arrowstyle="->", lw= 3, linestyle='--', color='rebeccapurple'))
plt.annotate("", xy=(14, 3), xytext=(14, 0.5),  arrowprops=dict(arrowstyle="->", lw= 3, linestyle='--', color='rebeccapurple'))
plt.annotate("", xy=(21, 4.8), xytext=(21, 0.8),  arrowprops=dict(arrowstyle="->", lw= 3, linestyle='--', color='rebeccapurple'))


plt.savefig('../images/hist_dens_CL.png')
plt.show()


# In[ ]:




