import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objs as go
 
# Load data from Excel file
df = pd.read_excel("/Users/paweshashrestha/Downloads/new/refined_data_all (1).xlsx")
 
# Mapping of numeric representation of Nepali months to their names
nepali_month_names = {
    1: 'Baisakh',
    2: 'Jestha',
    3: 'Ashad',
    4: 'Shrawan',
    5: 'Bhadra',
    6: 'Ashwin',
    7: 'Kartik',
    8: 'Mangsir',
    9: 'Poush',
    10: 'Magh',
    11: 'Falgun',
    12: 'Chaitra'
}
 
# Define a function to map each month to its corresponding season
def map_month_to_season(month):
    if month in ['Baisakh', 'Chaitra']:
        return 'Spring'
    elif month in ['Jestha', 'Ashad']:
        return 'Summer'
    elif month in ['Shrawan', 'Bhadra']:
        return 'Rainy'
    elif month in ['Ashwin', 'Kartik']:
        return 'Autumn'
    elif month in ['Mangsir', 'Poush']:
        return 'Pre Winter'
    elif month in ['Magh', 'Falgun']:
        return 'Winter'
 
# Replace numeric representation of Nepali months with their names
df['MO'] = df['MO'].map(nepali_month_names)
 
# Map months to seasons
df['Season'] = df['MO'].map(map_month_to_season)
 
# Group by season and hour of the day (HR), then calculate the average electricity consumption for each hour
grouped = df.groupby(['Season', 'HR'])
seasonal_hourly_average = grouped['electricity'].mean().unstack()
 
# Create traces for each season
season_data = []
for season in ['Spring', 'Summer', 'Rainy', 'Autumn', 'Pre Winter', 'Winter']:
    if season in seasonal_hourly_average.index:  # Check if the season exists in the data
        trace = go.Scatter(x=seasonal_hourly_average.loc[season].index, y=seasonal_hourly_average.loc[season].values, mode='lines', name=season)
        season_data.append(trace)
 
# Define layout for Plotly season plot
season_layout = go.Layout(title='Average Electricity Consumption vs Hour of the Day by Season',
                   xaxis=dict(title='Hour of the Day'),
                   yaxis=dict(title='Average Electricity Consumption in MW'),
                   legend=dict(title='Season'))
 
# Create Plotly season figure
season_fig = go.Figure(data=season_data, layout=season_layout)
 
def plot_electricity_consumption(df):
    try:
        # Filter data for the month of Kartik and the year 2080
        df_kartik_2080 = df[(df['MO'] == 'Kartik') & (df['YEAR'] == 2080)]
 
        if df_kartik_2080.empty:
            st.warning("No data available for Kartik in the year 2080.")
            return
 
        # Filter data for Tihar and Dashain
        tihar_data = df_kartik_2080[(df_kartik_2080['DY'].between(25, 29))]
        dashain_data = df_kartik_2080[(df_kartik_2080['DY'].between(4, 9))]
 
        # Group by hour of the day (HR) for each dataset
        tihar_hourly_average = tihar_data.groupby('HR')['electricity'].mean()
        dashain_hourly_average = dashain_data.groupby('HR')['electricity'].mean()
 
        # Create traces for Tihar and Dashain
        data = [
            go.Scatter(x=tihar_hourly_average.index, y=tihar_hourly_average.values, mode='lines', name='Tihar'),
            go.Scatter(x=dashain_hourly_average.index, y=dashain_hourly_average.values, mode='lines', name='Dashain')
        ]
 
        # Define layout
        layout = go.Layout(title='Average Electricity Consumption for Kartik (Year 2080)',
                           xaxis=dict(title='Hour of the Day'),
                           yaxis=dict(title='Average Electricity Consumption'))
 
        # Create figure
        fig = go.Figure(data=data, layout=layout)
 
        # Display the plot
        st.plotly_chart(fig)
 
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
 
 
# Function to plot daily hourly average
def plot_daily_hourly_average(df):
    # Group by day of the week (DOTW) and hour of the day (HR), then calculate the average electricity consumption for each hour
    grouped = df.groupby(['DOTW', 'HR'])
    daily_hourly_average = grouped['electricity'].mean().unstack()
 
    # Create traces for each day of the week
    data = []
    for dotw in range(1, 8):
        trace = go.Scatter(x=daily_hourly_average.columns, y=daily_hourly_average.loc[dotw].values, mode='lines', name=f'Day {dotw}')
        data.append(trace)
 
    # Define layout
    layout = go.Layout(title='Average Electricity Consumption vs Hour of the Day by Day of the Week',
                       xaxis=dict(title='Hour of the Day'),
                       yaxis=dict(title='Average Electricity Consumption in MW'),
                       legend=dict(title='Day of the Week'))
 
    # Create figure
    fig = go.Figure(data=data, layout=layout)
 
    # Display the plot
    st.plotly_chart(fig)
 
# Function to plot monthly hourly average
def plot_monthly_hourly_average(df):
    # Group by month (MO) and hour of the day (HR), then calculate the average electricity consumption for each hour
    grouped = df.groupby(['MO', 'HR'])
    monthly_hourly_average = grouped['electricity'].mean().unstack()
 
    # Create traces for each month
    data = []
    for month in df['MO'].unique():
        trace = go.Scatter(x=monthly_hourly_average.columns, y=monthly_hourly_average.loc[month].values, mode='lines', name=month)
        data.append(trace)
 
    # Define layout
    layout = go.Layout(title='Average Electricity Consumption vs Hour of the Day by Nepali Month',
                       xaxis=dict(title='Hour of the Day'),
                       yaxis=dict(title='Average Electricity Consumption in MW'),
                       legend=dict(title='Month'))
 
    # Create figure
    fig = go.Figure(data=data, layout=layout)
 
    # Display the plot
    st.plotly_chart(fig)
 
def dashboard():
    st.write("Welcome to Dashboard!")
   
    # Embed Google Maps iframe
    st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14130.927001396656!2d85.33981835!3d27.6946846!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb199a06c2eaf9%3A0xc5670a9173e161de!2sNew%20Baneshwor%2C%20Kathmandu%2044600!5e0!3m2!1sen!2snp!4v1707549720968!5m2!1sen!2snp" width="400" height="250" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>', unsafe_allow_html=True)
 
    # Plot daily hourly average
    plot_daily_hourly_average(df)
 
    # Plot monthly hourly average
    plot_monthly_hourly_average(df)
    plot_electricity_consumption(df)
 
    # Plot seasonal hourly average
    st.plotly_chart(season_fig)
    
if __name__ == "__main__":
    dashboard()
