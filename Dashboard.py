# -*- coding: utf-8 -*-

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime as dt
from dash.dependencies import Input, Output, State
from collections import defaultdict, OrderedDict

#import dash_daq as daq

import folium
from folium.plugins import HeatMap, FeatureGroupSubGroup,HeatMapWithTime, MarkerCluster


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

shark_coord = pd.read_csv('newshark_coord_visualizations.csv')

shark_coord["Date2"] = pd.to_datetime(shark_coord["Date2"], format="%m/%d/%Y")
shark_coord.sort_values("Date2", inplace=True)

locations = shark_coord[['Latitude', 'Longitude']]
locationcheck = shark_coord[['Case Number','Latitude', 'Longitude','Coordinate']]
locationlist = locations.values.tolist()
shark_coord.fillna("Unknown",inplace=True)

#######Global Map: Attacks Heatmap#######
center = [15,10]
heat = folium.Map(location=center, tiles = 'Stamen Terrain', zoom_start=1, control_scale=True)

HeatMap(locations).add_to(heat)
heat.save('Heat_Map.html')

#######Global Map:  Attack by Species Type#######
m = folium.Map(location=center, zoom_start=1, tiles='Stamen Terrain')

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

#######Global Map:  Attack Details#######

m3 = folium.Map(location=center, zoom_start=1.5, tiles='openstreetmap')
fg=folium.FeatureGroup(name='My Points', show=True)
m3.add_child(fg)
marker_cluster = MarkerCluster().add_to(fg)
Unprovoked = FeatureGroupSubGroup(marker_cluster, name = 'Unprovoked', control = True, show = True)
Provoked = FeatureGroupSubGroup(marker_cluster, name = 'Provoked', control = True, show = True)
Not_Confirmed = FeatureGroupSubGroup(marker_cluster, name = 'Not Confirmed', control = True, show = True)

for point in range(0, len(locationlist)):
    marker_info = []
    marker_info = ["Case Number:  %s" %shark_coord['Case Number'].iloc[point],
                   "Activity Type:  %s" %shark_coord['Activity Type'].iloc[point],
                   "Location:  %s" %shark_coord['Location'].iloc[point],
                   "Coordinate:  %s" %shark_coord['Coordinate'].iloc[point]]
    if shark_coord['Type'].iloc[point] == 'Unprovoked':
        folium.Marker(location=locationlist[point],popup=marker_info,icon=folium.Icon(color="green")).add_to(Unprovoked)
    elif shark_coord['Type'].iloc[point] == 'Provoked':
        folium.Marker(location=locationlist[point],popup=marker_info,icon=folium.Icon(color="blue")).add_to(Provoked)
    elif shark_coord['Type'].iloc[point] == 'Not Confirmed':
        folium.Marker(location=locationlist[point],popup=marker_info,icon=folium.Icon(color="pink")).add_to(Not_Confirmed)        

Unprovoked.add_to(m3)
Provoked.add_to(m3)
Not_Confirmed.add_to(m3)

folium.map.LayerControl(collapsed=True).add_to(m3)
m3

m3.save('DetailsMap.html')

#######Sunburst#######

shdf = shark_coord
shdf.fillna("Unknown",inplace=True)
shdf.insert(3, 'Continent/Region', "Unknown")
SA = 'Brazil|Ecuador|Colombia|Chile|Venezuela|Uruguay|Trinidad & Tobago'
NA = 'United States|Canada|Mexico'
EU = 'England|Ireland|Italy|United Kingdom|France|Scotland|Croatia|Norway|Montenegro|Spain|Greece'
CA_Carib ='Bahamas|Jamaica|Costa Rica|Cuba|Dominican Republic|Aruba|Panama|Honduras|El Salvador|Cayman Islands|Belize|Antigua|Caribbean Sea|Puerto Rico|Turks & Caicos|St Kitts / Nevis|St Martin|British Virgin Islands|Nevis|St Maarten|Grand Cayman'
ME_NA ='Egypt|Libya|Tunisia|Jordan|Israel|United Arab Emirates|Saudi Arabia|Yemen|Northern Arabian Sea|Palestinian Territories|Malta|Gulf Of Aden|Iran'
Oceania ='New Zealand|Australia|Fiji|Papua New Guinea|Tanzania|New Caledonia|Vanuatu|Solomon Islands'
Oislands ='Maldives|Seychelles|French Polynesia|Marshall Islands|Diego Garcia|Kiribati|Samoa|Guam|Mauritius|Reunion|Cape Verde|Tonga|Azores|Micronesia|Bermuda|Atlantic Ocean'
SAfri ='South Africa|Comoros|Madagascar|Mozambique|Somalia|Senegal|Angola|Namibia|Nigeria|Kenya|Sierra Leone|Liberia'
EA_Pacific ='Russia|Japan|Philippines|Taiwan|Vietnam|Hong Kong|Thailand|South Korea|China|Malaysia|Indonesia|India|Sri Lanka|Okinawa'
U = 'Unknown'

shdf['Continent/Region'].mask(shdf.Country.str.contains(SA),'South America', inplace = True)
shdf['Continent/Region'].mask(shdf.Country.str.contains(NA),'North America', inplace = True)
shdf['Continent/Region'].mask(shdf.Country.str.contains(EU),"Europe", inplace = True)
shdf['Continent/Region'].mask(shdf.Country.str.contains(CA_Carib),"Central America & Caribbean", inplace = True)
shdf['Continent/Region'].mask(shdf.Country.str.contains(ME_NA),'Middle East & Northern Africa', inplace = True)
shdf['Continent/Region'].mask(shdf.Country.str.contains(Oceania),'Oceania', inplace = True)
shdf['Continent/Region'].mask(shdf.Country.str.contains(Oislands),"Oceanic Islands", inplace = True)
shdf['Continent/Region'].mask(shdf.Country.str.contains(SAfri),'Southern Africa', inplace = True)
shdf['Continent/Region'].mask(shdf.Country.str.contains(EA_Pacific),'East Asia & Pacific', inplace = True)

shdf.insert(3, 'Hemisphere', "Unknown")

contidf = shdf[["Country","Continent/Region"]].copy()
contidf.drop_duplicates(subset=['Country'],inplace=True)
contidf

sunbdf = shdf.groupby("Country").count()[["Area"]].copy()
sunbdf.reset_index()

shark_sun_df = pd.merge(sunbdf , contidf , on= "Country",how="left")
shark_sun_df.head(2)

shark_sun_df = shark_sun_df.rename(columns={'Area': 'Cases'})
shark_sun_df = shark_sun_df.reindex(columns=['Continent/Region', 'Country','Cases'])

columns = ['parents', 'labels', 'values']

level1 = shark_sun_df.copy()
level1.columns = columns
level1['text'] = level1['values'].apply(lambda pop: '{:,.0f}'.format(pop))

level2 = shark_sun_df.groupby('Continent/Region').Cases.sum().reset_index()[['Continent/Region', 'Continent/Region','Cases' ]]
level2.columns = columns
level2['parents'] = 'World'
# move value to text for this level
level2['text'] = level2['values'].apply(lambda pop: '{:,.0f}'.format(pop))
level2['values'] = 0

level3 = pd.DataFrame({'parents': [''], 'labels': ['World'],
                       'values': [0.0], 'text': ['{:,.0f}'.format(shark_sun_df.Cases.sum())]})



levels = pd.concat([level1, level2, level3], axis=0).reset_index(drop=True)
levels["World"]="World"
sunburst = px.sunburst(levels,
                  path=["World","parents","labels"],
                  values='values',
                  title="Shark Attacks(1981-2021)",
                  width=520, height=520)
sunburst.update_layout(margin = dict(t=30, l=20, r=20, b=20))
#sunburst.write_html("sun_burst_shark.html")

#######Heatmap by Month#######

monthly = defaultdict(list)


shark_coord['Month']=shark_coord['Date'].str.split('-').str[0]

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

for date in months:
    monthly[date]
    
for r in shark_coord.itertuples():
    monthly[r.Month].append([r.Latitude, r.Longitude])
        
data = monthly

monthlymap = folium.Map(location=[15,10], zoom_start=1,tiles='openstreetmap')


hm = HeatMapWithTime(data=list(data.values()),
                     index=list(data.keys()), 
                     radius=15,
                     auto_play=True,
                     max_opacity=1)
hm.add_to(monthlymap)
monthlymap.save('monthlyattacks.html')

#######Heatmap by Year#######

byyear = defaultdict(list)


shark_coord['Year']=shark_coord['Case Number'].str.split('.').str[0]

years = []
start = 1981
end = 2021
while start <= end:
    years += [str(start)]
    start +=1

for date in years:
    byyear[date]
    
for r in shark_coord.itertuples():
    byyear[r.Year].append([r.Latitude, r.Longitude])
    
    
data = OrderedDict(sorted(byyear.items(), key=lambda t: t[0]))

year = folium.Map(location=center, zoom_start=2,tiles='openstreetmap')


hm = HeatMapWithTime(data=list(data.values()),
                     index=list(data.keys()), 
                     radius=15,
                     auto_play=True,    
                     max_opacity=1)
hm.add_to(year)

year.save('yearlyattacks.html')

#hm.save('YearlyMap.html')

#######Dashboard Creation#######

# Helper functions for dropdowns and slider
def create_dropdown_options(series):
    options = [{'label': i, 'value': i} for i in series.sort_values().unique()]
    return options
def create_dropdown_value(series):
    value = series.sort_values().unique().tolist()
    return value


sidebar = html.Div([dbc.Row([
    dbc.Col(
        html.Div([
            html.H1("Shark Attacks", style =  {'margin-top': '50px', 'text-transform': 'uppercase',
                          'font-size': '40px', 'color': 'white', 'text-align': 'center'}),
            html.P("This dashboard is intended to present insightful visuals from analysis conducted on forty years (1981-2021) of reported shark attack data. The focus area of the primary data set, “The Global Shark Attack File,” is comprised of 3,464 global attack events and maintained by the regional field Shark Research Institute. Visual maps and graphs in the dashboard seek to identify trends in the data that provide insight into where attacks are happening, and which internal and external factors most often lead to attacks. With a better understanding of attack trends and shark behavior, ocean-goers can leverage to mitigate the risk of incident when entering the water.", 
                   style = {'margin-bottom': '60px','color': 'white', 'text-align': 'center', 'font-size': '14px'}),
            html.Img(src="assets/santa-sharks.png", style={'width': '200px', 'margin-bottom': '30px','margin-left': '62px'}),
            html.Label(['Choose a Map:'],style={'margin-left': '20px','margin-top': '30px','margin-bottom': '10px','font-weight': 'bold', 'color': 'white'}),
            dcc.Dropdown(
                id='dropdown',
                options =[
                    {'label': 'Global HeatMap', 'value': 'map'},
                    {'label': 'Attack by Species', 'value': 'map2'},
                    {'label': 'Attack Details', 'value': 'map3'},
                    {'label': 'Global Heatmap by Month', 'value': 'map4'},
                    {'label': 'Global Heatmap by Year', 'value': 'map5'}
                    
                    ], value='map', style={"width": "90%",'margin-bottom': '20px','margin-left': '15px'}),
            html.P("The 'Attack by Species' and 'Attack Details' maps can be filtered by data type by hovering over the top right icon on the map.", 
                   style = {'color': 'white', 'text-align': 'center', 'font-size': '12px'})
            ], id='left-container', style = {'height': '937px', 'width': '350px', 'background-color': '#23395d',
                                             'float': 'left', 'margin': '0'})
                                             )])])
                                             
content = html.Div([dbc.Row([                                            
    dbc.Col(
        html.Div([
            html.H2("Maps", style = {'color':'white', 'margin-top':'10px'}),
            html.Iframe(id='graph',width = '600', height = '275'),
            html.H2('Sunburst',style = {'color':'white'}),
            dcc.Graph(figure=sunburst)
            ], id='middle-container', style = {'background-color': '#1c2e4a'}), width=3),
    dbc.Col(
        html.Div(
    children=[
        html.Div(
            children=[
                html.H2("Shark Species", style = {'color':'white', 'margin-top':'10px'}),
                html.P("Analyze the behavior of different shark species by region",
                    className="header-description", style = {'color':'white'}),
                ]),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Continent/Region",style = {'color':'white'}, className="menu-title"),
                        dcc.Dropdown(
                            id="continent-filter",
                            options=[
                                {"label": continent, "value": continent}
                                for continent in np.sort(shdf["Continent/Region"].unique())
                            ],
                            value="North America",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                              
            ],
            className="menu",
        ),
                html.Div(
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                id="fatal-chart",
                                config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                        html.Div(
                            children=dcc.Graph(
                                id="provoked-chart",
                                config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                    ],
                    className="wrapper",
                ),
            ]
        ), id='right-container', style = {'margin-left': '350px', 'background-color': '#1c2e4a'}, width = 5)])])



app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3),
                dbc.Col(content)
                ]
            ),
        ],
    fluid=True, style = {'backgroundColor': '#1c2e4a','margin': '0'}
    )
                                         
@app.callback(
    Output('graph', 'srcDoc'),
    [Input(component_id='dropdown', component_property='value')]
)


def select_graph(value):
    if value == 'map':
        firstmap = open('Heat_Map.html', 'r').read()
        return firstmap
    elif value == 'map2':
        secondmap = open('Species_Map.html','r',encoding='utf-8').read()
        return secondmap
    elif value == 'map3':
        thirdmap = open('DetailsMap.html', 'r',encoding='utf-8').read()
        return thirdmap
    elif value == 'map4':
        fourthmap = open('monthlyattacks.html', 'r',encoding='utf-8').read()
        return fourthmap
    elif value == 'map5':
        fifthmap = open('yearlyattacks.html', 'r', encoding = 'utf-8').read()
        return fifthmap

@app.callback(
    [Output("fatal-chart", "figure"),Output("provoked-chart", "figure")],
    [
        Input("continent-filter", "value"),
    ],
)




def update_charts(continent):
    maskp = (
        (shdf["Continent/Region"] == continent)
    )
    
    filtered_datap = shdf.loc[maskp, :]
    df=filtered_datap.groupby("Species Type").count().reset_index()
    
    fig1 = px.bar(df, x="Species Type", y="Case Number", color="Fatal (Y/N)", barmode="group")
    fig2 = px.bar(df, x="Species Type", y="Case Number", color="Type", barmode="group")
        
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
    
#if __name__ == '__main__':
#    app.run_server(host= '0.0.0.0',port=8050)
