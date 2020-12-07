#!/usr/bin/env python
# coding: utf-8


# import of standard Python libraries for data analysis
import pandas as pd
import numpy as np
from datetime import datetime

# import of libraries for handling netCDF files and file paths 
import netCDF4 as nc
from netCDF4 import Dataset
import glob
import xarray as xr
import pathlib

# import function meteo_paths to iterate over years
from year_select import meteo_paths

#starting year
year = 2010

# for loop to iterate over years and change selected year to Pandas dataframe
for meteo_path in meteo_paths():
    meteo_dataset = nc.Dataset(meteo_path)
    ds_meteo = xr.open_dataset(meteo_path)
    ds_meteo = ds_meteo.to_dataframe()

# removing columns not needed for analysis
    ds_meteo = ds_meteo.drop(columns=['aspect', 'slope', 'LWdown', 'Wind_DIR', 'DIR_SWdown', 'SCA_SWdown', 'LAT', 'LON', 
                                              'FRC_TIME_STP', 'ZREF', 'UREF', 'CO2air', 'Rainf'])
# changing names of columns to something more clear
    ds_meteo.columns = ["elevation", "massif_num", "surface_air_pressure", "air_temp",
                           "near_surface_humidity", "wind_speed", 
                           "snowfall_rate", "nebulosity", "relative_humidity",  
                            "freezing_level_altitude", "rain_snow_transition_altitude"]


# massif with num 30 is most likely mistake, because its latitude and longitude is outside France
# I decided to remove massif 30 from dataset
    ds_meteo = ds_meteo[ds_meteo["massif_num"]<30.0]
    ds_meteo.massif_num.nunique()

# Number of patches is not interesting for my analysis and massif as index is redundant
# therefore I decided to remove this info from my dataset
    ds_meteo.index = ds_meteo.index.droplevel(level = (0, 1))
    ds_meteo = ds_meteo.reset_index()

# change of day from string to datetime
    ds_meteo["day"] = ds_meteo.time.dt.date

# removing redundant varible time
    ds_meteo = ds_meteo.drop(columns=['time'])

# reducing variables to those we will need later on
    meteo_all = ds_meteo[["elevation", "massif_num", 'surface_air_pressure', 'air_temp',
           'near_surface_humidity', 'wind_speed', 'snowfall_rate',
           'nebulosity', 'relative_humidity', 'freezing_level_altitude',
           'rain_snow_transition_altitude', 'day']]

# creating new dataframe with only variables where I am interested in its mean
    meteo_mean = meteo_all[["elevation", "massif_num", 'day', 'surface_air_pressure',
           'near_surface_humidity', 'relative_humidity', 'freezing_level_altitude',
           'rain_snow_transition_altitude']]
# creating new dataframes with only variables where I am interested in its max and min
    meteo_max = meteo_all[["elevation", "massif_num", 'day', 'air_temp', 
                           'wind_speed', 'snowfall_rate','nebulosity']]
    meteo_min = meteo_all[["elevation", "massif_num", 'day', 'air_temp']]

# transforming variables to its mean, max and min values for certain day, massif and elevation
    meteo_mean = meteo_mean.groupby(['elevation','day', 'massif_num']).mean()
    meteo_max = meteo_max.groupby(['elevation','day', 'massif_num']).max()
    meteo_min = meteo_min.groupby(['elevation','day', 'massif_num']).min()

# merge of mean and max dataframe into one dataframe
    meteo1 = meteo_mean.merge(meteo_max, how="inner", left_on=meteo_mean.index.to_numpy(), right_on=meteo_max.index.to_numpy())
# merge with min dataframe
    meteo = meteo1.merge(meteo_min, how="inner", left_on="key_0", right_on=meteo_min.index.to_numpy())

# changing names of columns to add info about mean, max or min
    meteo.columns = ['elevation_day_massif_num', 'surface_air_pressure_mean', 'near_surface_humidity_mean',
           'relative_humidity_mean', 'freezing_level_altitude_mean',
           'rain_snow_transition_altitude_mean', 'air_temp_max', 'wind_speed_max',
           'snowfall_rate_max', 'nebulosity_max', 'air_temp_min']

# changing former multiindex of dataframe to list in order to separete 3 different variables
    meteo.elevation_day_massif_num = meteo.elevation_day_massif_num.apply(lambda x: list(x))

# separation of 3 variables previously included in multiindex
    meteo["elevation"] = meteo.elevation_day_massif_num.apply(lambda x: x[0])
    meteo["day"] = meteo.elevation_day_massif_num.apply(lambda x: x[1])
    meteo["massif"] = meteo.elevation_day_massif_num.apply(lambda x: x[2])

# removing redundant column
    meteo = meteo.drop(columns=['elevation_day_massif_num'])

# saving final dataframe to csv file
    meteo_final = meteo.to_csv(r'.\\meteo_csv_files\meteo_'+str(year)+'.csv', index = False)

 # year increment
    year += 1
