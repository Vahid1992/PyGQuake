import time
from typing import List
from numpy.lib.function_base import append, piecewise
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy.interpolate import CubicSpline
import re



df=pd.read_csv('C:/Users/vhosseinpo/Desktop/Code_f/Damage simulator/Final/Till_test_Monte carlo_Probablistic_Plus_sigma_2022-04-20.csv')


df = df.drop('VsAve', 1)
df = df.drop('T0', 1)
df = df.drop('Var_Vs', 1)
df = df.drop('Var_T0', 1)

print(df)

compression_opts = dict(method='zip',
                        archive_name='T0_Probablistic_Plus_sigma_plot_2022-04-21.csv')  
df.to_csv('T0_Probablistic_Plus_sigma_plot-2022-04-21.zip', index=False,
          compression=compression_opts) 