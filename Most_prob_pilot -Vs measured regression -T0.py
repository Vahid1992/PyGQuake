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
t0_val_list = []
vs_ave_list = []

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

     
     total1=group['h/Vs'].sum()

     n_c=len(group['Zone'] == 0)
     n_s=len(group['Zone'] == 1)
     n_g=len(group['Zone'] == 2)   
     n_t=len(group['Zone'] == 4) 
     

     #group.loc[group['Zone'] == 2,'Vs30'] = 30/((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))
     #group.loc[group['Zone'] == 1,'Vs30'] = 30/((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))
     #group.loc[group['Zone'] == 0,'Vs30'] = 30/((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))
     #group.loc[group['Zone'] == 4,'Vs30'] = 30/((total1)+((30-((2*n_c)+(2*n_s)+(2*n_g)+(2*n_t)))/2500))

     #print(group)
     
     
     n_tot= n_c + n_s + n_g + n_t 

     vs_ave= (n_tot*2)/(total1)
     t0_val=(4*(n_tot*2))/(vs_ave)

     
     #print(group)

     coorx_list.append(name[0])
     coory_list.append(name[1])
     vs_ave_list.append(vs_ave)
     t0_val_list.append(t0_val)



dff=pd.DataFrame(list(zip(coorx_list,coory_list, vs_ave_list, t0_val_list)), columns=['X','Y','VsAve','T0'])

compression_opts = dict(method='zip',
                        archive_name='T0_Mp_Measurerd_Vsdata_Till=580-2022-04-28.csv')  
dff.to_csv('T0_Mp_Measurerd_Vsdata_Till=580-2022-04-28.zip', index=False,
          compression=compression_opts)

        
