#!/usr/bin/env python
# coding: utf-8

# #  Objective of this source code:
# ### 1- Inspect the dataframe (created in I), filter the non necessary data and fill the missing records.
# ### 2- Generate the correspondant dataframe.

# In[17]:


# I.
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

import geopandas as gpd
#from area import area
import numpy as np

# II
# Reading the main reference df: wlands.

wlands = pd.read_csv('../data/wlands.csv', 
                      header=0, encoding='iso8859_1')


wlands.columns
# Reorder the columns 
wlands = wlands[['name_w', 'region_country','regionw','type', 'value','year', 'continent', 
                 'pop_est', 'geometry','number', 'iso_a3', 'gdp_md_est', 'footnotes', 
                  'source', 'general_source']]


# Let's inspect the data.

# In[18]:


wlands_16 = wlands[wlands.year==2016]
wcount = wlands_16.groupby(['name_w']).count()
wun = wcount['type'].unique()


# - This list {{wun}} are the differents values for lands types per country.
# - Those over 8, are more than expected; and under 8, are missing.
# 
# We'll work at first this with surplus values.

# In[19]:


wcount = wlands_16.groupby(['name_w']).count()
wcount[wcount['type']>8]


# Are China and Netherlands this that has extra values.
# Let's zoom them.

# In[20]:


wlands_16[(wlands_16['name_w'].isin(['China','Netherlands']))
         & (wlands_16['type']=='Land area (thousand hectares)')]


# - The 'name_w' column is the reference, and the 'region_country' is the name comming from the Land df.
# - In both cases, we can see that even that the values of every type of land change, the geometry is the same for every country named in 'name_w'.
# - Hence, in the map plot, it'll be not possible to draw the different locations.
# 
# So, this extra columns are going to be excluded.
# 

# In[21]:


wlands_16 = wlands_16[~wlands_16['region_country'].isin(['Netherlands Antilles [former]', 
                                              'China, Hong Kong SAR',
                                             'China, Macao SAR'])]


# Let's work just with the year 2016, and do some math.

# In[22]:


countries = len(wlands_16['name_w'].unique())
expected = 8 * countries
actual_registers = wlands_16.shape[0]
diffe = expected - actual_registers      


# - Notes:
#     - There are {{countries}} differentes countries.
#     - If every country has 8 differents types of land, we are specting to have {{expected}} registers in the dataframe; and we actually have {{actual_registers}} registers.
#     - This means, are {{diffe}} missing.
# 

# In[23]:


wc = wlands_16.groupby(['type']).count()
wc.year.sort_values(ascending=False)


# In[24]:


# Missing records from which countries?

wo = wlands_16.groupby(['name_w']).count()
wless = 8 - wo.type[wo.type<8]
print(wless, '\nTotal missing: ', wless.sum() )

wlist = wless.index.tolist() # List of countries with missing registers
w_16=wlands_16[wlands_16['name_w'].isin(wlist)]


# In[25]:


# Which has no Land Area?

wo = w_16.groupby(['name_w','type']).count()
wo = wo.reset_index(level=['type'])
wo = wo.pivot(columns='type', values='value')
wo.style.highlight_null(null_color='yellow')


# ### From the last table, we can see the missing types of land per country. Are in total 29 rows.
# ### Now we'll add the quantity of rows needed, it'll be merge with the original table, and then we will fill with the correspondant value.

# In[26]:


# Adding the quantity of missing rows.

def concat_list(df):
    left = []
    simple = []
    types = df.type.unique().tolist()
    rc = df['region_country'].unique().tolist()
    geom = df['geometry'].unique().tolist()
    c = 0
    for s in df['name_w'].unique():
        l_pc = df['type'][df['name_w']==s].tolist()
        for t in types:
            co = df['continent'][df.name_w==s].unique()[0]
            rw = df['regionw'][df.name_w==s].unique()[0]
            poe = df['pop_est'][df.name_w==s].unique()[0]
            geom = df['geometry'][df.name_w==s].unique()[0]
            num = df['number'][df.name_w==s].unique()[0]
            iso = df['iso_a3'][df.name_w==s].unique()[0]
            gpd = df['gdp_md_est'][df.name_w==s].unique()[0]
            if t not in l_pc:
                # the NaN spaces are the numbers of columns of the df reference
                simple.append([s,rc[c],rw, t,'',2016, co, poe, geom, num, iso, gpd,'','',''])
        c += 1
    return(simple)


l_simple = concat_list(w_16)#[1] # Reference list with no empty spaces
l_att = pd.DataFrame(l_simple, columns=(w_16.columns.tolist()))

# Fixing name problem
wlands_16['name_w'] = wlands_16['name_w'].str.replace("CÃ´te d'Ivoire", 'Cote dIvoire')
wlands_16['region_country'] = wlands_16['region_country'].str.replace("CÃ´te d'Ivoire", 'Cote dIvoire')


wlands16 = pd.concat([wlands_16, l_att], sort=False, axis=0).reset_index(drop=True)


# - The missing data can be classified in two: 
#     - this ones that has to be taken from external source.
#     - some others that can be calculated from data that we already has. (F. ex. Forrest cover (%) can be obtained from Forrest Cover Ha and Land area).
# 
# We'll began with the first case: data taken from external source.
# For this, it's going to be fill a table and then imported here.

# In[27]:


# Save to csv the missing reference table
l_simple = pd.DataFrame(l_simple, columns=wlands16.columns)

l_simple.to_csv(r'../data/l_simple.csv', index = False)


# In[28]:


# Open the csv of the missing records already filled

l_simple_mod = pd.read_csv('../data/l_simple_mod.csv', 
                      header=0, encoding='iso8859_1')


# In[29]:


# Merging the table with the missing values to the reference one (wlands_16)

wlands16 = pd.concat([wlands_16, l_simple_mod], sort=False, axis=0).reset_index(drop=True)
wlands16 = wlands16.sort_values(by='name_w')

wl = wlands16.copy()


# In[30]:



# II
# # Create the acronyme of the land types
wl['a_type'] = ''

lrep = {'Land area (thousand hectares)':'LA',
        'Arable land (thousand hectares)': 'AL', 'Arable land (% of total land area)':'AL_%',
        'Forest cover (thousand hectares)':'FC', 'Forest cover (% of total land area)':'FC_%',
        'Permanent crops (thousand hectares)':'PC','Permanent crops (% of total land area)':'PC_%',
        'Important sites for terrestrial biodiversity protected (% of total sites protected)':'IB%'}

wl['a_type'] = wl['type'].map(lrep)


# In[31]:


# Data frame with the countrys of the merged tables:
    # geopandas df
    # lands from the UN statistics
    # missing data
    
wl.to_csv(r'../data/wl.csv', index = False)

