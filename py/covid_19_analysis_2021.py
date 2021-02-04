import matplotlib
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.dates as mdates
import pandas as pd
from datetime import date, timedelta, datetime
import numpy as np
import seaborn as sns
sns.set(rc={'figure.figsize':(11.7,7.27)})

'''
# view all columns and rows
#pd.set_option( 'display.max_columns', None )
# pd.set_option( 'display.max_rows', None )
'''

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'

# get dataframes
confirmed = pd.read_csv( f'{url}/time_series_covid19_confirmed_global.csv', usecols=lambda columns:columns not in['Province/State', 'Lat', 'Long'])
deaths = pd.read_csv( f'{url}/time_series_covid19_deaths_global.csv', usecols=lambda columns:columns not in['Province/State', 'Lat', 'Long'] )
recovered = pd.read_csv( f'{url}/time_series_covid19_recovered_global.csv', usecols=lambda columns:columns not in['Province/State', 'Lat', 'Long'])

west_africa = ['Benin', 'Burkina Faso', "Cote d'Ivoire", 'Gambia', 'Ghana',
                   'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Niger',
                   'Nigeria', 'Senegal', 'Sierra Leone', 'Togo']
countries = ['Ghana', 'Burkina Faso', 'Cote d\'Ivoire', 'Nigeria']


def data_2021(df) -> 'data frame':
    
    assert isinstance( df, pd.DataFrame)
    
    df.rename( columns={'Country/Region': 'country'}, inplace=True)
    df = df[df['country'].isin(west_africa)]
    df.set_index('country', inplace=True)
    
    df.columns = pd.to_datetime( df.columns )  # convert column names to datetime values
    df = df.transpose()
   
    #date_range = pd.date_range( start='1/1/21', end=(date.today() + timedelta( days=-1 )).strftime('%m/%d/%y' ))# create a datetime range to help slice columns
    
    df_2020 = df[(df.index >= '2020-01-22') & (df.index <= '2020-12-31')]
    df_2021 = df[(df.index >= '2021-01-01') & (df.index <= datetime.today().strftime('%Y-%m-%d'))]
    
    df_2021.reset_index(inplace=True)
    df_2021.rename(columns={'index':'date'}, inplace=True)
    df_2021 = pd.melt(df_2021, id_vars=['date'], value_vars=west_africa)
    
    #df_2021 = df_2021.stack
     
    assert isinstance( df_2021, pd.DataFrame )  # check to ensure created obj is a dataframe
    assert isinstance( df_2020, pd.DataFrame )
    
    return df_2021, df_2020
    
confirmed1 = data_2021(confirmed)[0]
confirmed1.rename(columns={'value':'confirmed'}, inplace=True)

recovered1 = data_2021(recovered)[0]
recovered1.rename(columns={'value':'recovered'}, inplace=True)

deaths1 = data_2021(deaths)[0]
deaths1.rename(columns={'value':'dead'}, inplace=True)


data = pd.concat([confirmed1, deaths1, recovered1],axis=1)#.reset_index(drop=True)
data.columns = ['date','country','confirmed','dates1','country1','dead','dates2', 'country2','recovered']
data.drop(['dates1', 'dates2', 'country1','country2'], inplace =True,axis=1)
data.sort_values('date', inplace=True)
#data.reset_index(drop=True,inplace=True)
data2 = data[data['country'].isin(countries)]
datagroup = data2.groupby('country')


for key, data in datagroup:
    with sns.axes_style('darkgrid'):
        ax = sns.lineplot(x=data['date'], y=data['confirmed'], label=key)
        
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #ax.set_xticklabels(data['date'],rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
    ax.set_title('Evolution of COVID 19 in Ghana and its neighboring countries')
    ax.set(xlabel='Date', ylabel='Number of Confirmed cases')
    
    
for key, data in datagroup:
    with sns.axes_style('darkgrid'):
        ax = sns.lineplot(x=data['date'], y=data['dead'], label=key)
        
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #ax.set_xticklabels(data['date'],rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
    ax.set_title('Evolution of COVID 19 in Ghana and its neighboring countries')
    ax.set(xlabel='Date', ylabel='Number of Deaths')
    
for key, data in datagroup:
    with sns.axes_style('darkgrid'):
        ax = sns.lineplot(x=data['date'], y=data['recovered'], label=key)
        
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #ax.set_xticklabels(data['date'],rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
    ax.set_title('Evolution of COVID 19 in Ghana and its neighboring countries')
    ax.set(xlabel='Date', ylabel='Number of Recovered cases')
    
    
import plotly
import plotly.express as px



geojson = 'world_countries.json'

fig = px.choropleth(
    data,
    #geojson=geojson, 
    locations="country",
    #featureidkey = 'properties.name',
    color="dead", 
    #hover_name="country",
    scope='africa',
    animation_frame=data["date"].astype(str))
fig.show()




