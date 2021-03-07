#!/usr/bin/env python
# coding: utf-8

# In[4]:


# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

# II- Download the reference table
w_land = pd.read_csv('../data/w_land.csv')

#  wlands16 Backup
wlands = w_land.copy()


# In[3]:


# Function to define the pie groups
get_ipython().run_line_magic('matplotlib', 'inline')

wlands['CL%_ind'] = ''
def ind_cl(x):
    n=''
    if x <20:
        n = "<20%"
    if 20<= x <40:
        n = "20%-40%"
    if 40<= x <60:
        n = "40%-60%"    
    if 60 <= x <80:
        n = "60%-80%"
    return n

wlands['CL%_ind'] = wlands['CL%'].apply(ind_cl)

wl = wlands.groupby('CL%_ind').count()

# Define the plot
names=wl.name_w.index
size= wl.name_w.values

# Create the labels
labels= []
for n in range(names.shape[0]):
    ls = names[n]+ ', '+str(size[n])+' countries'
    labels.append(ls)

#Create a circle for the center of the plot
my_circle=plt.Circle((0,0), 0.7, color='white')

plt.pie(size, 
        labels=labels,
        colors=['blue','green','skyblue','orange'],
        pctdistance = 0.4,
        textprops={'fontsize':'12'})
plt.title ('Countries grouped by CL%', fontweight='bold')
p=plt.gcf()
p.gca().add_artist(my_circle)


plt.savefig('../images/c_pie.png')
plt.show()

