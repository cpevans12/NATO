#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 13:36:21 2023

@author: cpe28
"""

import wget
import os

def get_data(var,experiment,model,run,yr1,yr2,lat1,lat2,lon1,lon2,grid):
    for i in range(int(yr1),int(yr2)+1):
        file = 'https://ds.nccs.nasa.gov/thredds2/ncss/AMES/NEX/GDDP-CMIP6/'+str(model)+'/'+str(experiment)+'/'+str(run)+'/'+str(var)+'/'+str(var)+'_day_'+str(model)+'_'+str(experiment)+'_'+str(run)+'_'+str(grid)+'_'+str(i)+'.nc?var='+str(var)+'&north='+str(lat2)+'&west='+str(lon1)+'&east='+str(lon2)+'&south='+str(lat1)+'&horizStride=1&time_start='+str(i)+'-01-01T12%3A00%3A00Z&time_end='+str(i)+'-12-31T12%3A00%3A00Z&timeStride=1'
        wget.download(file)

models = ["ACCESS-CM2","ACCESS-ESM1-5","BCC-CSM2-MR","CMCC-CM2-SR5","CMCC-ESM2","CNRM-CM6-1","CNRM-ESM2-1","CanESM5","EC-Earth3","FGOALS-g3","GFDL-CM4","GFDL-ESM4","INM-CM4-8","INM-CM5-0","IPSL-CM6A-LR","MIROC-ES2L","MIROC6","MPI-ESM1-2-HR","MPI-ESM1-2-LR","MRI-ESM2-0","NESM3","NorESM2-LM","NorESM2-MM","TaiESM1"]

var = 'tasmax'
experiment = 'ssp585'

for i in models:
    if i in {'CESM2-WACCM','FGOALS-g3'}:
        run = 'r3i1p1f1'
    elif i == 'CESM2':
        run = 'r4i1p1f1'
    elif i in {'HadGEM3-GC31-MM', 'HadGEM3-GC31-LL'}:
        run = 'r1i1p1f3'
    elif i in {'CNRM-CM6-1', 'CNRM-ESM2-1','GISS-E2-1-G','MIROC-ES2L','UKESM1-0-LL'}:
        run = 'r1i1p1f2'
    else:
        run = 'r1i1p1f1'
    
    if i in {"ACCESS-CM2","ACCESS-ESM1-5","BCC-CSM2-MR","CanESM5","CESM2-WACCM","CESM2","CMCC-CM2-SR5","CMCC-ESM2","FGOALS-g3","GISS-ES-1-G","HadGEM3-GC31-LL","HadGEM3-GC-31-MM","IITM-ESM","MIROC-ES2L","MIROC6","MPI-ESM1-2-HR","MPI-ESM1-2-LR","MRI-ESM2-0","NESM3","NorESM2-LM","NorESM2-MM","TaiESM1","UKESM1-0-LL"}:
        grid = "gn"
    elif i in {"CNRM-CM6-1","CNRM-ESM1-1","EC-Earth3-Veg-LR","EC-Earth3","IPSL-CM6A-LR","KACE-1-0-G"}:
        grid = "gr"
    elif i in {"GFDL-CM4","GFDL-ESM4","INM-CM4-8","INM-CM5-0","KIOST-ESM"}:
        grid = "gr1"
    elif i in {"GFDL-CM4_gr2"}:
        grid = "gr2"
        
    get_data(var,experiment,i,run,2050,2059,29.,37.4,38.75,48.5,grid)
    
    for k in range(10):
        os.rename("tasmax_tasmax_day_"+str(i)+'_ssp585_'+str(run)+'_'+str(grid)+'_'+str(2050+k)+'.nc', "IRAQ_tasmax_day_"+str(i)+'_ssp585_'+str(run)+'_'+str(grid)+'_'+str(2050+k)+'.nc')
