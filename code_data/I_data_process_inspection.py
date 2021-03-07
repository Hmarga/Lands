#!/usr/bin/env python
# coding: utf-8

# #  Objective of this source code:
# ### 1- Download, inspect and format the UN data in order to merge it with the geopandas and Cartopy library.
# ### 2- Generate the correspondant dataframe.

# In[33]:


# I.
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

import geopandas as gpd
import numpy as np


# ## How many types of lands are classified by the UN statistics?

# In[34]:


# II 

landun = pd.read_csv('../data/SYB62_145_201904_Land.csv', 
                      header=1, encoding='iso8859_1')#'utf-8-sig')

# Reference column
landun['general_source'] = 'https://data.un.org/' #-Environment, Land - last version 2019
# or https://www.un.org/en/databases/ Statistical Data UN Data

# Change columns name
list = {'Unnamed: 1' : 'region_country',
         'Region/Country/Area': 'number',
         'Series' : 'type',
         'Value' : 'value',
         'Year' : 'year',
         'Footnotes' : 'footnotes',
         'Source' : 'source',
        }

landun = landun.rename(columns = list)

print('- The df has ',str(len(landun.columns)), ' columns :\n')
col = [print('*',landun.columns[n]) for n in range(len(landun.columns))]

print('\n- A size of ',str(landun.shape[0]), ' rows',
      '\n- A',landun.isnull().sum()[landun.isnull().sum()>0].item(),' null values; just in the "footnotes column',
      '\n- More specific details: \n')

landun.info()


# In[20]:


landun[(landun['region_country'].str.contains('Sudan')) & (landun.type.str.contains('Land'))]


# In[21]:


[print(n, landun.type.unique()[n])  for n in range(len(landun.type.unique()))]


# * There are 8 different groups, that can be classified in 5 types of land:
#     - The 5 lands types:  
#         - Land area ("thousand hectares")
#         - Arable land ("thousand hectares" and "% of total land area")
#         - Forest cover ("thousand hectares" and "% of total land area")
#         - Permanent crops ("thousand hectares" and "% of total land area")
#         - Important sites for terrestrial biodiversity protected ("% of total sites                                     protected")
# 

# ## How many countries do we have?

# In[22]:


print('\nThere are ' +str(landun.region_country.unique().shape[0])+ ' different names of regions/countries.\n')
#lcountry = print(landun.region_country.unique())


# If we see carefull the data, the firsts registers are region names (from 'Africa' to 'Polynesia'). We will filter just the countries names later.

# ## How much data do we have for every country by year?

# In[23]:


# Functions to style the differences in the tables

def highlight_max(s): # highlight the maximum in a Series yellow.
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]
    
def highlight_red(s): # highlight the maximum in a Series red.
    is_max = s == s.max()
    return ['color: red' if v else '' for v in is_max]


lg = landun.groupby(['year','type']).count()
lg[['region_country', 'value']]

###################################################################
# Let's focus in the nearest year with more complete data = 2016 ##
###################################################################

l16 = landun[landun.year==2016]
lg = l16.groupby(['year','type']).count()
lg = lg[['region_country']].sort_values(by='region_country')
lg['dif'] = lg.region_country.max() - lg.region_country
lg['dif_%'] = 100*(lg.dif/lg.region_country.max())

lg.style.apply(highlight_max, subset=['region_country']).apply(highlight_red, subset=['dif', 'dif_%'])


# Notes:
# 
# - The remarkables aspects of the table above are:
#    - The max value is 259. This means that the 'Land area' is the land type with more data statized; if we consider that there are 279 country names, there are lost 20 register this column for this specific type; and more for the rest of the types.
#    - The less percentage of data correspond to 'Important sites for terrestrial biodiversity protected (% of total sites protected)' type.
#    - There are no NULLs values, are just less values/registers/rows per country. See the complement in plot below. The column that has null values is footnotes; and there is data not needed for this example.
#    - These missing records will be watched later.
# 
# Because there are names in the 'region_country' column that are regions (like 'Middle Africa'), we will wait until match this data with the geopandas one, in order to filter just the countries and analyse better this values.
# 
# 

# 
# ## Let's see the geopandas library.

# In[24]:


# VI 

# NOTE: reg_world is a merge between the geopandas and shpreader libraries, in order to obtain
# the world regions asociated with the country and continent.

reg_world = pd.read_csv('../data/reg_world.csv', 
                       header=0, encoding='utf-8-sig') #'iso8859_1')#

world = reg_world.copy()

print('- The df has ',str(len(world.columns)), ' columns :\n')
col = [print('*',world.columns[n]) for n in range(len(world.columns))]

print('\n- A size of ',str(world.shape[0]), ' rows',
      '\n- No NULL values',
      '\n- More specific details: \n')

world.info()


# ## How many countries do we have in the geopandas library?

# In[25]:


print('\nThere are ' +str(world.name.unique().shape[0])+ ' different names of countries.\n')

# wcountry = print(world.name.unique())
# wcountry


# ### Merge  dataframes
# 
# ### In order to mix the country location data with the lands distribution, we will match the 'region_country' of the Lands df with the 'name' of the world df. 
# 

# In[26]:



world_lands = world.merge(landun, left_on ='name',
                          right_on ='region_country', how ='outer', 
                          indicator=True) #left_index=True


# There are register not coincident in both tables. This means, there are country names that are not exactly the same in both data bases.
# Let's find out this cases, keeping in mind that the reference is the geopandas df (world).
# We'll focus in those ones missing in world.

# In[27]:


# DataFrame with all the register, includind this ones that are not coincidents.

def diff_countries(ldf, cl): # df1 is world, df2 is landun
    df1=ldf[0]
    df2=ldf[1]
    n0 = cl[0]
    n1 = cl[1]
    d1 = pd.DataFrame(df1[n0].unique(), columns=[n0])
    d1['name_dif']=''
    d1['n_ind']=''
    d2 = df2[n1].unique()
    for nc in d2:
        pat = nc
        d1['name_dif'] = d1['name_dif'].mask(d1[n0].str.contains(pat, regex=False),pat)
    for l in range(d1.shape[0]):
        if d1.loc[l,n0] == d1.loc[l,'name_dif']:
            d1.loc[l,'n_ind'] = 'idem'
    d1 = d1[d1['n_ind']!= 'idem']
    d1 = d1[d1.name_dif!='']
    d1 = d1.drop('n_ind', axis=1)
        
    return (d1)

# Calling the function to know which country name in Landun is similar to World 
ldf1=[world, landun]
cl1 = ['name','region_country']
over_landun = diff_countries(ldf1,cl1)    

# Calling the function to know which country name in World is similar to Landun
ldf2=[landun, world]
cl2 = ['region_country', 'name']
over_world = diff_countries(ldf2,cl2)

over_landun.to_csv('../data/over_landun.csv', index = False)
over_world.to_csv('../data/over_world.csv', index = False)


# ###  <font color=green>There are some countries in both tables that are the same, but are writen in a very different way.</font>
# ###  <font color=green>That's why they were obtained the files above in order to show the partial matchs between both db: UN and Geopandas</font>
# ### <font color=green> Inspecting them manually, it mas made a reference table called 'country_ref'.</font>

# In[28]:


# Merging the country names

country_ref = pd.read_csv('../data/country_ref.csv', 
                          header=0, encoding='utf-8-sig')#iso8859_1')

# Particular cases:
landun.loc[1880:1904,'region_country'] = landun.loc[1880:1904,'region_country'].replace("Côte dIvoire","Côte d'Ivoire")


# # Let's merge this country_ref table with the landun one:

# In[29]:


world_lands[['name', 'region_country']].shape

country_ref
def add_countries(df1):
    df1['name_w']='' #df1 = landun
    for nc in range(country_ref.shape[0]):
        pat = country_ref.loc[nc,'region_country']
        df1['name_w']=df1['name_w'].mask(df1['region_country']==pat, country_ref.loc[nc,'name'])   
    df1['name_w'] = df1['name_w'].mask(df1['name_w']=='',df1['region_country'])
    return df1
    
landun_w = add_countries(landun)
landun_w.shape, landun.shape


# Now there is the Landun (lands df) with two country names columns: One with it originals('region_country') 
# names and the other with the World df names (name_w).
# Let's merge them in order to see how is it the match.

# In[30]:


y = 2016
world_lands_after = world.merge(landun_w, left_on ='name',
                          right_on ='name_w', how ='inner', 
                          indicator=True) #left_index=True,


world_lands_before = world.merge(landun[landun.year==y], left_on ='name',
                          right_on ='region_country', how ='inner', 
                          indicator=True) #left_index=True,

world_lands_after.shape, world_lands_before.shape


# After here, it's taken the world_lands_after df as the main reference.

# In[31]:


wlands = world_lands_after.reset_index(drop=True)

wlands = wlands.drop(columns='name')
wlands.info()


# In[32]:


# Data frame with the countrys of the merged tables:
    # geopandas df
    # lands from the UN statistics    
       
wlands.astype({'geometry': str}).to_csv(r'../data/wlands.csv', index = False)

