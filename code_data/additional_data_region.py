#!/usr/bin/env python
# coding: utf-8

# #  Objective of this souce code:
# ### 1- Merge the Cartopy library with the Geopandas one, in order to obtain the name of the Geographic Region of each country.
# ### 2- Generate the correspondant dataframe.

# In[25]:


# Ask shapereader to find the world regions

# I Libraries
import pandas as pd
import cartopy.io.shapereader as shpreader
import geopandas as gpd

# II
try:
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')) # GEOPANDAS DF
except:
    pass
    
shpfilename = shpreader.natural_earth(resolution='110m', 
                                      category='cultural',
                                      name='admin_0_countries')

reader = shpreader.Reader(shpfilename)
countries = reader.records()
country = next(countries)

# III Functions
def nome(s):
    df = s.attributes['NAME_EN'], s.attributes['REGION_WB'], s.attributes['NAME'], 
    s.attributes['GEOUNIT'], s.attributes['GEOU_DIF'],  s.attributes['GU_A3'],
    s.attributes['BRK_GROUP'] , s.attributes['POSTAL'] 
    return df

def region(c):
    countries_bn = sorted(countries, key=c)
    name_reg = []
    for country in countries_bn:
        name_reg.append([country.attributes['NAME_EN'], 
                         str(country.attributes['REGION_WB']), 
                         str(country.attributes['REGION_UN'])])
    df = pd.DataFrame(name_reg, columns=['name', 'regionw', 'regionun'])
    df = df.reset_index(drop=True)
    return(df)

# IV Create the df from shpreader
region = region(nome)


# In[26]:


# Merge shpreader and geopandas
rworld = world.merge(region, on='name', how='left', indicator=True)

rworld_miss = rworld[rworld._merge != 'both']
rworld_miss.astype({'geometry': str}).to_csv(r'../data/rworld_miss.csv', index = False)


# ### <font color=green> There are some countrys in Geopandas that were not found in Cartopy. </font>
# ### <font color=green> This missing records were filled manually.</font>
# 

# In[27]:


rworld_miss_mod = pd.read_csv('../data/rworld_miss_mod.csv', 
                      header=0, encoding='utf-8-sig')#'iso8859_1')#'


# In[28]:


rworld_miss_mod = pd.DataFrame(rworld_miss_mod)
rworld_both = rworld[rworld._merge == 'both']

# DF with both data region, continent and country
reg_world= pd.concat([rworld_both, rworld_miss_mod]).reset_index(drop=True)

reg_world= reg_world.drop(columns=['_merge'])

reg_world.astype({'geometry': str}).to_csv(r'../data/reg_world.csv', index = False)


# In[29]:


region.shape, world.shape, rworld.shape, reg_world.shape

