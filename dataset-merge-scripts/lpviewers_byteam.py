
# coding: utf-8

# In[4]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[35]:


#import domestic league pass views data
lpv_d = pd.read_csv('New_Domestic_League_Pass_Viewership.csv')

#games for each team, regular season
lpv_d2 = pd.concat([lpv_d.assign(Team = lpv_d['Home'], Opp = lpv_d['Away']),
                  lpv_d.assign(Team = lpv_d['Away'], Opp = lpv_d['Home'])])

#at home?
lpv_d2['At_Home'] = (lpv_d2.Team == lpv_d2.Home)

#regular season
lpv_d2.Date = pd.to_datetime(lpv_d2.Date)
lpv_d2 = lpv_d2[(lpv_d2.Date >= '10/17/2017') & (lpv_d2.Date <= '4/11/2018') & ~(lpv_d2.Team.isin(["EST","WST","USA","WLD"]))]

#lpv_d2.to_csv('lpv_d2.csv')

