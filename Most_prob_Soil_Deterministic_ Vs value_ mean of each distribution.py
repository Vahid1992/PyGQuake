import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy.interpolate import CubicSpline
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

df_sgc=pd.read_csv('c:/Users/vhosseinpo/Desktop/Data for Develop/Damage_Simulator/blk_sgc_final2.csv')
df_till=pd.read_csv('c:/Users/vhosseinpo/Desktop/Data for Develop/Damage_Simulator/blk_till.csv') #Till values will be loaded here

df_till['Zone'] = 4  #because in Tills Csv file the Zone value is 0 but it should be 4

df2 = [df_sgc,df_till]
df = pd.concat(df2)

df['Vs'] = 1
df['Vs'] = df['Vs'].astype('object')

coorx_list = []
coory_list =[]
vs30_list = []
nc_list=[]
ns_list=[]
ng_list=[]
nt_list=[]

#print(df)


grouped = df.groupby(['X','Y'])
#Vs calculation for each block
for name, group in grouped:

     group = group.sort_values(by='Z',ascending=False)

     group.loc[group['Zone'] == 2,'Z1'] = -((group['Z']) - ((group.iloc[0,2]) + 1))
     group.loc[group['Zone'] == 1,'Z1'] = -((group['Z']) - ((group.iloc[0,2]) +1))
     group.loc[group['Zone'] == 0,'Z1'] = -((group['Z']) - ((group.iloc[0,2]) + 1))
     group.loc[group['Zone'] == 4,'Z1'] = -((group['Z']) - ((group.iloc[0,2]) +1))

     group.loc[group['Zone'] == 4,'Vs'] = 580


#Vs for 0 < Z < 2
     try:
         group.at[group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 1.0))].index[0], 'Vs'] = 167.29
     except:
          try:
              group.at[group.loc[( group['Zone'] == 0) & ( (group['Z1'] == 1.0))].index[0], 'Vs'] = 122.1
          except:
               pass


     #Vs for 2 < Z < 4
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 3.0))].index[0], 'Vs'] = 195
     except:
          try:
               group.at[ group.loc[ (group['Zone'] == 0)  & ( (group['Z1'] == 3.0))].index[0], 'Vs'] = 153.27
          except:
               pass


     #Vs for 4 < Z < 6
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 5.0))].index[0], 'Vs'] = 200.7
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 5.0))].index[0], 'Vs'] = 167.93
          except:
               pass


     #Vs for 6< Z <8
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 7.0))].index[0], 'Vs'] = 224.90
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 7.0))].index[0], 'Vs'] = 171.250
          except:
               pass


     #Vs for 8< Z <10;
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 9.0))].index[0], 'Vs'] = 232.920
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 9.0))].index[0], 'Vs'] = 182.524
          except:
               pass


     #Vs for 10< Z <12;
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 11.0))].index[0], 'Vs'] = 249.04
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 11.0))].index[0], 'Vs'] = 193.86
          except:
               pass


     #Vs for 12< Z <14;     
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 13.0))].index[0], 'Vs'] = 253.86
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 13.0))].index[0], 'Vs'] = 199.193
          except:
               pass


     #Vs for 14 to 16 m
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 15.0))].index[0], 'Vs'] = 272.56
     except:
          try:
                group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 15.0))].index[0], 'Vs'] = 215.94
          except:
               pass


     #Vs for 16 to 18 m
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 17.0))].index[0], 'Vs'] = 251.27
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 17.0))].index[0], 'Vs'] = 223.64
          except:
               pass


     #Vs for 18 to 20 m
     try:     
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 19.0))].index[0], 'Vs'] = 258.0
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 19.0))].index[0], 'Vs'] = 235.38
          except:
               pass


     #Vs for 20 to 22 m:
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 21.0))].index[0], 'Vs'] = 247.78
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 21.0))].index[0], 'Vs'] = 246.3
          except:
               pass

     
     #VS for 22 to 24 m
     try:     
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 23.0))].index[0], 'Vs'] = 274.5
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 23.0))].index[0], 'Vs'] = 244.39
          except:
               pass


     #Vs for 24 to 26 m
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 25.0))].index[0], 'Vs'] = 227.83
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 25.0))].index[0], 'Vs'] = 247.42
          except:
               pass


     #Vs for 26 to 28 m:
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 27.0))].index[0], 'Vs'] = 277.0
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 27.0))].index[0], 'Vs'] = 253.40
          except:
               pass

     
     #Vs for 28 to 30 m:
     try:
          group.at[ group.loc[((group['Zone'] == 1) | (group['Zone'] == 2)) & ( (group['Z1'] == 29.0))].index[0], 'Vs'] = 229.5
     except:
          try:
               group.at[ group.loc[(group['Zone'] == 0)  & ( (group['Z1'] == 29.0))].index[0], 'Vs'] = 241.5
          except:
                pass




     group.loc[group['Zone'] == 2,'h/Vs'] = 2/group['Vs']
     group.loc[group['Zone'] == 1,'h/Vs'] = 2/group['Vs']
     group.loc[group['Zone'] == 0,'h/Vs'] = 2/group['Vs']
     group.loc[group['Zone'] == 4,'h/Vs'] = 2/group['Vs']

     
     total1=group['h/Vs'][0:15].sum()

     n_c=len(group [(group['Zone'] == 0)  & (group['Z1'] <= 29)]) 
     n_s=len(group [(group['Zone'] == 1)  & (group['Z1'] <= 29)]) 
     n_g=len(group [(group['Zone'] == 2)  & (group['Z1'] <= 29)])  
     n_t=len(group [(group['Zone'] == 4)  & (group['Z1'] <= 29)]) 
     

     #group.loc[group['Zone'] == 2,'Vs30'] = 30/((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))
     #group.loc[group['Zone'] == 1,'Vs30'] = 30/((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))
     #group.loc[group['Zone'] == 0,'Vs30'] = 30/((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))
     #group.loc[group['Zone'] == 4,'Vs30'] = 30/((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))

     #print(group)
     
     

     v30= 30/((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))
     coorx_list.append(name[0])
     coory_list.append(name[1])
     vs30_list.append(v30)
     nc_list.append(n_c)
     ns_list.append(n_s)
     ng_list.append(n_g)
     nt_list.append(n_t)




dff=pd.DataFrame(list(zip(coorx_list,coory_list, vs30_list, nc_list, ns_list, ng_list, nt_list)), columns=['X','Y','Vs30','Clay_n','Sand_n','Gravel_n','Till_n'])

compression_opts = dict(method='zip',
                        archive_name='2Wiht Number of blks_out_final_Deterministic (Mean of the distributis)_Mp_Till=580.csv')  
dff.to_csv('2With_number_blk_out_final_Deterministic(Mean of the distributions)_Mp_Till=580.zip', index=False,
          compression=compression_opts) 



toc = time.perf_counter()
print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")