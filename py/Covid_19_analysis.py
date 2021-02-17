import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
import seaborn as sns
import plotly.express as px
import json

sns.set( rc={'figure.figsize': (11.7, 7.27)} )
'''#view all columns and rows
pd.set_option( 'display.max_columns', None )
pd.set_option( 'display.max_rows', None )
'''

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'

# get dataframes
confirmed = pd.read_csv( f'{url}/time_series_covid19_confirmed_global.csv',
                         usecols=lambda columns: columns not in ['Province/State', 'Lat', 'Long'] )
deaths = pd.read_csv( f'{url}/time_series_covid19_deaths_global.csv',
                      usecols=lambda columns: columns not in ['Province/State', 'Lat', 'Long'] )
recovered = pd.read_csv( f'{url}/time_series_covid19_recovered_global.csv',                       usecols=lambda columns: columns not in ['Province/State', 'Lat', 'Long'] )

west_africa = ['Benin', 'Burkina Faso', "Cote d'Ivoire", 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Niger', 'Nigeria', 'Senegal', 'Sierra Leone', 'Togo']


# countries = ['Ghana', 'Burkina Faso', "Cote d'Ivoire", 'Nigeria']

def w_data(df):
	assert isinstance( df, pd.DataFrame )

	df.rename( columns={'Country/Region': 'country'}, inplace=True )
	df = df[df['country'].isin( west_africa )]
	df.set_index( 'country', inplace=True )

	df.columns = pd.to_datetime( df.columns )
	df = df.transpose()
	df.reset_index( inplace=True )

	df.rename( columns={'index': 'date'}, inplace=True )
	df = pd.melt( df, id_vars=['date'], value_vars=west_africa )
	df = df[(df['date'] > '2020-03-12') & (df['date'] <= datetime.today().strftime( '%Y-%m-%d' ))]

	assert isinstance( df, pd.DataFrame )  # check to ensure created obj is a dataframe
	return df


confirmed1 = w_data( confirmed )
confirmed1.rename( columns={'value': 'confirmed'}, inplace=True )

recovered1 = w_data( recovered )
recovered1.rename( columns={'value': 'recovered'}, inplace=True )

deaths1 = w_data( deaths )
deaths1.rename( columns={'value': 'dead'}, inplace=True )

data = pd.concat( [confirmed1, deaths1, recovered1], axis=1 )  # .reset_index(drop=True)
data.columns = ['date', 'country', 'confirmed', 'dates1', 'country1', 'dead', 'dates2', 'country2', 'recovered']
data.drop( ['dates1', 'dates2', 'country1', 'country2'], inplace=True, axis=1 )
datagroup = data.groupby('date')
data.to_csv('data_by_date.csv', index=False)

for key, data in datagroup:
    with sns.axes_style( 'whitegrid' ):
        ax = sns.lineplot( x=data['date'], y=data['confirmed'], label=key)
    plt.legend( bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
    ax.set_xticklabels( data['date'], rotation=45 )
    ax.xaxis.set_major_formatter( mdates.DateFormatter( '%b %d %Y' ) )
    ax.set_title( 'Evolution of COVID 19 in Ghana and its neighboring countries' )
    ax.set( xlabel='Date', ylabel='Number of Confirmed Cases' )
plt.show()

for key, data in datagroup:
    with sns.axes_style( 'whitegrid' ):
        ax = sns.lineplot( x=data['date'], y=data['confirmed'], label=key)

    plt.legend( bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
    ax.set_xticklabels( data['date'], rotation=45 )
    ax.xaxis.set_major_formatter( mdates.DateFormatter( '%b %d %Y' ) )
    ax.set_title( 'Evolution of COVID 19 in Ghana and its neighboring countries' )
    ax.set( xlabel='Date', ylabel='Number of Confirmed cases' )
plt.show()
for key, data in datagroup:
    with sns.axes_style( 'whitegrid' ):
        ax = sns.lineplot( x=data['date'], y=data['dead'], label=key )

    plt.legend( bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
    ax.set_xticklabels( data['date'], rotation=45 )
    ax.xaxis.set_major_formatter( mdates.DateFormatter( '%b %d %Y' ) )
    ax.set_title( 'Evolution of COVID 19 in Ghana and its neighboring countries' )
    ax.set( xlabel='Date', ylabel='Number of Deaths' )
plt.show()
for key, data in datagroup:
    with sns.axes_style( 'whitegrid' ):
        ax = sns.lineplot( x=data['date'], y=data['recovered'], label=key)

    plt.legend( bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
    ax.set_xticklabels( data['date'], rotation=45 )
    ax.xaxis.set_major_formatter( mdates.DateFormatter( '%b %d %Y' ) )
    ax.set_title( 'Evolution of COVID 19 in Ghana and its neighboring countries' )
    ax.set( xlabel='Date', ylabel='Number of Recoveries' )
plt.show()

africa = json.load( open( 'africa.json', 'r' ) )

fig = px.choropleth(
    data,
    geojson=africa,
    locations="country",
    color="dead",
    scope='africa',
    featureidkey='properties.name',
    animation_frame=data['date'].astype( str ),
    hover_name='country',
    hover_data=['confirmed', 'recovered'],
    labels={'dead': 'Covid-19 Deaths'},
    projection='mercator',
    title='Covid-19 Deaths  Across West Africa'
    )
fig.update_geos( fitbounds='locations', visible=False )

fig.show()

#save map to file
fig.write_html('Covid_plotly_map.html')
