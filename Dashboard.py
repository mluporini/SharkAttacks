# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 10:31:28 2022

@author: mirai
"""

import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime as dt
from dash.dependencies import Input, Output

import folium
from folium.plugins import HeatMap, FeatureGroupSubGroup


app = dash.Dash(__name__)

shark_coord = pd.read_csv('newshark_coord_visualizations.csv')

locations = shark_coord[['Latitude', 'Longitude']]
locationcheck = shark_coord[['Case Number','Latitude', 'Longitude','Coordinate']]
locationlist = locations.values.tolist()
shark_coord.fillna("Unknown",inplace=True)

######Total Attacks#######
center = [15,10]
heat = folium.Map(location=center, tiles = 'Stamen Terrain', zoom_start=1.5, control_scale=True)

HeatMap(locations).add_to(heat)
heat.save('Heat_Map.html')

#####Attack by Species Type#####
m = folium.Map(location=center, zoom_start=1.5, tiles='Stamen Terrain')

marker=folium.FeatureGroup(name='Shark Attacks', show=True)
m.add_child(marker)

Unknown = FeatureGroupSubGroup(marker, name = 'Unknown', control = True, show = True)
White = FeatureGroupSubGroup(marker, name = 'White', control = True, show = True)
Bull = FeatureGroupSubGroup(marker, name = 'Bull', control = True, show = True)
Blacktip = FeatureGroupSubGroup(marker, name = 'Blacktip', control = True, show = True)
Lemon = FeatureGroupSubGroup(marker, name = 'Lemon', control = True, show = True)
Spinner = FeatureGroupSubGroup(marker, name = 'Spinner', control = True, show = True)
Copper = FeatureGroupSubGroup(marker, name = 'Copper', control = True, show = True)
Tiger = FeatureGroupSubGroup(marker, name = 'Tiger', control = True, show = True)
Mako = FeatureGroupSubGroup(marker, name = 'Mako', control = True, show = True)
Whitetip = FeatureGroupSubGroup(marker, name = 'Whitetip', control = True, show = True)
Wobbegong = FeatureGroupSubGroup(marker, name = 'Wobbegong', control = True, show = True)

for point in range(0, len(locationlist)):
    marker_info = []
    marker_info = ["Case Number:  %s" %shark_coord['Case Number'].iloc[point],
                   "Activity Type:  %s" %shark_coord['Activity Type'].iloc[point],
                   "Location:  %s" %shark_coord['Location'].iloc[point],
                   "Coordinate:  %s" %shark_coord['Coordinate'].iloc[point]]
    if shark_coord['Species Type'].iloc[point] == 'Unknown':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="pink",fill=True).add_to(Unknown)
    elif shark_coord['Species Type'].iloc[point] == 'White':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="darkblue",fill=True).add_to(White)
    elif shark_coord['Species Type'].iloc[point] == 'Bull':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="green",fill=True).add_to(Bull)
    elif shark_coord['Species Type'].iloc[point] == 'Blacktip':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="red",fill=True).add_to(Blacktip)
    elif shark_coord['Species Type'].iloc[point] == 'Lemon':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="yellow",fill=True).add_to(Lemon)
    elif shark_coord['Species Type'].iloc[point] == 'Spinner':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="purple",fill=True).add_to(Spinner)
    elif shark_coord['Species Type'].iloc[point] == 'Copper':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="brown",fill=True).add_to(Copper)
    elif shark_coord['Species Type'].iloc[point] == 'Tiger':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="orange",fill=True).add_to(Tiger)
    elif shark_coord['Species Type'].iloc[point] == 'Mako':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="lightblue",fill=True).add_to(Mako)
    elif shark_coord['Species Type'].iloc[point] == 'Whitetip':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="pink",fill=True).add_to(Whitetip)
    elif shark_coord['Species Type'].iloc[point] == 'Wobbegong':
        folium.CircleMarker(location=locationlist[point],popup=marker_info,radius=2, color="gray",fill=True).add_to(Wobbegong)

Unknown.add_to(m)
White.add_to(m)
Bull.add_to(m)
Blacktip.add_to(m)
Lemon.add_to(m)
Wobbegong.add_to(m)
Copper.add_to(m)
Tiger.add_to(m)
Mako.add_to(m)
Whitetip.add_to(m)
Spinner.add_to(m)

folium.map.LayerControl(collapsed=True).add_to(m)


m.save('Species_Map.html')




#######Dashboard Creation#####

app.layout = html.Div(style = {
  'backgroundColor': '#111111'
}, children = [
    html.H1(
    children = 'Shark Attack Database',
    style = {
      'textAlign': 'center',
      'color': '#7FDBFF'
    }
  ),

    html.Div(children = 'Hello Guys!', style = {
    'textAlign': 'center',
    'color': '#7FDBFF'
  }),
    html.Iframe(id = 'map', srcDoc = open('Heat_Map.html', 'r').read(), width = '100%', height = '600'),
    html.Iframe(id = 'map2', srcDoc = open('Species_Map.html','r',encoding='utf-8').read(), width = '100%', height = '600')
])


if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',port=8050)
