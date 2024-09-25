import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from openlocationcode import openlocationcode as olc
import numpy as np
import pandas as pd


# Define a function to convert Plus Code to Polygon
def plus_code_to_polygon(plus_code):
    code_area = olc.decode(plus_code)
    sw_lat, sw_lng = code_area.latitudeLo, code_area.longitudeLo
    ne_lat, ne_lng = code_area.latitudeHi, code_area.longitudeHi

    # Define the polygon points
    polygon_points = [
        (sw_lng, sw_lat),  # SW
        (ne_lng, sw_lat),  # SE
        (ne_lng, ne_lat),  # NE
        (sw_lng, ne_lat),  # NW
        (sw_lng, sw_lat),  # Closing the loop to SW
    ]

    return Polygon(polygon_points)


drc_bounds = {
    "north": 5.392002,   # Northernmost point
    "south": -13.45835,  # Southernmost point
    "east": 31.305386,   # Easternmost point
    "west": 12.182336    # Westernmost point
}
# Decide on the level of precision (e.g., approximately 1km x 1km area)
step_lat = 0.009 
step_lng = 0.014

latitudes = np.arange(drc_bounds["south"], drc_bounds["north"], step_lat)
longitudes = np.arange(drc_bounds["west"], drc_bounds["east"], step_lng)

print('here')

plus_codes = []
for lat in latitudes:
    for lng in longitudes:
        code = olc.encode(lat, lng, 6)  # Adjust code_length as needed
        plus_codes.append(code)

plus_codes = list(set(plus_codes))
# Create the GeoDataFrame
data = {
    'plus_code': plus_codes,
    'geometry': [plus_code_to_polygon(code) for code in plus_codes]
}
plus_codes_gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

plus_codes_gdf['geometry_wkt'] = plus_codes_gdf['geometry'].apply(lambda x: x.wkt)

plus_codes_gdf.drop('geometry', axis=1, inplace=True)
plus_codes_gdf.to_csv('plus_codes_for_bigquery.csv', index=False)