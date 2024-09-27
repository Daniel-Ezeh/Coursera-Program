import geopandas as gpd

# Load the shapefile for the DRC
shapefile_path = 'gadm41_COD_shp.zip'  # replace with actual path
drc_boundary = gpd.read_file(shapefile_path)

# List of required provinces
required_provinces = [
    'Kinshasa', 'Kongo Central', 'Kwango', 'Kwilu', 'Mai-Ndombe',
    'Kasaï', 'Kasaï-Central', 'Kasaï-Oriental', 'Lomami', 'Sankuru',
    'Maniema', 'South Kivu', 'North Kivu', 'Ituri', 'Haut-Uele', 'Tshopo',
    'Bas-Uele', 'Nord-Ubangi', 'Mongala', 'Sud-Ubangi', 'Équateur',
    'Tshuapa', 'Tanganyika', 'Haut-Lomami', 'Lualaba', 'Haut-Katanga'
]

# Filter the provinces you need
filtered_provinces = drc_boundary[drc_boundary['NAME_1'].isin(required_provinces)]

# Display the filtered provinces
print(filtered_provinces)