import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Shapefile path
shapefile_path = "/Users/nickmark 1/Coding/Election-data/110m_cultural/ne_110m_admin_1_states_provinces.shp"

# Load the shapefile
world = gpd.read_file(shapefile_path)

# Filter for U.S. states
us_map = world[world['admin'] == 'United States of America']

# Example data for representatives lost
state_data = pd.DataFrame({
    "State": [
        "California", "Texas", "Florida", "New York", "Illinois",
        "Pennsylvania", "Ohio", "Georgia", "North Carolina", "Michigan",
        "New Jersey", "Virginia", "Washington", "Indiana", "Tennessee",
        "Arizona", "Massachusetts", "Wisconsin", "Maryland", "Colorado",
        "Missouri", "Alabama", "South Carolina", "Oregon", "Kentucky", "Connecticut"
    ],
    "Representatives Lost": [
        -8, -6, -4, -3, -3, -2, -2, -2, -2, -2,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1
    ]
})

# Normalize state names for consistency
state_data["State"] = state_data["State"].str.strip().str.title()
us_map["name"] = us_map["name"].str.strip().str.title()

# Merge GeoDataFrame with state data
state_map = us_map.merge(state_data, how="left", left_on="name", right_on="State")

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
state_map.boundary.plot(ax=ax, linewidth=1, color="black")
state_map.plot(
    column="Representatives Lost",
    cmap="Reds_r",
    legend=True,
    ax=ax,
    legend_kwds={'label': "Representatives Lost", 'orientation': "horizontal"}
)
plt.title("Representatives Lost by US States", fontsize=16)
plt.axis('off')
plt.show()

