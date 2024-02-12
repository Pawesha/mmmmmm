import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime

def remove_zeros_and_format_date(date_value):
    if isinstance(date_value, str):
        date_value = pd.to_datetime(date_value, errors='coerce')

    if pd.notna(date_value) and date_value.hour == 0 and date_value.minute == 0 and date_value.second == 0:
        return date_value.strftime('%Y/%m/%d')
    return pd.NaT

def filter_by_year_month(df, year, month):
    start_date = pd.to_datetime(f"{year}-{month}-01", format='%Y-%m-%d')
    end_date = start_date + pd.offsets.MonthEnd(0)
    return df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)].copy()
def dashboard():
    st.header("Welcome to Dashboard!")

    # Load data from Excel file
    filepath = "/Users/paweshashrestha/Downloads/major_final 2/python files/new/refined_dataset.xlsx"
    df = pd.read_excel(filepath)

    df['DATE'] = df['DATE'].apply(remove_zeros_and_format_date)
    df = df.dropna(subset=['DATE'])

# Sidebar widgets
    date_range = st.date_input("Select Date Range", [pd.to_datetime(df['DATE'].min()), pd.to_datetime(df['DATE'].max())])

    hour_range = st.slider("Select Hour Range", 1, 24, [1, 24])
    temperature_range = st.slider("Select Temperature Range", int(df['T2M'].min()), int(df['T2M'].max()), [int(df['T2M'].min()), int(df['T2M'].max())])

# Convert date_range to datetime
    date_range = [datetime.combine(date_range[0], datetime.min.time()), datetime.combine(date_range[1], datetime.max.time())]

# Filter data based on user input
    filtered_df = df[(pd.to_datetime(df['DATE']) >= date_range[0]) & (pd.to_datetime(df['DATE']) <= date_range[1]) &
                 (df['HOUR'].between(hour_range[0], hour_range[1])) &
                 (df['T2M'].between(temperature_range[0], temperature_range[1]))]



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

    def plot_electricity_consumption(df):
        try:
            # Filter data for the month of Kartik and the year 2080
            df_kartik_2080 = df[(df['MONTH'] == 'Kartik') & (df['YEAR\n'] == 2080)]


            if df_kartik_2080.empty:
                st.warning("No data available for Kartik in the year 2080.")
                return

            # Filter data for Tihar and Dashain
            tihar_data = df_kartik_2080[(df_kartik_2080['DAY'].between(25, 29))]
            dashain_data = df_kartik_2080[(df_kartik_2080['DAY'].between(4, 9))]

            # Group by hour of the day (HR) for each dataset
            tihar_hourly_average = tihar_data.groupby('HOUR')['electricity'].mean()
            dashain_hourly_average = dashain_data.groupby('HOUR')['electricity'].mean()

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

    def plot_daily_hourly_average(filtered_df):
        day_mapping = {'Sunday':1 , 'Monday':2 , 'Tuesday':3 ,  'Wednesday':4, 'Thursday':5 , 'Friday':6 , 'Saturday':7 }
        filtered_df['DOTW'] = filtered_df['DOTW'].map(day_mapping)
        # Group by day of the week (DOTW) and hour of the day (HR), then calculate the average electricity consumption for each hour
        grouped = filtered_df.groupby(['DOTW', 'HOUR'])
        daily_hourly_average = grouped['electricity'].mean().unstack()

        # Create traces for each day of the week
        data = []
        for DOTW in range(1, 8):
            if DOTW in daily_hourly_average.index:  # Check if the day of the week exists in the data
                trace = go.Scatter(x=daily_hourly_average.columns, y=daily_hourly_average.loc[DOTW].values, mode='lines', name=f'Day {DOTW}')
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

    def plot_monthly_hourly_average(df):
        df['MONTH'] = df['MONTH'].map(nepali_month_names)
        # Group by month (MO) and hour of the day (HR), then calculate the average electricity consumption for each hour
        grouped = df.groupby(['MONTH', 'HOUR'])
        monthly_hourly_average = grouped['electricity'].mean().unstack()


        # Create traces for each month
        data = []
        for month in df['MONTH'].unique():
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

    def description(df):
        # Major KPI
        total_consumption = df['electricity'].sum()
        average_consumption = df['electricity'].mean()
        max_consumption = df['electricity'].max()
        min_consumption = df['electricity'].min()

        # Display Major KPIs
        st.subheader("Major KPIs")
        st.write(f"Total Consumption: {total_consumption:.2f} units")
        st.write(f"Average Consumption: {average_consumption:.2f} units")
        st.write(f"Maximum Consumption: {max_consumption:.2f} units")
        st.write(f"Minimum Consumption: {min_consumption:.2f} units")

        # Consumption Chart
        st.subheader("Electricity Consumption Over Time")
        fig_consumption = px.line(df, x='DATE', y='electricity', title='Electricity Consumption Over Time')

        st.plotly_chart(fig_consumption)

        # Consumption Chart - Average Electricity Consumption per Month
        st.subheader("Average Electricity Consumption per Month")

   # Group by MonthYear and calculate the average electricity consumption
        grouped_data_monthly = df.groupby(['DATE'])['electricity'].mean().reset_index()

# Convert 'DATE' column to pandas datetime format
        grouped_data_monthly['DATE'] = pd.to_datetime(grouped_data_monthly['DATE'], format='%Y/%m/%d')

# Create line chart
        fig_avg_consumption = px.line(grouped_data_monthly,
                      x=grouped_data_monthly['DATE'],
                      y='electricity',
                      labels={'x': 'Time Period', 'electricity': 'Average Electricity Consumption'},
                      title='Average Electricity Consumption per Month')
        st.plotly_chart(fig_avg_consumption)


        # Day of Week Pie Chart - Average Electricity Consumption
        st.subheader("Average Electricity Consumption by Day of the Week")
        # Map day numbers to names
        day_mapping = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
        df['DOTW'] = df['DOTW'].map(day_mapping)
        fig_day_of_week = px.pie(df.groupby('DOTW')['electricity'].mean().reset_index(),
                         names='DOTW', values='electricity',
                         title='Average Electricity Consumption by Day of the Week')
        st.plotly_chart(fig_day_of_week)

    def plot_season_monthly_consumption(df):
        # Define layout for Plotly season plot
        season_layout = go.Layout(title='Average Electricity Consumption vs Hour of the Day by Season',
                       xaxis=dict(title='Hour of the Day'),
                       yaxis=dict(title='Average Electricity Consumption in MW'),
                       legend=dict(title='Season'))

        # Replace numeric representation of Nepali months with their names
        df['MONTH'] = df['MONTH'].map(nepali_month_names)

        # Group by season and hour of the day (HR), then calculate the average electricity consumption for each hour
        grouped = df.groupby(['seasons', 'HOUR'])
        seasonal_hourly_average = grouped['electricity'].mean().unstack()

        # Create traces for each season
        season_data = []
        for seasons in ['Spring', 'Monsoon', 'Autumn', 'Winter','Rainy','Pre Winter','Summer']:
            if seasons in seasonal_hourly_average.index:  # Check if the season exists in the data
                trace = go.Scatter(x=seasonal_hourly_average.loc[seasons].index, y=seasonal_hourly_average.loc[seasons].values, mode='lines', name=seasons)
                season_data.append(trace)

        # Create Plotly season figure
        season_fig = go.Figure(data=season_data, layout=season_layout)
        st.plotly_chart(season_fig)

    description(filtered_df)
    plot_daily_hourly_average(filtered_df)
    plot_monthly_hourly_average(filtered_df)
    plot_electricity_consumption(filtered_df)
    plot_season_monthly_consumption(filtered_df)
    
if __name__ == "__main__":
    dashboard()
