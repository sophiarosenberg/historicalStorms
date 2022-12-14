# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:59:25 2022

This code takes a csv with a 'storm' column and selects out storms > 12 hrs consecutive duration 
and saves to a csv

@author: smrosen2
"""


import pandas as pd

###------select storms that are longer than 12 hours----------

# Set path to excel file with all times with waves Hs > hs90 AND storm number
storm_file = r"C:\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\1. Identify storms based on Hs - updated\Hs90_time_series.xlsx"


## Create panda dataframe with necessary wave columns
df  = pd.read_excel(storm_file, usecols = ['storm','time','Hs','Tp','Dm'])


## Group by storm number and count number of entries per storm
## Need to assign a name "count" to the count column and use reset index
## For example, storm 1 has 12 entries (duration = 12 hrs)

df_storms = df.groupby(['storm']).size().reset_index(name = 'duration(hrs)')


## Find storms that are less than 12 hours duration and convert it to a list
df_storms.drop(df_storms[df_storms['duration(hrs)'] > 12].index, inplace = True)

storms_to_delete = list(df_storms["storm"])
#print (len(storms_to_delete))
# x number of storms <12 hrs in duration


## Using list of storms from previous step, delete storms < 12hrs from original data frame (df_all):
df2 = df[~df['storm'].isin(storms_to_delete)]

# Export new csv file with all storms >12hrs
df2.to_csv('Hs90storms_greater_than_12hrs.csv',index = False)

# create a df with storm number and duration
new_df = df2.groupby(['storm']).size().reset_index(name = 'duration(hrs)')
new_df = new_df.assign(storm_new=range(1,len(new_df)+1))
new_df.to_csv('storm_durations.csv',index = False)

# 786 storms with Hs > Hs90 (2.13m) and longer than 12hrs duration

### go into csv and use previous IF statement again to get new updated storm numbers




