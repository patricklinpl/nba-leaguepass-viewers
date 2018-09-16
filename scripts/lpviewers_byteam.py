
# coding: utf-8

# In[1]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[5]:


#import domestic league pass views data
lpv_d = pd.read_csv('../dataset/provided-data/New_Domestic_League_Pass_Viewership.csv')

#regular season
lpv_d.Date = pd.to_datetime(lpv_d.Date)
lpv_d = lpv_d[(lpv_d.Date >= '10/17/2017') & (lpv_d.Date <= '4/11/2018') & ~(lpv_d.Home.isin(["EST","WST","USA","WLD"]))]


#games for each team, regular season
lpv_d2 = pd.concat([lpv_d.assign(Team = lpv_d['Home'], Opp = lpv_d['Away']),
                  lpv_d.assign(Team = lpv_d['Away'], Opp = lpv_d['Home'])])

#at home?
lpv_d2['At_Home'] = (lpv_d2.Team == lpv_d2.Home)

lpv_d.to_csv('../dataset/lpv_d.csv')
lpv_d2.to_csv../dataset/lpv_d2.csv')

