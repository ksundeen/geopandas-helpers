#!/usr/bin/env python
# coding: utf-8

# Run export of CSV file from mongdodb
# 
# 1. 

# In[ ]:


import pandas as pd
import geopandas as gpd
print(pd.__version__)


# In[ ]:


df = gpd.read_file('geopandas_input/locations_jan_2022.csv') 
df.crs = 'epsg:4326'
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['geolocation.longitude'], df['geolocation.latitude']))
outfile = r"geopandas_output/jobid_location_track_lines.geojson"
gdf .to_file(outfile, driver='GeoJSON', encoding="utf-8")

