#!/usr/bin/env python
# coding: utf-8

# #  Objective of this source code:
# ### 1- Create the indicators use for the analysis.
# ### 2- Generate the correspondant dataframe.

# In[1]:


# I.
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

import geopandas as gpd
from shapely import wkt
#from area import area
import numpy as np

# II
# Reading the main table
wl = pd.read_csv('../data/wl.csv', 
                 header=0, 
                 encoding='iso8859_1')

#  wlands Backup
wlands = wl.copy()


# In[2]:



# III
# Creating the dataframe to calcule the main indicators
AL = wlands[['region_country','name_w','regionw','pop_est','value', 'geometry', 'continent']][wlands['a_type']=='AL'].rename(columns={'value':'AL'}).reset_index(drop=True)
PC = wlands[['value']][wlands['a_type']=='PC'].rename(columns={'value':'PC'}).reset_index(drop=True)
LA = wlands[['value']][wlands['a_type']=='LA'].rename(columns={'value':'LA'}).reset_index(drop=True)

w_land = pd.concat([AL, PC, LA], axis=1, join='inner')


def noNaN(df,values):
    for v in values:
        df[values] = df[values].replace(np.nan, 0)
        return df[values]

noNaN(w_land,['AL','PC','LA'])

# II
# Creating the indicators:
# CL, CL%(AL + PC), 'pop_est%', 'density' and 'density_CL', HpF, ref, ind
w_land['CL']= w_land['AL']+w_land['PC']
w_land['CL%']= 100*w_land['CL']/w_land['LA']
w_land['pop_est%'] = 100* w_land['pop_est']/w_land['pop_est'].sum()
w_land['density'] = (w_land['pop_est']/4)/(0.1 + w_land['LA']*1000)
w_land['density_CL'] = (w_land['pop_est']/4)/(0.1+w_land['CL']*1000)

ref_val = 1 #---->> Ha Reference Value!!!!

w_land['ref_val'] = 1
w_land['HpF'] = (4000) * w_land['CL']/w_land['pop_est']
w_land['ref'] = w_land['HpF'] - ref_val
w_land = w_land.sort_values(by=['continent', 'ref']).reset_index(drop=True)
w_land['ind'] = w_land['HpF'].apply(lambda x: 'over' if x >=ref_val else 'under')

## Exceptions:
#w_land = w_land[~w_land['name_w'].str.contains('Falkland Is.')] 


# In[3]:


# Data frame with the countrys of the merged tables and the new indicators.

w_land.to_csv(r'../data/w_land.csv', index = False)

