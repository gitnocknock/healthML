import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# Read the JSON file with Population Data
populationData = pd.read_json("populationData.json")
healthCareFacilities = pd.read_json("healthCare.json") 
geographicalArea = gpd.read_file("geographicalArea.geojson")

# Convert Data into a more readable format
df_population = pd.DataFrame(populationData)
df_geoData = gpd.GeoDataFrame(geographicalArea) # Adds Geometary Spatial Data Column

# Convert to GeoDataFrame
facilities_gdf = gpd.GeoDataFrame(
    healthCareFacilities,
    geometry=gpd.points_from_xy(healthCareFacilities.Longitude, healthCareFacilities.Latitude),
    crs="EPSG:4326"
)
# Convert facilities to match county CRS
facilities_gdf = facilities_gdf.to_crs(geographicalArea.crs)

# Plot the geographical area and healthcare facilities
ax = geographicalArea.plot(edgecolor='black', facecolor='none')
facilities_gdf.plot(ax=ax, color='red', markersize=50)

plt.show()