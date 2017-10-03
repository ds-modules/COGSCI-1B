import pandas as pd
import numpy as np
import folium
import seaborn as sns
import matplotlib.pyplot as plt

def map_with_bins(column, df, quantiles=False):
    """Takes a column from a df, determines what bin each row lies
    in, then plots on a map with the color dependent on the bin"""
    
    bin_cutoffs=5
    color_lst=['#2c7bb6', '#abd9e9', '#ffffbf', '#fdae61', '#d7191c']
    
    if quantiles:
        bins = pd.qcut(df[column], bin_cutoffs)
    else:
        bins = pd.cut(df[column], bin_cutoffs)
    bin_names = bins.cat.categories
      
    bin_to_color = dict(zip(bin_names, color_lst))   
    bin_display = pd.DataFrame(bin_names, columns=['Bins'])
    display(bin_display.style.applymap(lambda x: 'background-color: {}'.format(bin_to_color[x])))

    mapper = folium.Map(zoom_start=8)
    for lat, lon , bn in list(zip(df['Latitude'], df['Longitude'], bins)):
        folium.Circle(
            radius=300,
            location=[lat, lon],
            color=bin_to_color[bn],
            fill=False).add_to(mapper)
    return mapper

def overlay_hex(x_values, y_values):
    """Overlays a regression line on top of a hex plot
    Works well when dealing with a large number of observations"""
    g = sns.jointplot(x_values, y_values, kind="hex")
    sns.regplot(x_values, y_values, ax=g.ax_joint, scatter=False)
    
def drop_and_subset(column, df, desired):
    lst = desired.copy()
    lst.append(column)
    intermediate = combined.dropna(subset=[column])
    return intermediate[lst].copy()