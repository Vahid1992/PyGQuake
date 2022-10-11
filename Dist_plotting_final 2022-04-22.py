from cmath import nan
import time
from tkinter.font import BOLD
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
from scipy import stats




fig, ax = plt.subplots(1, 1)

#sand and gravel (Coarse)
distype_sand = stats.norm
p1_sand = 0.8653306111387722 
p2_sand = 0.9799695878610736, 
p_locsand ,p_scalesand = 251.27,80.94

x = np.linspace(distype_sand.ppf(0.001,loc=p_locsand, scale=p_scalesand), distype_sand.ppf(0.999, loc=p_locsand, scale=p_scalesand), 1000)
plt.plot(x, distype_sand.pdf(x, loc=p_locsand, scale=p_scalesand), color='crimson', label='Coarse sediments (Normal)')



#Clay (Fine)
 
distype_clay=stats.invgauss

p1_clay=0.64
p2_clay= 3.390300075127488 
p_locclay, p_scaleclay =159.24, 100.62

print(p_locclay)

x = np.linspace(distype_clay.ppf(0.001, p1_clay, loc=p_locclay, scale=p_scaleclay), distype_clay.ppf(0.999, p1_clay,  loc=p_locclay, scale=p_scaleclay), 1000)
plt.plot(x, distype_clay.pdf(x, p1_clay,  loc=p_locclay, scale=p_scaleclay), color='blue', label='Fine sediments (Inverse Gaussian)')

plt.xlim(0, 500)
plt.ylim(0,0.035)

ax.tick_params(axis='both', which='major', labelsize=14)
ax.tick_params(axis='both', which='minor', labelsize=14)

plt.xlabel("Vs (m/s)",fontsize=16)
plt.ylabel("Probability",fontsize=16)

plt.legend()
plt.show()
