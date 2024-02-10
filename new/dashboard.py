import streamlit as st
import pandas as pd
import plotly.express as px
 
def dashboard():
    st.write("Welcome to Dashboard!")
 
    # Load the data from the Excel file
    df = pd.read_excel("/Users/paweshashrestha/Downloads/new/refined_data_all (1).xlsx")
    
   
 
    # Bar graph: Total Electricity Consumption by Year
    total_electricity_by_year = df.groupby('YEAR')['electricity'].sum().reset_index()
    st.subheader('Total Electricity Consumption by Year')
    st.plotly_chart(plot_bar_graph(total_electricity_by_year, 'YEAR', 'electricity', 'Total Electricity Consumption', 'Year', 'Total Electricity Consumption'))
 
    # Bar graph: Average Electricity Consumption by Day of the Week
    avg_electricity_by_dotw = df.groupby('DOTW')['electricity'].mean().reset_index()
    st.subheader('Average Electricity Consumption by Day of the Week')
    st.plotly_chart(plot_bar_graph(avg_electricity_by_dotw, 'DOTW', 'electricity', 'Average Electricity Consumption', 'Day of the Week', 'Average Electricity Consumption'))
 
    # Bar graph: Average Electricity Consumption by Hour of the Day
    avg_electricity_by_hr = df.groupby('HR')['electricity'].mean().reset_index()
    st.subheader('Average Electricity Consumption by Hour of the Day')
    st.plotly_chart(plot_bar_graph(avg_electricity_by_hr, 'HR', 'electricity', 'Average Electricity Consumption', 'Hour of the Day', 'Average Electricity Consumption'))
    
 
def plot_bar_graph(data, x_column, y_column, title, x_label, y_label):
    fig = px.bar(data, x=x_column, y=y_column, labels={x_column: x_label, y_column: y_label}, title=title)
    return fig
 
def plot_area_chart(data, x_column_year, x_column_month, y_column, title, x_label, y_label, color_column):
    fig = px.area(data, x=x_column_month, y=y_column, facet_col=x_column_year, labels={x_column_month: x_label, y_column: y_label}, title=title, color=color_column)
    return fig
 
if __name__ == "__main__":
    dashboard()