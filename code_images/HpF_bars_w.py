#!/usr/bin/env python
# coding: utf-8

# In[1]:


# I.
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import pandas as pd
import geopandas as gpd
import numpy as np

# II
# Download reference table
w_land = pd.read_csv('../data/w_land.csv')

#  wlands Backup
w_land = w_land.copy()


# In[3]:


# III
# Summary of world values
get_ipython().run_line_magic('matplotlib', 'inline')

plt.style.use('seaborn-darkgrid')
plt.rcParams.update({'ytick.labelleft':'off',
                     'axes.labelsize':14,
                     'xtick.labelsize':12
                    })

r = w_land['regionw'].unique()

coli = ['regionw', 'ind', 'HpF']
pv = w_land[coli]
pv = pv.groupby(['regionw','ind']).count()
pv['%'] = pv.groupby(level=0).apply(lambda x:  100*x / x.sum())

fig= plt.figure(figsize=(10,6))

# Define the barplots: under and over.
overbar = pv['%'][pv.index.isin(['over'], level=1)].to_list()
if len(overbar) == 6: ##Adding a 0 value in order to have the same list len with underbar
    overbar.insert(5,0)
underbar = pv['%'][pv.index.isin(['under'], level=1)].to_list()

# Define graph setting
barWidth = 1

# Create over/under bars
nu = plt.bar(r, underbar, color='orange', edgecolor='white', width=barWidth, label="Under")
no = plt.bar(r, overbar, bottom=underbar, color='green', edgecolor='white', width=barWidth, label="Over" )

plt.box(on=False)
# Add a legend
plt.legend(ncol=2, fontsize=13, bbox_to_anchor=(0.4,1))

# Custom x axis
wlegend = ['East Asia & \nPacific', 'Europe &\n Central Asia','Latin America &\n Caribbean',
           'Middle East &\n North Africa', 'North\n America', 'South Asia', 'Sub-Saharan\n Africa']
plt.xticks(r, wlegend)
plt.tick_params(axis='both', which='both', length=0)
plt.xlabel("CL Country Percentage per Geographic Region")

# Placing the percentages values
for n in range(len(overbar)):
    if n == 5:
        plt.text(nu.patches[n].xy[0]+0.3, nu.patches[n].xy[1]+2, str(round(underbar[n],1))+'%', fontsize=16, fontstyle='oblique')
    else:
        plt.text(nu.patches[n].xy[0]+0.3, nu.patches[n].xy[1]+2, str(round(underbar[n],1))+'%', fontsize=16, fontstyle='oblique')
        plt.text(no.patches[n].xy[0]+0.3, no.patches[n].xy[1]+2, str(round(overbar[n],1))+'%', fontsize=16, fontstyle='oblique')


# To fix the plot size to the layout 
plt.tight_layout()

# Show graphic
plt.savefig('../images/HpF_bars_w.png')


# In[ ]:




