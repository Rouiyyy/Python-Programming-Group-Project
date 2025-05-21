import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import os
import webbrowser

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full file path
file_path = os.path.join(script_dir, "kc_house_data.csv")

# Load the dataset
dat1 = pd.read_csv(file_path)

# Create quantile bins
quantiles = pd.qcut(dat1['price'], q=10, labels=False, duplicates='drop')

# Generate colors using matplotlib's plasma colormap
cmap = cm.get_cmap('plasma', 10)
norm = mcolors.Normalize(vmin=0, vmax=9)
dat1['price_color'] = quantiles.apply(lambda q: mcolors.to_hex(cmap(norm(q))))

# Initialize map
map_center = [dat1['lat'].mean(), dat1['long'].mean()]
m = folium.Map(location=map_center, zoom_start=10)

# Add circle markers and tooltips
for _, row in dat1.iterrows():
    tooltip_text = (
        f"Price: ${row['price']:,.0f}<br>"
        f"Bedrooms: {row['bedrooms']}<br>"
        f"Bathrooms: {row['bathrooms']}<br>"
        f"Sqft Living: {row['sqft_living']:,}<br>"
        f"Year Built: {row['yr_built']}"
    )

    folium.CircleMarker(
        location=[row['lat'], row['long']],
        radius=np.log(row['price'] / 1000),
        color=None,
        fill=True,
        fill_opacity=0.3,
        fill_color=row['price_color'],
        tooltip=folium.Tooltip(tooltip_text, sticky=True)
    ).add_to(m)

# Save and open the map
map_path = os.path.join(script_dir, "house_price_map.html")
m.save(map_path)
webbrowser.open(f"file://{map_path}")
