#!/usr/bin/env python
# coding: utf-8

''' PURPOSE: Loads geojson data as points, updates a column from another . 
Then converts gps timestamps to track lines.
'''

import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
from random import random

print(pd.__version__)


# Read in location point data
# gdf = gpd.read_file(r'geopandas_input/sample1.json')
gdf = gpd.read_file(r'geopandas_input/sample2.geojson')

# Populate new column in pandas geodataframe for the unique id
def getId(x):
    return x * int(random() * 100000)
gdf["unique_join_id"] =  gdf["id"].map(lambda x: getId(x) )

# Read in Units polygon
unitsDf = gpd.read_file(r'imdf/unit.geojson')
unitsDf_Level3 = unitsDf[unitsDf['level_id'] == '9C84FF15-CCC2-47B9-947F-EADBC1BA911C']

sortColumn = "create_date"
groupByColumn = "epicjobid" 

# Sort dataframe by the timestamp & reset index
sortedDf = gdf.sort_values(sortColumn).reset_index(drop=True)

# Group the points by the track 
# sortedDf_grouped = sortedDf.groupby(['user_id']).agg({'geometry':list})
sortedDf_grouped = sortedDf.groupby([groupByColumn]).agg({'geometry':list})

# Reset geometry to by looping through the grouped track ids & creating line strings
sortedDf_grouped['geometry'] = sortedDf_grouped['geometry'].apply(lambda x: LineString(x))

sortedDf_grouped_gdf = gpd.GeoDataFrame(sortedDf_grouped)

# outputFilepath = r"geopandas_output/user_id_location_track_lines.geojson"
outputFilepath = r"geopandas_output/sortBy" + sortColumn + "_groupByColumn" + groupByColumn + ".geojson"
sortedDf_grouped_gdf.to_file(outputFilepath, driver='GeoJSON', encoding="utf-8")
    


