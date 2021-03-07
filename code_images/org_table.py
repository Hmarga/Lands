#!/usr/bin/env python
# coding: utf-8

# In[1]:


# I  Libraries
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# II  Table
# Manual list with definitions of organism
color_r = [["lightgrey","lightgrey"],
           ["whitesmoke","whitesmoke"],
           ["lightgrey","lightgrey"],
           ["whitesmoke","whitesmoke"],
           ["gold","gold"]]

columns = ['Organism/Group','Land Needed']
data = [['Food and Agricultural Organization','6.8Ha per person'],
         ['infographic by 1BOG.org','0.0005Ha per person'],
         ['aquaponics','0.8Ha per family of four'],
         ['Grow BioIntensive','0.04 Ha per person'],
         ['Permaculture','1Ha per family of four']]
         
fig = plt.figure(figsize=(12,5))
cx = fig.add_subplot(111, frameon=False, xticks=[], yticks=[])

tao=plt.table(colLabels=columns, 
                    cellText = data, # dlands.valu
                    loc='left', 
                    cellColours=color_r,#plt.cm.hot(normal(vals)),
                    colWidths = (0.5,0.3),
                    cellLoc = 'center',
                    rowLoc = 'left',
                    bbox = (-0.15,0,1.25,1) #xo, yo, x1, y1
                   )

# Changing the fontfamily
props = dict(boxstyle='round', facecolor='red', alpha=0.5) #wheat
for n in range(2):
    tao[0,n].set_text_props(weight= 'bold', size=60)
for n in range(1,5):
    for s in range(0,2):
        tao[n,s].set_text_props(size=48)
for n in range(2):
    tao[5,n].set_text_props(weight='extra bold',size='xx-large', color='blue', style='oblique', bbox=props)

plt.tight_layout()
plt.savefig('../images/org_table.png')


# In[ ]:




