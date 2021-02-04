#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import folium
import numpy as np

pd.set_option( 'display.max_columns', None )
pd.set_option( 'display.max_rows', None )

# df_covid['Country/Region']=df_covid['Country/Region'].replace(['US', 'Russia', 'Guinea-Bissau','Cote d\'Ivoire','Congo (Brazzaville)','Congo (Kinshasa)','Tanzania'], ['United States of America', 'Russian Federation','Guinea Bissau','Ivory Coast','Republic of the Congo','Democratic Republic of the Congo','United Republic of Tanzania'])


# In[2]:


# load data
df_covid = pd.read_csv( '..\csv\country_wise_latest.csv' )
df_covid.rename( columns={'Country/Region': 'Country'}, inplace=True )
df_covid['Country']=df_covid['Country'].replace(['Cote d\'Ivoire','Congo (Brazzaville)','Congo (Kinshasa)','Tanzania', 'Cabo Verde'], ['Ivory Coast','Republic of the Congo','Democratic Republic of the Congo','United Republic of Tanzania', 'Cape Verde'])
# df_covid.set_index('Country', inplace=True)


# In[3]:


wa_data0 = df_covid.loc[df_covid['WHO Region']=='Africa']
wa_data1 = df_covid.loc[df_covid['Country'].isin(['Egypt', 'Sudan', 'Libya', 'Somalia', 'Tunisia', 'Morocco'])]
wa_data =pd.concat([wa_data0, wa_data1])
wa_data = wa_data.sort_values(by='Country')


# In[4]:


# create empty world map
world_map = folium.Map( location=[0,0], zoom_start=2, max_bounds=True )

# load json dat for world
world_geo = r'africa-copy.json'


# In[5]:


# create choropleth map
folium.Choropleth(
    geo_data=world_geo,
    name='choropleth',
    data=wa_data,
    columns=['Country', 'Deaths'],
    key_on='feature.properties.name',
    # threshold_scale=threshold_scale,
    fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2,
    legend_name='Covid-19 Deaths Across Africa',
).add_to( world_map )


# In[6]:


world_map


# In[7]:


import plotly
import plotly.express as px
import json


# In[8]:


africa = json.load(open('africa-copy.json','r'))

'''africa_id_map={}
for feature in africa['features']:
    feature['id'] = feature['properties']['name']
    africa_id_map[feature['properties']['name']] = feature['id']

wa_data['id']=wa_data['Country'].apply(lambda x:africa_id_map[x]
'''

# In[ ]:


wa_data


# In[ ]:


fig = px.choropleth(
    wa_data,
    geojson=africa, 
    locations="Country",
    color="Deaths", 
    hover_name="Country",
    hover_data=['Confirmed', 'Active','Deaths / 100 Cases'],
    labels = {'Deaths': 'Number of Covid-19 Deaths'},
    scope='africa'
    )
fig.show()
#fig.write_html('Covid_africa_map.html')

