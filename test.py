import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Load data
populationData = pd.read_json("populationData.json")
healthCareFacilities = pd.read_json("healthCare.json") 
geographicalArea = gpd.read_file("geographicalArea.geojson")

# Convert to GeoDataFrame
facilities_gdf = gpd.GeoDataFrame(
    healthCareFacilities,
    geometry=gpd.points_from_xy(healthCareFacilities.Longitude, healthCareFacilities.Latitude),
    crs="EPSG:4326"
)

# Make sure CRS matches county map
facilities_gdf = facilities_gdf.to_crs(geographicalArea.crs)


coords = np.column_stack((facilities_gdf.geometry.x, facilities_gdf.geometry.y))


db = DBSCAN(eps=0.02, min_samples=2).fit(coords)  
facilities_gdf['cluster'] = db.labels_


fig, ax = plt.subplots(figsize=(10,10))

# Plot county boundary
geographicalArea.plot(ax=ax, color='white', edgecolor='black')

# Plot clustered facilities (clustered points)
facilities_gdf[facilities_gdf['cluster'] >= 0].plot(
    ax=ax,
    color='blue',
    markersize=50,
    label='Facility Cluster'
)

# Plot noise points (potential underserved areas)
facilities_gdf[facilities_gdf['cluster'] == -1].plot(
    ax=ax,
    color='red',
    markersize=50,
    label='Potential Underserved'
)

plt.legend()
plt.title("Healthcare Facility Clusters in DeKalb County")
plt.show()
