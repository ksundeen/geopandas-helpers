#!/usr/bin/env python
# coding: utf-8

''' PURPOSE: Convert csv to geojson with latlong fields in the CSV.'''

import pandas as pd
import geopandas as gpd
import datetime
import pytz
import time
import matplotlib.pyplot as plt

print(pd.__version__)


df = gpd.read_file('geopandas_input/sample.csv') 
df.crs = 'epsg:4326'

# Filter out empty rows without any geometries
df_clean = df[df['geolocation_longitude'] != '']
print(df_clean.count())

''' Use function (datetime.datetime(2019,12,1,0,0) - datetime.datetime(1970,1,1)).total_seconds() to convert to epoch. 
Found from 
https://www.delftstack.com/howto/python/python-datetime-to-epoch/#:~:text=Use%20the%20strftime%20%28format%29%20Function%20to%20Convert%20Datetime,of%20this%20process%2C%20strptime%20%28%29%20method%20is%20used.
'''

timestring = "2021-11-01T11:05:28.042Z"
# String formatting for dates: https://blog.logrocket.com/python-datetime-module-handling-dates-time/#:~:text=With%20the%20Python%20datetime%20module%2C%20you%20can%20write,main%20classes%2C%20date%2C%20time%2C%20tzinfo%2C%20DateTime%2C%20and%20timedelta.
# epochtime = datetime.datetime.strptime(locationDf["create_date"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()

# Function to calculate epoch datetime stamp to use as a joining unique ID
def to_epoch(date):
    # strip microseconds
    dateArr = date.split('.')
    no_microseconds_date = dateArr[0]
    #print(no_microseconds_date)
    new_time = datetime.datetime.strptime(no_microseconds_date, "%Y-%m-%dT%H:%M:%S")#.%fZ")
    return new_time.timestamp()

# Run a field calculate from the create_date to populate epoch_time field.
# locationDf["epoch_time"] =  datetime.datetime(1970,1,1,0,0,0).timestamp()
df_clean["epoch_time"] =  df_clean["create_date"].map(lambda x: to_epoch(x))

# once loaded, export to geojson
gdf = gpd.GeoDataFrame(df_clean, geometry=gpd.points_from_xy(df_clean['geolocation_longitude'], df_clean['geolocation_latitude']))
outfile = r"geopandas_output/location_nov2021_dec2021_joined_epic_nov2021_jan2022_v2.geojson"
gdf.to_file(outfile, driver='GeoJSON', encoding="utf-8")

# Plot locations using matplotlib
gdf.plot()