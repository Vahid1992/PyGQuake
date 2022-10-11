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

df['Vs'] = 1
df['Vs'] = df['Vs'].astype('object')

#Number of Mont_Carlo Simulation 
mont_size = 1000


#Lists that the Vs30 values are save in
coorx_list = []
coory_list =[]
vs30_list = []


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

#print(group)
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


     #Vs for 8< Z <10
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
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 15.0))].index[0], 'Vs'] = pearson3.rvs(0.8653306111387722, 271.210496461739, 61.76779848778838,size=(1,mont_size))
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


     #Vs for 18 to 20 m (0 = Clay and (Sand o Gravel = 1 , 2))
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
     
     
     group.loc[group['Zone'] == 2,'h/Vs'] = 2/group['Vs']
     group.loc[group['Zone'] == 1,'h/Vs'] = 2/group['Vs']
     group.loc[group['Zone'] == 0,'h/Vs'] = 2/group['Vs']
     group.loc[group['Zone'] == 4,'h/Vs'] = 2/group['Vs']
     
     #print(group)
     #print(group['Vs'][0:15])

     total1=group['h/Vs'][0:15].sum()


     n_c=len(group [(group['Zone'] == 0)  & (group['Z1'] <= 29)]) 
     n_s=len(group [(group['Zone'] == 1)  & (group['Z1'] <= 29)]) 
     n_g=len(group [(group['Zone'] == 2)  & (group['Z1'] <= 29)])  
     n_t=len(group [(group['Zone'] == 4)  & (group['Z1'] <= 29)]) 
     

     v30= 30 /((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))
              
     
     #print(group)

     coorx_list.append(name[0])
     coory_list.append(name[1])
     vs30_list.append(v30)

dff=pd.DataFrame(list(zip(coorx_list,coory_list, vs30_list)), columns=['X','Y','Vs30'])

#print(dff)


#dff.iloc['Mean_Vs30'] = np.mean(dff['Vs30'])
def mean_nm(x):
    return np.mean(x)

def sum_nm(x):
    return np.sum(x)

dff['Mean_Vs30'] = dff['Vs30'].map(mean_nm)
dff['Var'] = (dff['Vs30'] - dff['Mean_Vs30'])**2
dff['Var_f']= ((dff['Var'].map(sum_nm))/mont_size)
dff['Sigma'] = (dff['Var_f'])**(0.5)

dff = dff.drop('Vs30', 1)
dff = dff.drop('Var', 1)
#print(dff)
#print(dff.head(5))
compression_opts = dict(method='zip',
                        archive_name='_Vs30Monte carlo_Probablistic_Plus_sigma_2022-04-21.csv')  
dff.to_csv('Vs30_Monte carlo_Probablistic_Plus_sigma_2022-04-21.zip', index=False,
          compression=compression_opts) 

toc = time.perf_counter()
print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")

