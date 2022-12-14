
import numpy as np
import os
from netCDF4 import Dataset
from datetime import datetime, timezone
import pytz
from datetime import timedelta
import pandas as pd

def datenum_to_datetime(datenum):
    """
    Convert Matlab datenum into Python datetime.
    :param datenum: Date in datenum format
    :return:        Datetime object corresponding to datenum.
    """
    days = datenum % 1
    hours = days % 1 * 24
    minutes = hours % 1 * 60
    seconds = minutes % 1 * 60
    return datetime.fromordinal(int(datenum)) \
           + timedelta(days=int(days)) \
           + timedelta(hours=int(hours)) \
           + timedelta(minutes=int(minutes)) \
           + timedelta(seconds=round(seconds)) \
           - timedelta(days=366)

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def getWIS(file):
    waves = Dataset(file)

    waveHs = waves.variables['waveHs'][:]
    waveTp = waves.variables['waveTp'][:]
    waveMeanDirection = waves.variables['waveMeanDirection'][:]
    waveTm = waves.variables['waveTm'][:]
    waveTm1 = waves.variables['waveTm1'][:]
    waveTm2 = waves.variables['waveTm2'][:]
    waveHsWindsea = waves.variables['waveHsWindsea'][:]
    waveTmWindsea = waves.variables['waveTmWindsea'][:]
    waveMeanDirectionWindsea = waves.variables['waveMeanDirectionWindsea'][:]
    waveSpreadWindsea = waves.variables['waveSpreadWindsea'][:]
    timeW = waves.variables['time'][:]
    waveTpSwell = waves.variables['waveTpSwell'][:]
    waveHsSwell = waves.variables['waveHsSwell'][:]
    waveMeanDirectionSwell = waves.variables['waveMeanDirectionSwell'][:]
    waveSpreadSwell = waves.variables['waveSpreadSwell'][:]

    output = dict()
    output['waveHs'] = waveHs
    output['waveTp'] = waveTp
    output['waveMeanDirection'] = waveMeanDirection
    output['waveTm'] = waveTm
    output['waveTm1'] = waveTm1
    output['waveTm2'] = waveTm2
    output['waveTpSwell'] = waveTpSwell
    output['waveHsSwell'] = waveHsSwell
    output['waveMeanDirectionSwell'] = waveMeanDirectionSwell
    output['waveSpreadSwell'] = waveSpreadSwell
    output['waveHsWindsea'] = waveHsWindsea
    output['waveTpWindsea'] = waveTmWindsea
    output['waveMeanDirectionWindsea'] = waveMeanDirectionWindsea
    output['waveSpreadWindsea'] = waveSpreadWindsea
    output['t'] = timeW

    return output

# Change path to where you put WIS data and your desired output directory of csv
wavedir = r"\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\0. Get WIS data\WIS files"
outputdir = r"C:\Users\smrosen2\Desktop\Mirlo Beach\Hypothetical Storms\Dylan method\0. Get WIS data"


# LOADING THE WIS FILES
# Need to sort the files to ensure correct temporal order...
waveFiles = os.listdir(wavedir)
waveFiles.sort()
waveFiles_path = [os.path.join(os.path.abspath(wavedir), x).replace("\\", "/") for x in waveFiles]
Hs = []
Tp = []
Dm = []
timeWave = []
for i in waveFiles_path:
    waves = getWIS(i)
    Hs = np.append(Hs,waves['waveHs'])
    Tp = np.append(Tp,waves['waveTp'])
    Dm = np.append(Dm,waves['waveMeanDirection'])
    timeWave = np.append(timeWave,waves['t'].flatten())

# tWave = [DT.datetime.fromtimestamp(x) for x in timeWave]
tWave = [datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M") for x in timeWave]
# CONVERT TO GMT (same string type and format as above)
tWave = [datetime.strptime(x,"%Y-%m-%d %H:%M").astimezone(pytz.UTC).strftime("%Y-%m-%d %H:%M") for x in tWave]
tC = np.array(tWave)

### create csv with all WIS data and time steps --> corrected to UTC with above timestep correction
time=[]
for i in tWave:
    time.append(i)
        
waveHs=[]
for i in Hs:
    waveHs.append(i)
    
waveTp=[]
for i in Tp:
    waveTp.append(i)
    
waveDm=[]
for i in Dm:
    waveDm.append(i)    

# create csv with data by hour       
df = pd.DataFrame({'time': time, 'Hs': waveHs, 'Tp': waveTp, 'Dm': waveDm}, columns = ['time', 'Hs', 'Tp', 'Dm'])
savepath = os.path.join(outputdir,"full_WIS_time_series_UTC.csv")
df.to_csv(savepath)




