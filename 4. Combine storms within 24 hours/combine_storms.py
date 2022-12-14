# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 18:51:39 2022

Goal: Combine periods in between storms that are less than 24 hours apart
Method: when start periods are less than 24 hours apart, change old start time to new start time

helpful sites:
https://stackoverflow.com/questions/60039948/expand-pandas-dataframe-date-ranges-to-individual-rows

@author: smrosen2
"""
import pandas as pd
import datetime


### load file with storm numbers and times, and file with full wave dataset
# storm file
storm_file = r"C:\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\3. Merge tides and waves - Updated\merge storm waves and tides\storm_waves_tides_1980_2020_left_merge.csv"
storm_df = pd.read_csv(storm_file)

# load full merged wave and tide file
full_df = pd.read_csv(r"C:\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\3. Merge tides and waves - Updated\merge full waves and tides\full_waves_tides_1980_2020.csv")

# Convert date string to datetime object
full_df["time"] = pd.to_datetime(full_df["time"])



#### Create dfs with only storm start times and end times
df = storm_df[['storm', 'time']]

# Convert date string to datetime object
df["time"] = pd.to_datetime(df["time"])

# create separate dfs for start times and end times, respectively
df_start = df.drop_duplicates(subset = ['storm'], keep ='first').reset_index(drop = True)
df_end = df.drop_duplicates(subset = ['storm'], keep ='last').reset_index(drop = True)


# merge start and end time dfs as separate columns in the same df for the same storm
merged_df = pd.merge(df_start, df_end, on='storm')

# rename start and end time columns
merged_df = merged_df.rename(columns={'time_x': 'start_time', 'time_y': 'end_time'})

# Convert date string to datetime object (to match other df for later merging)
merged_df["start_time"] = pd.to_datetime(merged_df["start_time"])
merged_df["end_time"] = pd.to_datetime(merged_df["end_time"])

# add a column for new storm number
merged_df = merged_df.assign(storm_new=range(1,len(merged_df)+1))

# save start and end times to new csv
merged_df.to_csv("storm_start_end_times.csv")

### Get Hs for range between start and end times
# get range of times with associated storm number (freq = hourly)
new_df = merged_df
new_df['time'] = [pd.date_range(s, e, freq='h') for s, e in
              zip(pd.to_datetime(new_df['start_time']),
                  pd.to_datetime(new_df['end_time']))]

new_df = new_df.explode('time').drop(['start_time', 'end_time'], axis=1)


# merge by time to full waves and tides csv (all hours from 1980-end of 2019)
final_df = pd.merge(new_df, full_df, on='time', how='left')

# sort by time in ascending order
final_df.sort_values(by = ['time'], inplace = False)

# create a df with storm number and duration
new_df = final_df.groupby(['storm']).size().reset_index(name = 'duration(hrs)')
new_df['duration_plus_12hrs'] = new_df['duration(hrs)']+23
new_df = new_df.assign(storm_new=range(1,len(new_df)+1))
new_df.to_csv("storm_durations.csv")

#convert merged_df to csv file
final_df.to_csv("full_storm_range.csv", index = False)










       
        