import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Load data
healthCareFacilities = pd.read_json("data/healthCare.json")
geographicalArea = gpd.read_file("data/geographicalArea.geojson")
zcta = gpd.read_file("data/tl_2025_us_zcta520/tl_2025_us_zcta520.shp")
population_df = pd.read_csv("data/dekalb_population.csv")

# Filter Georgia ZCTAs
georgia_zcta = zcta[zcta['ZCTA5CE20'].str.startswith(('30','31'))]

# All DeKalb ZIP codes
dekalb_zips = [
    '30002','30012','30021','30030','30032','30033','30034','30035',
    '30038','30039','30058','30079','30083','30084','30087','30088',
    '30094','30288','30294','30306','30307','30315','30316','30317',
    '30319','30322','30324','30328','30329','30338','30340','30341',
    '30345','30346','30350','30360'
]

# Filter ZCTAs for DeKalb
dekalb_zcta = georgia_zcta[georgia_zcta['ZCTA5CE20'].isin(dekalb_zips)]

# Make sure ZIP codes are string type for merging
dekalb_zcta['ZCTA5CE20'] = dekalb_zcta['ZCTA5CE20'].astype(str)
population_df['ZCTA5CE20'] = population_df['ZCTA5CE20'].astype(str)

# Merge population data into ZCTA GeoDataFrame
dekalb_zcta = dekalb_zcta.merge(population_df, on='ZCTA5CE20')

# Create healthcare GeoDataFrame
facilities_gdf = gpd.GeoDataFrame(
    healthCareFacilities,
    geometry=gpd.points_from_xy(healthCareFacilities.Longitude, healthCareFacilities.Latitude),
    crs="EPSG:4326"
)

# Match CRS to county map
facilities_gdf = facilities_gdf.to_crs(geographicalArea.crs)
dekalb_zcta = dekalb_zcta.to_crs(geographicalArea.crs)

# DBSCAN clustering
coords = np.column_stack((facilities_gdf.geometry.x, facilities_gdf.geometry.y))
db = DBSCAN(eps=0.02, min_samples=2).fit(coords)
facilities_gdf['cluster'] = db.labels_

# Plot choropleth
fig, ax = plt.subplots(figsize=(12,12))

# Choropleth: population by ZIP code
dekalb_zcta.plot(
    ax=ax,
    column='Population',
    cmap='Greens',
    legend=True,
    edgecolor='black',
    linewidth=0.5
)

# County boundary outline
geographicalArea.boundary.plot(ax=ax, color='black', linewidth=1)

# Overlay healthcare clusters
facilities_gdf[facilities_gdf['cluster'] >= 0].plot(
    ax=ax, color='blue', markersize=50, label='Facility Cluster'
)
facilities_gdf[facilities_gdf['cluster'] == -1].plot(
    ax=ax, color='red', markersize=50, label='Potential Underserved'
)

# Custom legend
cluster_handle = mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=10, label='Facility Cluster')
underserved_handle = mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=10, label='Potential Underserved')
plt.legend(handles=[cluster_handle, underserved_handle])

plt.title("DeKalb County Population Choropleth with Healthcare Facility Clusters")
plt.show()
