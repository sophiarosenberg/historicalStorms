# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:23:08 2022

# This code:
1) pulls water level gauge data (both measured and predicted) for each storm time period 
(max sig wave heights, non-tidal residuals (surge), and storm durations), and
outputs a csv file with wave and water lvl data for each numbered storm)

Duck, NC Station 8651370
Range limit for data from NOAA site is 365 days

Help for tide analysis for csv: https://ocefpaf.github.io/python4oceanographers/blog/2014/07/07/pytides/

input: start date and end date
output: a separate csv file for each year between start and end date (saved to downloads)
save all tide files to single folder in working directory

Valid Date Format for web link is yyyyMMdd, MM/dd/yyyy, yyyyMMdd HH:mm, or MM/dd/yyyy HH:mm  
      
@author: smrosen2
"""
import webbrowser
import datetime


# Get start and end dates from user input
begin_date = input("Enter the start date in MM/DD/YYYY format: ") #01/01/1980
stop_date = input("Enter the end date in MM/DD/YYYY format: ")    #01/01/2021

# Set the time step (in days) between data downloads (if required)
delta = datetime.timedelta(days = 365) 
   
# Convert date string to datetime object using strptime ('string from time')
start_time = datetime.datetime.strptime(begin_date,"%m/%d/%Y") 
end_time = datetime.datetime.strptime(stop_date,"%m/%d/%Y") 


# Loop through to get seperate csv file for each 1 year time step (required by NOAA)
# This loop pulls both measured and predicted water levels and saves files to downloads
while start_time < end_time:
    # convert start date to correct format MM/dd/yyyy
    start_date = start_time.strftime('%m/%d/%Y')
    # set end date 1 year after start time
    end_date = (start_time + delta).strftime('%m/%d/%Y')
    # run the api browser to include string concatenated start and end dates specified above
    webbrowser.open('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date=' + str(start_date) + '%2001:00&end_date=' + str(end_date) + '%2011:00&datum=NAVD&station=8651370&time_zone=GMT&units=metric&interval=h&format=csv')
    webbrowser.open('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=' + str(start_date) + '%2001:00&end_date=' + str(end_date) + '%2011:00&datum=NAVD&station=8651370&time_zone=GMT&units=metric&interval=h&format=csv')
    # set new start_time to 1 year later; code will run until start_time reaches end_time
    start_time = start_time + delta
    














