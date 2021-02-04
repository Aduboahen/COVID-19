import pandas as pd
import folium

# load data
df_covid = pd.read_csv( 'country_wise_latest.csv' )
df_covid.rename( columns={'Country/Region': 'Country'}, inplace=True )
# df_covid.set_index('Country', inplace=True)

west_africa = ['Benin', 'Burkina Faso', "Cote d'Ivoire", 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia',
               'Mali', 'Niger', 'Nigeria', 'Senegal', 'Sierra Leone', 'Togo']

wa_data = df_covid.loc[df_covid['Country'].isin(west_africa)]
# create empty world map
world_map = folium.Map( location=[0, 0], zoom_start=2 )

# load json dat for world
world_geo = r'world_countries.json'

# threshold_scale = np.linspace(df_san['Deaths'].min(),df_san['Deaths'].max(),6, dtype=int)
# threshold_scale = threshold_scale.tolist() # change the numpy array to a list
# threshold_scale[-1] = threshold_scale[-1] + 1


# create choropleth map
folium.Choropleth(
    geo_data=world_geo,
    name='choropleth',
    data=wa_data,
    columns=['Country', 'Deaths'],
    key_on='feature.properties.name',
    # threshold_scale=threshold_scale,
    fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2,
    legend_name='Covid-19 Deaths',
).add_to( world_map )

# world_map.render()

world_map.save( 'Covid-19 Deaths.html' )

# df_covid['Country/Region']=df_san['Country/Region'].replace(['US', 'Russia', 'Guinea-Bissau','Cote d\'Ivoire','Congo (Brazzaville)','Congo (Kinshasa)','Tanzania'], ['United States of America', 'Russian Federation','Guinea Bissau','Ivory Coast','Republic of the Congo','Democratic Republic of the Congo','United Republic of Tanzania'])
