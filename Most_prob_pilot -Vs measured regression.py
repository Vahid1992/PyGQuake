import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy.interpolate import CubicSpline




df_sgc=pd.read_csv('c:/Users/vhosseinpo/Desktop/Data for Develop/Damage_Simulator/blk_sgc_final2.csv')
df_till=pd.read_csv('c:/Users/vhosseinpo/Desktop/Data for Develop/Damage_Simulator/blk_till.csv') #Till values will be loaded here

df_till['Zone'] = 4  #because in Tills Csv file the Zone value is 0 but it should be 4

df2 = [df_sgc,df_till]
df = pd.concat(df2)

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


     group.loc[group['Zone'] == 2,'vs_gravel'] = (162.531)*((group['Z1'])**0.161)
     group.loc[group['Zone'] == 1,'vs_sand'] = (162.531)*((group['Z1'])**0.161)
     group.loc[group['Zone'] == 0,'vs_clay'] = (109.709*(group['Z1'])**0.246)
     group.loc[group['Zone'] == 4,'vs_till'] = 580
     

     group.loc[group['Zone'] == 2,'h/Vs'] = 2/group['vs_gravel']
     group.loc[group['Zone'] == 1,'h/Vs'] = 2/group['vs_sand']
     group.loc[group['Zone'] == 0,'h/Vs'] = 2/group['vs_clay']
     group.loc[group['Zone'] == 4,'h/Vs'] = 2/group['vs_till']

     
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
                        archive_name='Vs30_Mp_Measurerd_Vsdata_Till=580-2022-03-03.csv')  
dff.to_csv('Vs30_Mp_Measurerd_Vsdata_Till=580-2022-03-03.zip', index=False,
          compression=compression_opts)

        
