import pandas as pd
# Read the JSON file with Population Data
populationData = pd.read_json("populationData.json")
healthCareFacilities = pd.read_json("healthCare.json") 

#  Total Population Density
land_mass = 271
total_population = populationData.loc[populationData["race_category"] == "Total Population", "population"].iloc[0]
totalPopulationDensity = int(total_population / land_mass)
print("Total Population Density:", totalPopulationDensity)

# The Health Care Facatlites
print("Health Care Facilities Data:", healthCareFacilities) 
