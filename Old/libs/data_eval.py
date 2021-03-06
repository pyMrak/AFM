# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 12:37:43 2017

@author: andmra2
"""
from os.path import getsize


def checkForDataErrors(gdat, path):
    #print('datalen:', len(gdat.data))
    for m, meas in enumerate(gdat.data):
        #print('started', m)
        mStart = False
        mCount = 0
        startT = []
        durTime = []
        average = []
        size = getsize(path+gdat.filenames[m]+'.txt')
        for i, Volt in enumerate([item[1] for item in meas][1:-1:10]):
            Volt = float(Volt)
            if Volt > 1 and not mStart:
                mStart = True
                mStTime = i
                startT.append(float(meas[i*10+1][3]))
                mCount += 1
                avg = 0
            if mStart:
                if Volt < 1:
                    durTime.append(i-mStTime)
                    mStart = False
                    average.append(avg / durTime[-1])
                else:
                    avg += Volt
        if mStart:
            for j, Volt in enumerate([item[1] for item in meas][-20:-1]):
                if Volt < 1:
                    durTime.append(gdat.MeasDur*10-20+j-mStTime)
                    mStart = False
        if mStart:
            durTime.append(gdat.maxlines/10-mStTime)
        average.append(avg / (i-mStTime))
        if gdat.maxlines < 7000: 
            if size > 300000:
                print('!!!Warning!!! Not typical file size detected - File', gdat.filenames[m]+'.txt is too large')
        elif size > 1200000:
            print('!!!Warning!!! Not typical file size detected - File', gdat.filenames[m]+'.txt is too large')
        if size < 200000:
            print('!!!Warning!!! Not typical file size detected - File', gdat.filenames[m]+'.txt is too small')
        if mCount == 0:
            print('!!!Warning!!! Not typical measurement detected - No voltage or very low voltage in measurement', gdat.filenames[m])
        elif mCount > 1:
            print('!!!Warning!!! Not typical measurement detected - Multiple measurements in measurement', gdat.filenames[m])
        else:
            if durTime[0] < gdat.MeasDur*10-5:
                print('!!!Warning!!! Not typical measurement detected - Measurement', gdat.filenames[m], 'is shorter than expected')
                print(durTime[0], gdat.MeasDur)
            
            if average[0] < 4:
                print('!!!Warning!!! Not typical measurement detected - Not usual  voltage profile in measurement', gdat.filenames[m])
            if startT[0] > 710:
                print('!!!Warning!!! Not typical measurement detected - Too high start temperature in measurement', gdat.filenames[m])
        #print('ended', m)

      
def findMeasStart(measurements):
    MesStart = []
    for measurement in measurements:
        for pos, title in enumerate(measurement[0]):
            if title == 'U[V]':
                break
        for t, sample in enumerate(measurement[1:]):
                if sample[pos] > 1:
                    MesStart.append(t)
                    break
    return MesStart 