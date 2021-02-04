import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta

# view all columns and rows
# pd.set_option( 'display.max_columns', None )
# pd.set_option( 'display.max_rows', None )

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'

# get dataframes
confirmed = pd.read_csv( f'{url}/time_series_covid19_confirmed_global.csv' )
deaths = pd.read_csv( f'{url}/time_series_covid19_deaths_global.csv' )
recovered = pd.read_csv( f'{url}/time_series_covid19_recovered_global.csv' )

'''recovered = pd.read_csv( 'time_series_covid19_recovered_global.csv' )
confirmed = pd.read_csv( 'time_series_covid19_confirmed_global.csv' )
deaths = pd.read_csv( 'time_series_covid19_deaths_global.csv' )'''

# remove unneccesary columns from dataframe
dfs = [deaths, recovered, confirmed]

for df in dfs:
    df.rename( columns={'Country/Region': 'Country'}, inplace=True )
    df.drop( ['Province/State', 'Lat', 'Long'], inplace=True, axis=1 )
    df.set_index( 'Country', inplace=True )


# slice dataframe for data into date two data frames by year
def data_2021(df1) -> 'data frame':
    assert isinstance( df1, pd.DataFrame )  # check to ensure arg passed is a dataframe
    west_africa = ['Benin', 'Burkina Faso', "Cote d'Ivoire", 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Niger', 'Nigeria', 'Senegal', 'Sierra Leone', 'Togo']
    df1 = df1.loc[west_africa]  # slice df from data from only west africa
    df1.columns = pd.to_datetime( df1.columns )  # convert column names to datetime values
    date_range_21 = pd.date_range( start='1/1/21', end=(date.today() + timedelta( days=-1 )).strftime(
        '%m/%d/%y' ) )  # create a datetime range to help slice columns
    # date_range_20 = pd.date_range(start='1/1/22', end='1/')
    df_2021 = df1[date_range_21].transpose()  # transpose data to give a better chart visualisation
    # df_2020 = df1[date_range_20].transpose()
    assert isinstance( df_2021, pd.DataFrame )  # check to ensure created obj is a dataframe
    # assert isinstance( df_2020, pd.DataFrame )
    return df_2021  # , df_2020


# creating line charts
def confirmed_line_chart(dataset) -> 'line plot':
    ax = dataset.plot.line(  )
    ax.set_title( 'West Africa: Covid-19 Confirmed Cases Trend for 2021' )
    ax.set_xlabel( 'COUNTRIES' )
    ax.set_ylabel( 'NUMBER' )
    ax.set_facecolor('black')

    plt.savefig( 'Confirmed_line_chart_2021.png', bbox_inches='tight' )


def recovered_line_chart(dataset) -> 'line plot':
    ax = dataset.plot.line()
    ax.set_title( 'West Africa: Covid-19 Recovered Cases Trend for 2021' )
    ax.set_xlabel( 'COUNTRIES' )
    ax.set_ylabel( 'NUMBERs' )

    plt.savefig( 'Recovered_line_chart_2021.png' )


def deaths_line_chart(dataset) -> 'line plot':
    ax = dataset.plot.line()

    ax.set_title( 'West Africa: Covid-19 Deaths Trend for 2021' )
    ax.set_xlabel( 'COUNTRIES' )
    ax.set_ylabel( 'NUMBER' )

    plt.savefig( 'Deaths_line_chart_2021.png' )


# creating box charts
def confirmed_box_chart(dataset) -> 'box plot':
    ax = dataset.plot.box( )
    ax.set_title( 'West Africa: Covid-19 Confirmed Cases Trend for 2021' )
    ax.set_xlabel( 'COUNTRIES' )
    ax.set_ylabel( 'NUMBER' )

    plt.savefig( 'Confirmed_box_chart_2021.png' )


def recovered_box_chart(dataset) -> 'box plot':
    ax = dataset.plot.line()
    ax.set_title( 'West Africa: Covid-19 Recovered Cases Trend for 2021' )
    ax.set_xlabel( 'COUNTRIES' )
    ax.set_ylabel( 'NUMBERs' )

    plt.savefig( 'Recovered_box_chart_2021.png' )


def deaths_box_chart(dataset) -> 'box plot':
    ax = dataset.plot.line()

    ax.set_title( 'West Africa: Covid-19 Deaths Trend for 2021' )
    ax.set_xlabel( 'COUNTRIES' )
    ax.set_ylabel( 'NUMBER' )

    plt.savefig( 'Deaths_box_chart_2021.png' )


countries = ['Ghana', 'Burkina Faso', 'Cote d\'Ivoire', 'Nigeria']

confirmed_line_chart( data_2021( confirmed )[countries] )
recovered_line_chart( data_2021( recovered )[countries] )
deaths_line_chart( data_2021( deaths )[countries] )
confirmed_box_chart( data_2021( confirmed )[countries] )
recovered_box_chart( data_2021( recovered )[countries] )
deaths_box_chart( data_2021( deaths )[countries] )