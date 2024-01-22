#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
data = pd.read_csv('D:/zieit/диплом/CS2_33_8_30_10.csv')


# In[3]:


df = pd.DataFrame(data)


# In[4]:


c_1 = df[df['Cycle_Index']==1] 


# ## Получаем данные в отделной колонке dq/dv

# In[7]:


c_1['roundedV'] = round(c_1['Voltage(V)'], 3)


# In[8]:


c_1


# In[9]:


c_1 = c_1.drop_duplicates(
        subset=[
            'roundedV',
            'Cycle_Index'])


# In[10]:


c_1


# In[11]:


c_1 = c_1.reset_index(drop=True)


# In[15]:


c_1['dV'] = c_1['Voltage(V)'].diff()


# In[16]:


c_1charge = c_1[c_1['Current(A)'] > 0]


# In[17]:


c_1charge['Charge_dQ'] = c_1charge['Charge_Capacity(Ah)'].diff()


# In[18]:


c_1charge


# In[19]:


c_1charge['dQ/dV'] = c_1charge['Charge_dQ'] /c_1charge['dV']
c_1charge[['dQ/dV', 'dV', 'Charge_dQ']] = c_1charge[['dQ/dV', 'dV', 'Charge_dQ']].fillna(0)
c_1charge = c_1charge[c_1charge['dQ/dV'] >= 0]


# In[20]:


c_1charge


# In[27]:


ax = plt.axes()
ax.plot(c_1charge['Voltage(V)'], c_1charge['dQ/dV'])
ax.set(xlabel='Voltage', ylabel='dQ/dV')


# In[39]:


import numpy as np
import scipy.io
from scipy.signal import savgol_filter

def my_savgolay(dataframe, windowlength, polyorder):
    """Takes battery dataframe with a dQ/dV column and applies a
    sav_golay filter to it, returning the dataframe with a new
    column called Smoothed_dQ/dV"""
    assert not windowlength % 2 == 0
    assert polyorder < windowlength
    unfilt = pd.concat([dataframe['dQ/dV']])
    unfiltar = unfilt.values
    dataframe['Smoothed_dQ/dV'] = scipy.signal.savgol_filter(
        unfiltar, windowlength, polyorder)
    return dataframe


# In[50]:


c_1_f = my_savgolay(c_1charge, 99, 8)


# In[60]:


ax = plt.axes()
ax.plot(c_1_f['Voltage(V)'], c_1_f['Smoothed_dQ/dV'], color = 'k', linewidth=4)
ax.plot(c_1charge['Voltage(V)'], c_1charge['dQ/dV'], color = 'g', linewidth=1)
ax.set(xlabel='Voltage', ylabel='dQ/dV')


# In[42]:


c_1_f 


# In[ ]:




