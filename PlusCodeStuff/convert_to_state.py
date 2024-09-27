import geopandas as gpd
from shapely.geometry import Point
from openlocationcode import openlocationcode as olc
import numpy as np

# Load the GeoJSON of DRC provinces
gdf = gpd.read_file("gadm41_COD_1.json")

# Define a function to create a grid of lat/lon points
def generate_grid(min_lat, max_lat, min_lon, max_lon, step_size):
    latitudes = np.arange(min_lat, max_lat, step_size)
    longitudes = np.arange(min_lon, max_lon, step_size)
    return [(lat, lon) for lat in latitudes for lon in longitudes]

# Generate grid for DRC (coordinates are approximate)
min_lat, max_lat = -13.459, 5.354
min_lon, max_lon = 12.039, 31.305
grid_points = generate_grid(min_lat, max_lat, min_lon, max_lon, 0.01)

# Generate Plus Codes and map to provinces
plus_codes_by_province = {}

for lat, lon in grid_points:
    point = Point(lon, lat)
    plus_code = olc.encode(lat, lon)
    
    # Check which province this point belongs to
    for idx, row in gdf.iterrows():
        if row['geometry'].contains(point):
            province_name = row['name']  # Assumed column name for province
            if province_name not in plus_codes_by_province:
                plus_codes_by_province[province_name] = []
            plus_codes_by_province[province_name].append(plus_code)
            break





# import geopandas as gpd
# from shapely.geometry import Point
# import openlocationcode as olc
# import csv

# # Load the GeoJSON of DRC provinces
# gdf = gpd.read_file("path_to_drc_provinces.geojson")

# # Define a function to create a grid of lat/lon points
# def generate_grid(min_lat, max_lat, min_lon, max_lon, step_size):
#     latitudes = np.arange(min_lat, max_lat, step_size)
#     longitudes = np.arange(min_lon, max_lon, step_size)
#     return [(lat, lon) for lat in latitudes for lon in longitudes]

# # Generate grid for DRC (coordinates are approximate)
# min_lat, max_lat = -13.459, 5.354
# min_lon, max_lon = 12.039, 31.305
# grid_points = generate_grid(min_lat, max_lat, min_lon, max_lon, 0.01)

# # Open CSV file for writing
# with open('pluscodes_drc.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     # Write CSV header
#     writer.writerow(['pluscode', 'polygon', 'state'])

#     # Iterate over grid points
#     for lat, lon in grid_points:
#         point = Point(lon, lat)
#         plus_code = olc.encode(lat, lon)
        
#         # Check which province this point belongs to
#         for idx, row in gdf.iterrows():
#             if row['geometry'].contains(point):
#                 province_name = row['name']  # Assumed column name for province/state
#                 polygon_wkt = row['geometry'].wkt  # Convert polygon to WKT format

#                 # Write the Plus Code, Polygon WKT, and Province to the CSV file
#                 writer.writerow([plus_code, polygon_wkt, province_name])
#                 break  # Exit after finding the matching province