# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:08:48 2022

input: copied link (lines 22-23) to all tide files (save from downloads to single folder)
    
output: a single csv file with all data ordered chronologically from start to end date
output: a single csv file with matching wave and water level data by hour

@author: smrosen2
"""

import glob
import os
import pandas as pd 

#----tide files---------------------
### Merge csv files into one file ordered chronologically by time (for both measured and predicted water levels)
    
# Set the path for joining multiple files (opening the webbrowser will automatically save files to downloads directory)
measured_path = r"C:\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\2. Import tides\NOAA T&C data\measured"
predicted_path = r"C:\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\2. Import tides\NOAA T&C data\predicted"
files_hr = os.path.join(measured_path, "CO-OPS__8651370__hr*.csv").replace("\\","/")
files_pr = os.path.join(predicted_path, "CO-OPS__8651370__pr*.csv").replace("\\","/")

#Creates a list of merged files for both measured and predicted water levels (with their full paths)
files_hr = glob.glob(files_hr)
files_pr = glob.glob(files_pr)

#Join hr and pr files with concat and read_csv
tide_df_hr = pd.concat(map(pd.read_csv, files_hr), ignore_index = True)
tide_df_pr = pd.concat(map(pd.read_csv, files_pr), ignore_index = True)

# sort values ascending by the 'Date Time' column
tide_df_hr.sort_values(by = ['Date Time'], inplace = True)
tide_df_pr.sort_values(by = ['Date Time'], inplace = True)


# convert the Date Time string to date object
tide_df_hr['Date Time'] = pd.to_datetime(tide_df_hr['Date Time'])
tide_df_pr['Date Time'] = pd.to_datetime(tide_df_pr['Date Time'])

# create new column called "time" that is in a different time format 
# (so all time columns match between wave and tide dfs) 
tide_df_hr['time'] = tide_df_hr['Date Time'].dt.strftime('%m/%d/%Y %H:%M')
tide_df_pr['time'] = tide_df_pr['Date Time'].dt.strftime('%m/%d/%Y %H:%M')

# delete original time from tide dfs
tide_df_hr.drop(['Date Time'], inplace = True, axis = 1)
tide_df_pr.drop(['Date Time'], inplace = True, axis = 1)

# drop duplicates in tide dfs
# for some reason dates are duplicated in some spots
tide_df_pr_2 = tide_df_pr.drop_duplicates()
tide_df_hr_2 = tide_df_hr.drop_duplicates()

# merge tide dfs by time column (merge only times that do not match)
# merged by 'outer' in order to get all data; data missing on certain dates for measured
merged_df = pd.merge(tide_df_hr_2, tide_df_pr_2, on = 'time', how = 'outer')



#-----wave file-----------------
# load in wave file with full time series
wave_csv = r"C:\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\0. Get WIS data\full_WIS_time_series_UTC.csv"
wave_df = pd.read_csv(wave_csv)

# convert the 'time' column to date object
wave_df['time'] = pd.to_datetime(wave_df['time'])

# create new column called "time_new" that is in a different time format; this 
wave_df['time_new'] = wave_df['time'].dt.strftime('%m/%d/%Y %H:%M')

# delete original time from wave_df
wave_df.drop(['time'], inplace = True, axis = 1)

# rename 'time_new' to 'time'
wave_df.columns = wave_df.columns.str.replace('time_new', 'time')


# Merge tide and wave dataframes by the 'time' column and save to csv file
# merged on left in order to gt all wave data, and exclude tide data that is outside of wave date range
final_merged_df = pd.merge(wave_df, merged_df, on= 'time', how = 'left')

# sort by time in ascending order
final_merged_df.sort_values(by = ['time'], inplace = False)

# convert merged_df to csv file
final_merged_df.to_csv("full_waves_tides_1980_2020.csv", index = False)






    