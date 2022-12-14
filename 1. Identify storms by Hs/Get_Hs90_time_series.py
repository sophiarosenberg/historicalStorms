# -*- coding: utf-8 -*-
"""
Created on Thursday Nov 3 09:58:28 2022
before running this code, comment out bottom section


@author: smrosen2
"""
import pandas as pd
import os
import numpy as np

# Station: Nags Head, Duck, Station 


## Assign name to csv file with full WIS wave data from 1/1/1980-1/1/2020 
Hs_file = r"\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\0. Get WIS data\full_WIS_time_series_UTC.csv"
outputdir = r"\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\1. Identify storms based on Hs - updated"

## Create panda data frame of all wave data and TWL
df = pd.read_csv(Hs_file)


# Keep rows with Hs > Hs90 threshold
# determines threshold by finding 90th percentile (highest 10% of wave heights) from full WIS dataset
Hs = []
for index, row in df.iterrows():    
    Hs.append(float(row['Hs']))

hs90 = np.nanpercentile(Hs,90)
print ("90th percentile Hs: ", hs90, " meters")

df2 = df[df.Hs > hs90]

# save to csv
savepath = os.path.join(outputdir,"Hs90_time_series.csv")
df2.to_csv(savepath)

# Save csv as an excel spreadsheet and group storms within 1 day:
# 1) Create a new column named “storm”
# 2) In first row entry, put a 1
# 3) In next row entry, type this IF statement: =IF((C3-C2)<1,D2,D2+1)
#       C1 = time
#       D1 = storm header
#       Apply to rest of column
# This IF statement gives a consecutive storm number to each storm in dataset based on hourly time intervals breaking in between separate storm events
# if two rows are more than a day apart, they are separated into separate storms

### After doing the above steps, run "Get_storms_12hrs.py"



































