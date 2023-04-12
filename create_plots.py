import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as NC
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.cm import get_cmap
from matplotlib.pyplot import cm
import glob

files = glob.glob("/Volumes/Elements/IRAQ/tas/*.nc")
files.sort()

data = NC.Dataset(files[0])
lat = np.array(data.variables['lat'])
lon = np.array(data.variables['lon'])
tas = np.array(data.variables['tas'])
tas[tas>500.] = np.nan
tas = tas-273.15


fig = plt.figure(figsize=(14,10))
ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
ax.set_extent([38.875,48.625,29.125,37.375],crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE,edgecolor='k',linewidth=0.5)
ax.add_feature(cfeature.BORDERS, edgecolor='k', linewidth=0.5)
ax.add_feature(cfeature.LAKES, edgecolor='k', linewidth=0.5,facecolor='none')
ax.add_feature(cfeature.LAND, edgecolor='k', linewidth=0.5,facecolor='none')
ax.gridlines()
plt.show()
plt.close()



days = [0,365,730,1096,1461,1826,2191,2557,2922,3287,3652]
all_data = np.empty([24,10,366])
for i in range(24):
    data = NC.Dataset(files[i])
    tas = np.array(data.variables['tas'])
    tas[tas>500.] = np.nan
    tas = tas-273.15

    if i in {0,1,5,6,8,14,16,17,18,19,20}:
        for j in range(10):
            if j in {2,6}:
                year = np.nanmean(tas[days[j]:days[(j+1)]],axis=(1,2))
                all_data[i,j,:] = year[:]
            else:
                year = np.nanmean(tas[days[j]:days[(j+1)]],axis=(1,2))
                all_data[i,j,0:365] = year[:]
    else:
        for j in range(10):
            year = np.nanmean(tas[(j*365):((j*365)+365)],axis=(1,2))
            all_data[i,j,0:365] = year[0:365]


all_data[all_data>100.] = np.nan

model_ens = np.nanmean(all_data,axis=1)
model_mean = np.nanmean(model_ens,axis=0)
model_std = np.nanstd(model_ens,axis=0)


day = [1,32,60,91,121,152,182,213,244,274,305,335]
models = ["ACCESS-CM2","ACCESS-ESM1-5","BCC-CSM2-MR","CMCC-CM2-SR5","CMCC-ESM2","CNRM-CM6-1","CNRM-ESM2-1","CanESM5","EC-Earth3","FGOALS-g3","GFDL-CM4","GFDL-ESM4","INM-CM4-8","INM-CM5-0","IPSL-CM6A-LR","MIROC-ES2L","MIROC6","MPI-ESM1-2-HR","MPI-ESM1-2-LR","MRI-ESM2-0","NESM3","NorESM2-LM","NorESM2-MM","TaiESM1"]

month=["January","February","March","April","May","June","July","August","September","October","November","December"]

color = iter(cm.tab20(np.linspace(0, 1, 24)))
fig = plt.figure(figsize=(10,8))
for i in range(24):
    plt.plot(model_ens[i,0:365],color=next(color),alpha = 1,lw=0.5,label=str(models[i]))
plt.plot(model_mean[0:365],color='k',lw=4,label = "Ens. Mean")
plt.plot(model_mean[0:365]+model_std[0:365],color='r',alpha=0.6,lw=3,label="Ens. STD")
plt.plot(model_mean[0:365]-model_std[0:365],color='r',alpha=0.6,lw=3)
plt.xlim(0,365)
plt.xticks([1,32,60,91,121,152,182,213,244,274,305,335],month,fontsize=15,rotation=45)
# plt.xlabel("Day of Year",fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel("Temp. (°C)",fontsize=15)
plt.legend(bbox_to_anchor=(1.05, 1),fontsize=10)
plt.title("Iraq Average Daily Temperature\nSSP585, 2050-2059",fontsize=20)
plt.savefig("iraq_temp_projections_v3.jpeg",dpi=500,bbox_inches='tight')
plt.show()
plt.close()



years = np.arange(2050,2060,1)


for i in range(10):
    fig = plt.figure(figsize=(10,8))
    color = iter(cm.tab20(np.linspace(0, 1, 24)))
    for j in range(24):
        plt.plot(all_data[j,i,0:365],color=next(color),label=str(models[j]),ls='--')
    plt.plot(np.nanmean(all_data[:,i,:],axis=0),color='k',lw=3,label="Ens. Mean")
    plt.xlim(0,365)
    plt.xticks([1,32,60,91,121,152,182,213,244,274,305,335],month,rotation=45,fontsize=15)
    # plt.xlabel("Day of Year",fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel("Temp. (°C)",fontsize=15)
    plt.legend(fontsize=15)
    plt.title("Iraq Daily Average Temperature\nSSP585: " + str(years[i]),fontsize=20)
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.savefig("iraq_temp_projections_v2_"+str(years[i])+".jpeg",dpi=500,bbox_inches='tight')
    plt.show()
    plt.close()

color = iter(cm.plasma(np.linspace(0, 1, 10)))
fig = plt.figure(figsize=(10,8))
for i in range(10):
    plt.plot(np.nanmean(all_data[:,i,0:365],axis=0),color=next(color),lw=2,label=str(years[i]))
plt.xlim(0,365)
plt.xticks([1,32,60,91,121,152,182,213,244,274,305,335],month,rotation=45,fontsize=15)
plt.xlabel("Day of Year",fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel("Temp. (°C)",fontsize=15)
plt.legend(fontsize=15)
plt.title("Iraq Daily Average Temperature\nSSP585 Ensemble Mean",fontsize=20)
plt.legend(bbox_to_anchor=(1.0, 1))
plt.savefig("iraq_temp_projections_yearly_mean_v2.jpeg",dpi=500,bbox_inches='tight')
plt.show()
plt.close()


color = iter(cm.tab20(np.linspace(0, 1, 24)))
fig = plt.figure(figsize=(10,8))
for i in range(24):
    plt.plot(np.nanmean(all_data[i,:,:],axis=1),color=next(color),label=str(models[i]),ls='--')
plt.plot(np.nanmean(all_data,axis=(0,2)),color='k',label='Ens. Mean',lw=4)
plt.legend(bbox_to_anchor=(1.05, 1))
plt.xticks(np.arange(10),np.arange(2050,2060),fontsize=15)
plt.xlim(0,9)
plt.yticks(fontsize=15)
plt.ylabel("Temp. (°C)",fontsize=15)
plt.title("Iraq Daily Average Temperature Time Series\nSSP585",fontsize=20)
plt.savefig("iraq_temp_projections_trends_v2.jpeg",dpi=500,bbox_inches='tight')
plt.show()
plt.close()


fig = plt.figure(figsize=(10,8))
color = iter(cm.tab20(np.linspace(0, 1, 24)))
for i in range (24):
    plt.plot(all_data[i,9,:]-all_data[i,0,:],color=next(color),ls='--',label=str(models[i]))
plt.plot(np.nanmean(all_data[:,9,:],axis=0)-np.nanmean(all_data[:,0,:],axis=0),color='k',ls='-',label='Ens. Mean')
plt.xlim(0,365)
plt.xticks([1,32,60,91,121,152,182,213,244,274,305,335],month,rotation=45,fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel("Temp. Difference (°C)",fontsize=15)
plt.legend(bbox_to_anchor=(1.05, 1))
plt.title("Iraq Temperature Change Projections\nSSp585 2059-2050",fontsize=20)
plt.savefig("iraq_temp_difference_v2.jpeg",dpi=500,bbox_inches='tight')
plt.show()
plt.close()


day = [1,32,60,91,121,152,182,213,244,274,305,335]
jan = all_data[:,:,0:31]
feb = all_data[:,:,31:59]
march = all_data[:,:,59:90]
april = all_data[:,:,90:121]
may = all_data[:,:,121:151]
june = all_data[:,:,151:181]
july = all_data[:,:,181:212]
august = all_data[:,:,212:243]
september = all_data[:,:,243:273]
october = all_data[:,:,273:304]
november = all_data[:,:,304:334]
december = all_data[:,:,334:365]
months = [jan,feb,march,april,may,june,july,august,september,october,november,december]
month=["January","February","March","April","May","June","July","August","September","October","November","December"]

monthly_data = np.empty([12,3])
for i in range(12):
    monthly_data[i,0] = np.nanmean(months[i])
    monthly_data[i,1] = np.nanmin(months[i])
    monthly_data[i,2] = np.nanmax(months[i])


fig = plt.figure(figsize = (10, 5))
plt.bar(np.arange(12),monthly_data[:,2],color='tab:red',label='Max. Temp.')
plt.bar(np.arange(12),monthly_data[:,0],color='tab:green',label='Mean Temp.')
plt.bar(np.arange(12),monthly_data[:,1],color='tab:cyan', label='Min. Temp.')
plt.legend()
plt.xticks(np.arange(12),month,rotation=45,fontsize=12)
plt.yticks(fontsize=12)
plt.ylabel("Temp. (°C)",fontsize=12)
plt.ylim(-1,50)
plt.title("Iraq Daily Temperature Projections\nSSP585 2050s",fontsize=15)
plt.savefig("iraq_bar_plot.jpeg",dpi=500,bbox_inches='tight')
plt.show()
plt.close()

all_data = np.empty([24,3652,34,40])
for i in range(24):
    data = NC.Dataset(files[i])
    tas = np.array(data.variables['tas'])
    tas[tas>500.] = np.nan
    tas = tas-273.15
    
    if i in {0,1,5,6,8,14,15,16,17,18,19,20}:
        all_data[i,:,:] = tas
    else:
        all_data[i,0:3650,:,:] = tas



all_data[all_data>100.] = np.nan

# days = [0,365,730,1096,1461,1826,2191,2557,2922,3287,3652]
levels = np.arange(10,30.1,0.1)
fig = plt.figure(figsize=(14,10))
ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
ax.set_extent([38.875,48.625,29.125,37.375],crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE,edgecolor='k',linewidth=0.5)
ax.add_feature(cfeature.BORDERS, edgecolor='k', linewidth=0.5)
ax.add_feature(cfeature.LAKES, edgecolor='k', linewidth=0.5,facecolor='none')
ax.add_feature(cfeature.LAND, edgecolor='k', linewidth=0.5,facecolor='none')
ax.gridlines()
cb = plt.contourf(lon,lat,np.nanmean(all_data[:,3287::,:,:],axis=(0,1)),levels,transform=ccrs.PlateCarree(),cmap=get_cmap("jet"),extend='both')
cbar = plt.colorbar(cb,orientation="vertical",label="Temp. (°C)")
ax.set_xticks([40., 42., 44.,46.], crs=ccrs.PlateCarree())
ax.set_xticklabels(["40°E", "42°E", "44°E","46°E"],fontsize=15)
ax.set_yticks([30.,32.,34.,36.], crs=ccrs.PlateCarree())
ax.set_yticklabels(["30°N","32°N","34°N","36°N"],fontsize=15)
ax.yaxis.tick_left()
plt.title("Iraq Ensemble Daily Average Temperature\n2059",fontsize=20)
plt.savefig("iraq_2059_map.jpeg",dpi=500,bbox_inches='tight')
plt.show()
plt.close()







# =============================================================================
# tasmax
# =============================================================================
# =============================================================================
files = glob.glob("/Volumes/Elements/IRAQ/tasmax/*.nc")
files.sort()

data = NC.Dataset(files[0])
lat = np.array(data.variables['lat'])
lon = np.array(data.variables['lon'])
tasmax = np.array(data.variables['tasmax'])
tasmax[tasmax>500.] = np.nan
tasmax = tasmax-273.15


days = [0,365,730,1096,1461,1826,2191,2557,2922,3287,3652]
all_data = np.empty([24,10,366])
for i in range(24):
    data = NC.Dataset(files[i])
    tasmax = np.array(data.variables['tasmax'])
    tasmax[tasmax>500.] = np.nan
    tasmax = tasmax-273.15

    if i in {0,1,5,6,8,14,16,17,18,19,20}:
        for j in range(10):
            if j in {2,6}:
                year = np.nanmean(tasmax[days[j]:days[(j+1)]],axis=(1,2))
                all_data[i,j,0:366] = year[:]
            else:
                year = np.nanmean(tasmax[days[j]:days[(j+1)]],axis=(1,2))
                all_data[i,j,0:365] = year[:]
    else:
        for j in range(10):
            year = np.nanmean(tasmax[(j*365):((j*365)+365)],axis=(1,2))
            all_data[i,j,0:365] = year[0:365]

all_data[all_data>100.] = np.nan
all_data_mean = np.nanmean(all_data,axis=0)

heat_stress = np.empty([24,10])
for i in range(24):
    for j in range(10):
        count = np.count_nonzero(all_data[i,j,0:365]>43.3)
        heat_stress[i,j] = count

color = iter(cm.tab20(np.linspace(0, 1, 24)))
fig = plt.figure(figsize=(10,8))
for i in range(23):
    plt.plot(heat_stress[i,:],color=next(color),label=str(models[i]),ls='--')
plt.plot(np.nanmean(heat_stress,axis=0),color='k',lw=3,label="Ens. Mean")
plt.plot()
plt.legend(bbox_to_anchor=(1.0, 1))
plt.ylabel("Number of Days",fontsize=15)
plt.xticks(np.arange(10),np.arange(2050,2060),fontsize=15)
plt.title("Iraq Heat Stress Projections\nSSP585 2050s",fontsize=20)
plt.savefig("iraq_heat_stress.jpeg",dpi=500,bbox_inches='tight')
plt.show()
plt.close()
