import fnmatch
import gzip
import numpy as np
import pandas as pd
import math
import os

maxdfall = pd.DataFrame(columns=['HOST', 'T', 'TIME', 'DATE', 'CPUBUSY', 'MEMUSED'])

lastTIME = ''
startdate = ''
enddate = ''

def linesearcher(lines):
    buildrow = []
    utildf = pd.DataFrame(columns=['HOST', 'T', 'TIME', 'DATE', 'CPUBUSY', 'MEMUSED'])
    matchlist = ["AAA,host*", "ZZZZ,T*", "CPU_ALL,T*", "MEM,T*"]
    for line in lines:
        line = line.strip()
        for match in matchlist:
            if fnmatch.fnmatch(line, match):
                ticks = line.split(',')
                linelist = np.array(ticks).tolist()
                if linelist[0] == 'AAA':
                    hostname = linelist[2]

                if linelist[0] == 'ZZZZ':
                    global startdate
                    global enddate
                    startdate = linelist[3]
                    if enddate == '':
                        enddate = startdate
                    buildrow.append(hostname)
                    buildrow.append(linelist[1])
                    buildrow.append(linelist[2])
                    global lastTIME
                    if startdate == enddate:  # stay in the same day
                        lastTIME = linelist[2]
                    buildrow.append(linelist[3])

                if linelist[0] == 'CPU_ALL':
                    buildrow.append(linelist[6])
                if linelist[0] == 'MEM':
                    buildrow.append(100 - float(linelist[2]))

                    if startdate == enddate:  # make sure we're not appending data from next day
                        utildf = utildf.append(dict(zip(utildf.columns, buildrow)), ignore_index=True)
                    # drop rows outside of the 24 hour day
                    # get first date and remove any recs not matching
                    # firstdate = utildf['DATE'].iloc[0]
                    # utildf = utildf[utildf.DATE == firstdate]

                    buildrow = []
    enddate = ''
    hourloop(utildf)

def hourloop(utildf):
    global lastTIME
    for hour in range(0, int(lastTIME.split(':')[0]) + 1):
        tempdf = pd.DataFrame(columns=utildf.columns)
        tempdf = (utildf[utildf['TIME'].str.match(str(hour).zfill(2) + ':')])  # get only records that match current hour format  e.g. 00:
        tempdf.reset_index(inplace=True, drop=True)
        maxdf = pd.DataFrame(columns=utildf.columns)
        maxdf = maxdf.append(tempdf[tempdf['TIME'].str.match(str(hour).zfill(2) + ':')].loc[0])  # get the first record in tempdf
        maxdf.reset_index(inplace=True, drop=True)
        maxdf['CPUBUSY'].loc[0] = tempdf['CPUBUSY'].max()  # get the max from the current hour records
        maxdf['MEMUSED'].loc[0] = tempdf['MEMUSED'].max()  # get the max from the current hour records
        global maxdfall
        maxdfall = maxdfall.append(maxdf)  #dataframe of the hourly rows by date with max util values for each hour

        del maxdf
        del tempdf

    maxdfall.reset_index(inplace=True, drop=True)
    return (maxdfall.to_csv('nmondata_May2019.csv'))

for file in os.listdir('/tmp/NMON/'):
    if fnmatch.fnmatch(file, '*.nmon.gz'):
        with gzip.open('/tmp/NMON/' + file, mode='rt', encoding='UTF-8') as nmonfile:
            #nfile = nmonfile.read().decode('utf-8')
            lines = ''
            lines = nmonfile.readlines()
            print(lines)
            linesearcher(lines)
    if fnmatch.fnmatch(file, '*.nmon'):
        with open('/tmp/NMON/' + file, "r", ) as nmonfile:
            lines = ''
            lines = nmonfile.readlines()
            #print(lines)
            linesearcher(lines)
