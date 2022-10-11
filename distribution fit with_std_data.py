import re
import pandas as pd
import numpy as np
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


df = pd.read_csv("C:/Users/vhosseinpo/Desktop/Vs-data (1)/SCPTu-UQAC-MTQ-Total.csv")


#print(df.head())
#print(df.shape)
#print(df.dtypes)
#print(df.columns)


columns = ['Z (m)','Vs (m/s)', 'Vs_measured (m/s)', 'Soil Type', 'New Soil Type']

# This dataframe is whole of the data

df = df[columns]

#this data fram is data related to sand soil type
df2= df[df['New Soil Type']=='Clay']


#this dataframe is clay soil type
df3= df[df['New Soil Type']=='Sand']


#input data to run


#df4=df2[(df2['Z (m)'] > 30)]  

df4=df3[(df3['Z (m)'] > 30) & (df3['Z (m)'] <= 32)]

#print(df2["Vs (m/s)"].max())

#print(df4[(df4['Vs (m/s)']>250)])

#Change these before run the code
bin_histo = 5
bin_chi = 10

#How to define number of bins for Histogram:

#n                  Bins
#Less than 25         5
#25 to 100             Nearest integer to n / 5
#More than 100        Largest integer below 10 × log(n)

#How to define number of bins for Chi-square 

    #For χ² (chi-squared) binning with n data points:
      #If n < 35, bins = nearest integer to [n/5]
      #If n >= 35, bins = largest integer below [1.88 n ^ (2/5)]
    # 1010 points for All data's - 20 bins


df4['Vs (m/s)'].hist(bins=bin_histo,legend=True)

def standarise(column,pct,pct_lower):
    sc = StandardScaler() 
    y = df4[column][df4[column].notnull()].to_list()
    y.sort()
    len_y = len(y)
    y = y[int(pct_lower * len_y):int(len_y * pct)]
    len_y = len(y)
    yy=([[x] for x in y])
    sc.fit(yy)
    y_std =sc.transform(yy)
    y_std = y_std.flatten()
    return y_std,len_y,y

#Fitting different Distributions and checking Goodness of fit based on Chi-square Statistics

def fit_distribution(column,pct,pct_lower):
    # Set up list of candidate distributions to use
    # See https://docs.scipy.org/doc/scipy/reference/stats.html for more
     
    y_std,size, y_org = standarise(column,pct,pct_lower)
    dist_names = ['weibull_min','norm','weibull_max','beta',
                 'invgauss','uniform','gamma','expon', 'lognorm','pearson3','triang']

    chi_square_statistics = []
    dist_params = []

    #For χ² (chi-squared) binning with n data points:
      #If n < 35, bins = nearest integer to [n/5]
      #If n >= 35, bins = largest integer below [1.88 n ^ (2/5)]
    # 1010 points for All data's - 20 bins

    percentile_bins = np.linspace(0,100,bin_chi)
    percentile_cutoffs = np.percentile(y_org, percentile_bins) # Here for my data I should change the value with y_org 
    observed_frequency, bins = (np.histogram(y_org, bins=percentile_cutoffs)) #refer previous comment
    cum_observed_frequency = np.cumsum(observed_frequency)

    # Loop through candidate distributions

    for distribution in dist_names:
        # Set up distribution and get fitted distribution parameters
        dist = getattr(scipy.stats, distribution)
        param = dist.fit(y_org) #Here we also can use y_std as input parameter for chi-squared 

        #print("{}\n{}\n".format(dist, param))

        dist_params.append(param)

        
      
        # Get expected counts in percentile bins
        # cdf of fitted sistrinution across bins
        cdf_fitted = dist.cdf(percentile_cutoffs, *param)
        expected_frequency = []
        for bin in range(len(percentile_bins)-1):
            expected_cdf_area = cdf_fitted[bin+1] - cdf_fitted[bin]
            expected_frequency.append(expected_cdf_area)

        # Chi-square Statistics
        expected_frequency = np.array(expected_frequency) * size
        cum_expected_frequency = np.cumsum(expected_frequency)
        ss = round(sum (((cum_expected_frequency - cum_observed_frequency) ** 2) / cum_observed_frequency),0)
        chi_square_statistics.append(ss)


    #Sort by minimum ch-square statistics
    results = pd.DataFrame()
    results['Distribution'] = dist_names
    results['chi_square'] = chi_square_statistics
    results ['Dis_params'] = dist_params
    results.sort_values(['chi_square'], inplace=True)

    #print ('\nDistributions listed by Betterment of fit:')
    #print ('............................................')
    #print (results)
    return results



Dist_param= fit_distribution('Vs (m/s)',0.99,0.01)
print(Dist_param)



#Write distribution params in Excel file
Dist_param.to_excel("Disparam_Clay_30m-32m.xlsx", engine='xlsxwriter')







y_std,len_y,y_org = standarise('Vs (m/s)',0.99,0.01)

#print("Y_std is:",y_std)
#print("len y is:",len_y)
#print("Y is:",y)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Distparams defination for each distribution,

norm_param1, norm_param2= Dist_param.loc[Dist_param['Distribution'] == 'norm', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'norm', 'Dis_params'].iloc[0][1]

inguass_param1, inguass_param2,inguass_param3= Dist_param.loc[Dist_param['Distribution'] == 'invgauss', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'invgauss', 'Dis_params'].iloc[0][1],Dist_param.loc[Dist_param['Distribution'] == 'invgauss', 'Dis_params'].iloc[0][2]

lognorm_param1,lognorm_param2,lognorm_param3= Dist_param.loc[Dist_param['Distribution'] == 'lognorm', 'Dis_params'].iloc[0][0] , Dist_param.loc[Dist_param['Distribution'] == 'lognorm', 'Dis_params'].iloc[0][1], Dist_param.loc[Dist_param['Distribution'] == 'lognorm', 'Dis_params'].iloc[0][2]

beta_param1,beta_param2,beta_param3,beta_param4= Dist_param.loc[Dist_param['Distribution'] == 'beta', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'beta', 'Dis_params'].iloc[0][1], Dist_param.loc[Dist_param['Distribution'] == 'beta', 'Dis_params'].iloc[0][2], Dist_param.loc[Dist_param['Distribution'] == 'beta', 'Dis_params'].iloc[0][3]

pearson3_param1,pearson3_param2, pearson3_param3= Dist_param.loc[Dist_param['Distribution'] == 'pearson3', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'pearson3', 'Dis_params'].iloc[0][1], Dist_param.loc[Dist_param['Distribution'] == 'pearson3', 'Dis_params'].iloc[0][2]

uniform_param1, uniform_param2 = Dist_param.loc[Dist_param['Distribution'] == 'uniform', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'uniform', 'Dis_params'].iloc[0][1]

gamma_param1, gamma_param2, gamma_param3 = Dist_param.loc[Dist_param['Distribution'] == 'gamma', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'gamma', 'Dis_params'].iloc[0][1], Dist_param.loc[Dist_param['Distribution'] == 'gamma', 'Dis_params'].iloc[0][2]

triang_param1, triang_param2, triang_param3 = Dist_param.loc[Dist_param['Distribution'] == 'triang', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'triang', 'Dis_params'].iloc[0][1], Dist_param.loc[Dist_param['Distribution'] == 'triang', 'Dis_params'].iloc[0][2]

expo_param1, expo_param2 = Dist_param.loc[Dist_param['Distribution'] == 'expon', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'expon', 'Dis_params'].iloc[0][1]

weibull_max1, weibull_max2, weibull_max3 = Dist_param.loc[Dist_param['Distribution'] == 'weibull_max', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'weibull_max', 'Dis_params'].iloc[0][1], Dist_param.loc[Dist_param['Distribution'] == 'weibull_max', 'Dis_params'].iloc[0][2]

weibull_min1, weibull_min2, weibull_min3 = Dist_param.loc[Dist_param['Distribution'] == 'weibull_min', 'Dis_params'].iloc[0][0], Dist_param.loc[Dist_param['Distribution'] == 'weibull_min', 'Dis_params'].iloc[0][1], Dist_param.loc[Dist_param['Distribution'] == 'weibull_min', 'Dis_params'].iloc[0][2]

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

plt.hist(y_org,bins=bin_histo)
plt.xlabel('Vs (m/s)')
plt.ylabel('Frequency')



#Plotting most proprate distributions
# 
y1=y_org
y2=y_org #y_std 

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 5))
axes[0].hist(y1,bins=bin_histo)
axes[0].set_xlabel('Vs(m/s)\n\nHistogram plot of Oberseved Data')
axes[0].set_ylabel('Frequency')
axes[1].plot(y1,norm.pdf(y2,norm_param1, norm_param2))
axes[1].set_xlabel('Vs(m/s)\n\nNormal Distribution')
axes[1].set_ylabel('pdf')
fig.tight_layout()



fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 5))
axes[0].plot(y1,invgauss.pdf(y2,inguass_param1, inguass_param2,inguass_param3))
axes[0].set_xlabel('Vs(m/s)\n\nInverse-Gaussian Distribution')
axes[0].set_ylabel('pdf')
axes[1].plot(y1,lognorm.pdf(y2, lognorm_param1, lognorm_param2, lognorm_param3))
axes[1].set_xlabel('Vs(m/s)\n\nLognormal Distribution')
axes[1].set_ylabel('pdf')
fig.tight_layout()


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 5))
axes[0].plot(y1,beta.pdf(y2,beta_param1,beta_param2,beta_param3,beta_param4))
axes[0].set_xlabel('Vs(m/s)\n\nBeta Distribution')
axes[0].set_ylabel('pdf')
axes[1].plot(y1,pearson3.pdf(y2, pearson3_param1,pearson3_param2, pearson3_param3))
axes[1].set_xlabel('Vs(m/s)\n\nPearson3 Distribution')
axes[1].set_ylabel('pdf')
fig.tight_layout()


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 5))
axes[0].plot(y1,gamma.pdf(y2,gamma_param1,gamma_param2,gamma_param3))
axes[0].set_xlabel('Vs(m/s)\n\nGamma Distribution')
axes[0].set_ylabel('pdf')
axes[1].plot(y1,expon.pdf(y2, expo_param1,expo_param2))
axes[1].set_xlabel('Vs(m/s)\n\nExponential Distribution')
axes[1].set_ylabel('pdf')
fig.tight_layout()


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 5))
axes[0].plot(y1,weibull_max.pdf(y2,weibull_max1,weibull_max2,weibull_max3))
axes[0].set_xlabel('Vs(m/s)\n\nWeibull_max Distribution')
axes[0].set_ylabel('pdf')
axes[1].plot(y1,weibull_min.pdf(y2,weibull_min1,weibull_min2, weibull_min3))
axes[1].set_xlabel('Vs(m/s)\n\nWeibull_min Distribution')
axes[1].set_ylabel('pdf')
fig.tight_layout()


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 5))
axes[0].plot(y1,uniform.pdf(y2,uniform_param1,uniform_param2))
axes[0].set_xlabel('Vs(m/s)\n\n Uniform Distribution')
axes[0].set_ylabel('pdf')
axes[1].plot(y1,uniform.pdf(y2,uniform_param1,uniform_param2))
axes[1].set_xlabel('Vs(m/s)\n\nUniform Distribution')
axes[1].set_ylabel('pdf')
fig.tight_layout()





#QQ Plot 
##############################################################

data_points = norm.rvs(norm_param1, norm_param2, size=2000)   
data_points2 = invgauss.rvs(inguass_param1, inguass_param2,inguass_param3,size = 2000) 
data_points3 = lognorm.rvs(lognorm_param1,lognorm_param2,lognorm_param3,size = 2000)
data_points4 = beta.rvs(beta_param1,beta_param2,beta_param3,beta_param4,size = 2000)
data_points5 = weibull_max.rvs(weibull_max1, weibull_max2, weibull_max3 , size = 2000)
data_points6 = pearson3.rvs(pearson3_param1,pearson3_param2, pearson3_param3,size = 2000)
data_points7 = weibull_min.rvs(weibull_min1, weibull_min2, weibull_min3 , size = 2000)
data_points8 = uniform.rvs(uniform_param1, uniform_param2 , size = 2000)
data_points9 = expon.rvs(expo_param1, expo_param2 , size = 2000)
data_points10 = triang.rvs(triang_param1, triang_param2, triang_param3, size = 2000)
data_points11 = gamma.rvs(gamma_param1, gamma_param2, gamma_param3 , size = 2000)






f, ax = plt.subplots(figsize=(8,8))
ax.plot([100 , 500], [100, 500], ls="--", c=".3")

percentile_bins = np.linspace(0,100,100)
percentile_cutoffs1 = np.percentile(y_org, percentile_bins)
percentile_cutoffs_norm= np.percentile(data_points, percentile_bins)
percentile_cutoffs_invgauss = np.percentile(data_points2, percentile_bins)
percentile_cutoffs_lognorm = np.percentile(data_points3, percentile_bins)
percentile_cutoffs_beta = np.percentile(data_points4, percentile_bins)
percentile_cutoffs_weibull_max = np.percentile(data_points5, percentile_bins)
percentile_cutoffs_pearson3 = np.percentile(data_points6, percentile_bins)
percentile_cutoffs_weibull_min = np.percentile(data_points7, percentile_bins)
percentile_cutoffs_uniform = np.percentile(data_points8, percentile_bins)
percentile_cutoffs_expon = np.percentile(data_points9, percentile_bins)
percentile_cutoffs_triang = np.percentile(data_points10, percentile_bins)
percentile_cutoffs_gamma = np.percentile(data_points11, percentile_bins)


#to enable which dis will displayed on QQ plot, just simply turn on with removig comment sign #

#ax.scatter(percentile_cutoffs1,percentile_cutoffs_invgauss,c='r',label = 'Inverse-Gaussian Distribution',s = 40)
ax.scatter(percentile_cutoffs1,percentile_cutoffs_norm,c='b',label = 'Normal Distribution',s = 40)
#ax.scatter(percentile_cutoffs1,percentile_cutoffs_lognorm,c='g',label = 'Log-Normal Distribution',s = 40)
ax.scatter(percentile_cutoffs1,percentile_cutoffs_beta,c='y',label = 'Beta Distribution',s = 40)
#ax.scatter(percentile_cutoffs1,percentile_cutoffs_weibull_max,c='c',label = 'Weibull_max Distribution',s = 40)
ax.scatter(percentile_cutoffs1,percentile_cutoffs_pearson3,c='m',label = 'Pearson3 Distribution',s = 40)
#ax.scatter(percentile_cutoffs1,percentile_cutoffs_weibull_min,c='k',label = 'weibull_min Distribution',s = 40)
#ax.scatter(percentile_cutoffs1,percentile_cutoffs_uniform,c='0.75',label = 'Uniform Distribution',s = 40)
#ax.scatter(percentile_cutoffs1,percentile_cutoffs_expon,c='#ff7f0e',label = 'Expon Distribution',s = 40)
#ax.scatter(percentile_cutoffs1,percentile_cutoffs_triang,c='#8c564b',label = 'Triang Distribution',s = 40)
ax.scatter(percentile_cutoffs1,percentile_cutoffs_gamma,c='#9467bd',label = 'Gamma Distribution',s = 40)

ax.set_xlabel('Theoretical cumulative distribution')
ax.set_ylabel('Observed cumulative distribution')
ax.legend()
plt.show()

#####################################################################
