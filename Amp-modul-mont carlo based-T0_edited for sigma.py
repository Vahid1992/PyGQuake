import time
from typing import List
from numpy.lib.function_base import append, piecewise
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy.interpolate import CubicSpline
import re
# from mlutils import dataset, connector
import scipy.stats
from scipy.stats import *
from sklearn.preprocessing import StandardScaler
import math
import matplotlib.pyplot as plt
import warnings
import statsmodels.api as sm 
import seaborn as sns
import pylab as py
from scipy.stats import gamma
from scipy.stats import norm
from scipy.stats import beta
from scipy.stats import invgauss
from scipy.stats import uniform
from scipy.stats import pearson3


tic = time.perf_counter()


df_sgc=pd.read_csv('c:/Users/vhosseinpo/Desktop/Data for Develop/Damage_Simulator/blk_sgc_final2.csv') #this block model is related to Sand and Clay I should add till blocks to this DataFrame
df_till = pd.read_csv('c:/Users/vhosseinpo/Desktop/Data for Develop/Damage_Simulator/blk_till.csv') #data frame of till blocks

df_sgc_t=pd.read_csv('c:/Users/vhosseinpo/Desktop/Data for Develop/Damage_Simulator/Test data/sgc test data.csv') #Test data
df_till_t = pd.read_csv('c:/Users/vhosseinpo/Desktop/Data for Develop/Damage_Simulator/Test data/till test data.csv') #Test data

df_till['Zone'] = 4


df2 = [df_sgc,df_till]

df = pd.concat(df2)
 
#print(df)
#print(df)

df['Vs'] = 250

df['Vs'] = df['Vs'].astype('object')

#Number of Mont_Carlo Simulation 
mont_size = 500


#Lists that the Vs30 values are save in
coorx_list = []
coory_list =[]
vs_ave_list = []
t0_val_list = []


#print(df)
grouped = df.groupby(['X','Y'])

tic = time.perf_counter()


#Vs calculation for each block
for name, group in grouped:

     
     group = group.sort_values(by='Z',ascending=False)
     #print(group)
     group.loc[group['Zone'] == 2,'Z1'] = -((group['Z']) - ((group.iloc[0,2]) + 1))
     group.loc[group['Zone'] == 1,'Z1'] = -((group['Z']) - ((group.iloc[0,2]) +1))
     group.loc[group['Zone'] == 0,'Z1'] = -((group['Z']) - ((group.iloc[0,2]) + 1))
     group.loc[group['Zone'] == 4,'Z1'] = -((group['Z']) - ((group.iloc[0,2]) +1))
    
     #group.loc[group['Zone'] == 4,'Vs'] = 580  #I considered the Vs of till as 385 Based on Nastev et al. but I changed it to 580 based on Motazedian

     #Insert Till value for each depth equal to the motazedian Values:


#Vs for 0 < Z < 2
     try:
         group.at[group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 1.0))].index[0], 'Vs'] = norm.rvs(167.29, 51.14,size=(1,mont_size))
     except:
          try:
               group.at[group.loc[( group['Zone'] == 0) & ( (group['Z1'] == 1.0))].index[0], 'Vs'] = invgauss.rvs(1.1261363076163105, 86.13499308802449, 31.936641403334185,size=(1,mont_size))
          except:
               try:
                   group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 1.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                    pass
  

#Vs for 2 < Z < 4
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 3.0))].index[0], 'Vs'] = norm.rvs(195, 46.42,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[ (group['Zone'] == 0)  & ( (group['Z1'] == 3.0))].index[0], 'Vs'] = pearson3.rvs(-0.5141773152287485, 153.27658747702444, 36.21983854820455,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 3.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 4 < Z < 6
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 5.0))].index[0], 'Vs'] = norm.rvs(200.7, 32.79,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 5.0))].index[0], 'Vs'] = beta.rvs(6.547396353352547, 7.223340071155293, 45.712631296229375, 257.0617609425842,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 5.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 6< Z <8
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 7.0))].index[0], 'Vs'] = invgauss.rvs(0.05652148577625393, 30.54235860458192, 3438.690058713144,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 7.0))].index[0], 'Vs'] = beta.rvs(1.3958921003033669, 2.183027749044431, 105.22365548291673, 169.2849500262882,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 7.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 8< Z <10;
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 9.0))].index[0], 'Vs'] = beta.rvs(1.244889111129242, 2.475781117997336, 166.03745834302617, 199.89633212250178,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 9.0))].index[0], 'Vs'] = gamma.rvs(19.70380862547599, 7.717350836493496, 8.871748708019934,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 9.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 10< Z <12;
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 11.0))].index[0], 'Vs'] = gamma.rvs( 7.06930213075877, 106.18823990682716, 20.206914568030264 ,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 11.0))].index[0], 'Vs'] = norm.rvs(193.86, 40,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 11.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 12< Z <14;     
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 13.0))].index[0], 'Vs'] = gamma.rvs( 1.8842494746204357, 174.44072397415243, 42.15095601905071 ,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 13.0))].index[0], 'Vs'] = beta.rvs(2.2686464974618596, 3.390300075127488, 115.37142017129472, 209.087720639677,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 13.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 14 to 16 m
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 15.0))].index[0], 'Vs'] = beta.rvs(0.8242021039715993, 0.9799695878610736, 168.99999999999997, 226.69376247169276,size=(1,mont_size))
     except:
          try:
                group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 15.0))].index[0], 'Vs'] = gamma.rvs(3.6357730769355507, 120.1061330653387, 26.359527792561188,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 15.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 16 to 18 m
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 17.0))].index[0], 'Vs'] = norm.rvs(251.27,80.94,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 17.0))].index[0], 'Vs'] = invgauss.rvs(0.64, 159.24, 100.62,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 17.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 18 to 20 m
     try:     
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 19.0))].index[0], 'Vs'] = norm.rvs(258.0,53.03,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 19.0))].index[0], 'Vs'] = invgauss.rvs(0.598, 162.87, 121.26,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 19.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 20 to 22 m:
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 21.0))].index[0], 'Vs'] = beta.rvs(0.7158788325473433, 0.2980984255564101, 93.56452131315946, 218.43547868684058,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 21.0))].index[0], 'Vs'] = gamma.rvs(1.3184238324278428, 184.25623112521134, 47.0710101936822,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 21.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

     
#VS for 22 to 24 m
     try:     
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 23.0))].index[0], 'Vs'] = uniform.rvs(258.0, 33.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 23.0))].index[0], 'Vs'] = pearson3.rvs(0.8228526357760895, 244.39996788477546, 37.19115860174169,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 23.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


 #Vs for 24 to 26 m
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 25.0))].index[0], 'Vs'] = norm.rvs(227.83,71.93,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 25.0))].index[0], 'Vs'] = invgauss.rvs(0.2762085236479199, 190.01119984652314, 207.86122691360248,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 25.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 26 to 28 m:
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 27.0))].index[0], 'Vs'] = uniform.rvs(242.0, 70.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 27.0))].index[0], 'Vs'] = gamma.rvs(2.742306726833103, 199.2445345447964, 19.750413870694363,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 27.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

     
 #Vs for 28 to 30 m:
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 29.0))].index[0], 'Vs'] = uniform.rvs(178.0, 103.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 29.0))].index[0], 'Vs'] = uniform.rvs(184, 115,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 29.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 30 to 32 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 31.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 31.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 31.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 32 to 34 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 33.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 33.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 33.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 34 to 36 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 35.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 35.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 35.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass



#Vs for 36 to 38 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 37.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 37.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 37.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 38 to 40 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 39.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 39.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 39.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass
     
#Vs for 40 to 42 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 41.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 41.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 41.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 42 to 44 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 43.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 43.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 43.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 44 to 46 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 45.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 45.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 45.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 46 to 48 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 47.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 47.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 47.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass
     
     
#Vs for 48 to 50 m:        
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 49.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 49.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 49.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 50 to 52 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 51.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 51.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 51.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 52 to 54 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 53.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 53.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 53.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

 #Vs for 54 to 56 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 55.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 55.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 55.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 56 to 58 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 57.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 57.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 57.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 58 to 60 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 59.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 59.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 59.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass
     
#Vs for 60 to 62 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 61.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 61.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 61.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 62 to 64 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 63.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 63.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 63.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 64 to 66 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 65.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 65.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 65.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 66 to 68 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 67.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 67.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 67.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

          
#Vs for 68 to 70 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 69.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 69.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 69.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass  

#Vs for 70 to 72 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 71.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 71.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 71.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass  

#Vs for 72 to 74 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 73.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 73.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 73.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 74 to 76 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 75.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 75.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 75.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass   


#Vs for 76 to 78 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 77.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 77.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 77.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass   


#Vs for 78 to 80 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 79.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 79.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 79.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass   


#Vs for 80 to 82 m:           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 81.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 81.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 81.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass   

#Vs for 82 to 84 m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 83.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 83.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 83.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass   

#Vs for 84 to 86 m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 85.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 85.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 85.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass   

#Vs for 86 to 88 m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 87.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 87.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 87.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass   

#Vs for 88 to 90 m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 89.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 89.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 89.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass   

     
#Vs for 90 to 92 m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 91.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 91.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 91.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass  


#Vs for 92 to 94 m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 93.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 93.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 93.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass  

#Vs for 94 to 96 m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 95.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 95.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 95.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass 

#Vs for 96 to 98 m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 97.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 97.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 97.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


#Vs for 98 to 100 m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 99.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 99.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 99.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass

#Vs for 100 to 102m:
           
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 101.0))].index[0], 'Vs'] = uniform.rvs(204.0, 92.0,size=(1,mont_size))
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  &  (group['Z1'] == 101.0)].index[0], 'Vs'] = beta.rvs(7.35698765329232, 558599.8258111686, 151.07667144854122, 8638072.143276554,size=(1,mont_size))
          except:
               try:
                    group.at[group.loc[( group['Zone'] == 4) & ( (group['Z1'] == 101.0))].index[0], 'Vs'] = norm.rvs(580, 174,size=(1,mont_size))
               except:
                     pass


     #print(group)


     group.loc[group['Zone'] == 2,'h/Vs'] = 2/group['Vs']
     group.loc[group['Zone'] == 1,'h/Vs'] = 2/group['Vs']
     group.loc[group['Zone'] == 0,'h/Vs'] = 2/group['Vs']
     group.loc[group['Zone'] == 4,'h/Vs'] = 2/group['Vs']
     
     #print(group)
     #print(group['Vs'][0:15])

     total1=group['h/Vs'].sum()


     n_c=len(group['Zone'] == 0)
     n_s=len(group['Zone'] == 1)
     n_g=len(group['Zone'] == 2)   
     n_t=len(group['Zone'] == 4)

     n_tot= n_c + n_s + n_g + n_t 
     

     vs_ave= (n_tot*2)/(total1)
     t0_val=(4*(n_tot*2))/(vs_ave)

     
     #print(group)

     coorx_list.append(name[0])
     coory_list.append(name[1])
     vs_ave_list.append(vs_ave)
     t0_val_list.append(t0_val)



dff=pd.DataFrame(list(zip(coorx_list,coory_list, vs_ave_list, t0_val_list)), columns=['X','Y','VsAve','T0'])

#print(dff)


#dff.iloc['Mean_Vs30'] = np.mean(dff['Vs30'])
def mean_nm(x):
    return np.mean(x)

def sum_nm(x):
    return np.sum(x)


dff['Mean_VsAve'] = dff['VsAve'].map(mean_nm)
dff['Var_Vs'] = (dff['VsAve'] - dff['Mean_VsAve'])**2
dff['Var_f_Vs']= ((dff['Var_Vs'].map(sum_nm))/mont_size)
dff['Sigma_Vs'] = (dff['Var_f_Vs'])**(0.5)


dff['Mean_T0'] = dff['T0'].map(mean_nm)
dff['Var_T0'] = (dff['T0'] - dff['Mean_T0'])**2
dff['Var_f_T0']= ((dff['Var_T0'].map(sum_nm))/mont_size)
dff['Sigma_T0'] = (dff['Var_f_T0'])**(0.5)

dff = dff.drop('VsAve', 1)
dff = dff.drop('Var_T0', 1)
dff = dff.drop('Var_f_T0', 1)
dff = dff.drop('T0', 1)

#print(dff)
#print(dff.head(5))
compression_opts = dict(method='zip',
                        archive_name='T0_Monte carlo_Probablistic_Plus_sigma_2022-04-29.csv')  
dff.to_csv('T0_Monte carlo_Probablistic_Plus_sigma_2022-04-29.zip', index=False,
          compression=compression_opts) 

toc = time.perf_counter()
print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")

