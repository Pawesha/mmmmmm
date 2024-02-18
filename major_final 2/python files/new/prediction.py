import pandas as pd
import streamlit as st
import nepali_datetime
from datetime import datetime, timedelta
import requests
from nepali_datetime import date as nepali_date
import plotly.express as px
import plotly.graph_objs as go
 
def convert_to_ad_date(bs_year, bs_month, bs_day):
    bs_date = nepali_datetime.date(bs_year, bs_month, bs_day)
    ad_date = bs_date.to_datetime_date()
    return ad_date
 
def get_holidays(year):
    # Provided holiday data
    
    holidays_data = {
      "holidays": [
    {"name": "Maghe Sankranti", "date": "2023-01-15"},
    {"name": "Sonam Losar", "date": "2023-01-22"},
    {"name": "Festival of Lord Shiva", "date": "2023-02-18"},
    {"name": "Festival of Colors", "date": "2023-03-07"},
    {"name": "International Women's Day", "date": "2023-03-08"},
    {"name": "March Equinox", "date": "2023-03-20"},
    {"name": "Nepali New Year's Eve", "date": "2023-04-13"},
    {"name": "Nepali New Year's Day", "date": "2023-04-14"},
    {"name": "Festival of Breaking the Fast", "date": "2023-04-22"},
    {"name": "Buddha's Birthday", "date": "2023-05-05"},
    {"name": "June Solstice", "date": "2023-06-21"},
    {"name": "Feast of the Sacrifice", "date": "2023-06-29"},
    {"name": "Gaura Festival", "date": "2023-09-06"},
    {"name": "Haritalika Teej", "date": "2023-09-18"},
    {"name": "Constitution Day", "date": "2023-09-20"},
    {"name": "September Equinox", "date": "2023-09-23"},
    {"name": "Phulpati", "date": "2023-10-21"},
    {"name": "Asthami", "date": "2023-10-22"},
    {"name": "Navami", "date": "2023-10-23"},
    {"name": "Dashami", "date": "2023-10-24"},
    {"name": "Laxmi Puja", "date": "2023-11-12"},
    {"name": "Chaath Puja", "date": "2023-11-18"},
    {"name": "Guru Nanak's Birthday", "date": "2023-11-27"},
    {"name": "December Solstice", "date": "2023-12-22"},
    {"name": "Christmas Eve", "date": "2023-12-24"},
    {"name": "Christmas Day", "date": "2023-12-25"},
    
    {"name": "Maghe Sankranti", "date": "2020-01-15"},
    {"name": "Sonam Losar", "date": "2020-01-25"},
    {"name": "Maha Shivaratri", "date": "2020-02-11"},
    {"name": "Nari Dibas", "date": "2020-03-08"},
    {"name": "Ghode Jatra", "date": "2020-03-24"},
    {"name": "Ram Navami", "date": "2020-04-02"},
    {"name": "Nepali New Year", "date": "2020-04-14"},
    {"name": "Labour Day", "date": "2020-05-01"},
    {"name": "Buddha Jayanti", "date": "2020-05-07"},
    {"name": "Ramjan Edul Fikra", "date": "2020-05-25"},
    {"name": "Ganatantra Diwas", "date": "2020-05-28"},
    {"name": "Edul Aajaha", "date": "2020-07-31"},
    {"name": "Gai Jatra", "date": "2020-08-04"},
    {"name": "Haritalika Teej", "date": "2020-08-21"},
    {"name": "Gaura Parba", "date": "2020-08-26"},
    {"name": "Indra Jatra", "date": "2020-09-01"},
    {"name": "Constitution Day", "date": "2020-09-19"},
    {"name": "Ghatasthapana", "date": "2020-10-17"},
    {"name": "Phulpati", "date": "2020-10-22"},
    {"name": "Maha Ashtami", "date": "2020-10-24"},
    {"name": "Maha Navami", "date": "2020-10-25"},
    {"name": "Vijaya Dashami", "date": "2020-10-26"},
    {"name": "Ekadashi", "date": "2020-10-27"},
    {"name": "Laxmi Puja", "date": "2020-11-15"},
    {"name": "Govardhan Puja", "date": "2020-11-16"},
    {"name": "Chhath Puja", "date": "2020-11-20"},
    {"name": "Guru Nanak's Birthday", "date": "2020-11-30"},
    {"name": "Christmas Day", "date": "2020-12-25"},
    {"name": "Udhauli Parva", "date": "2020-12-29"},
    {"name": "Tamu Losar", "date": "2020-12-30"},
    
    {"name": "Maghe Sankranti", "date": "2024-01-15"},
    {"name": "Sonam Losar", "date": "2024-01-25"},
    {"name": "International Women's Day", "date": "2024-03-08"},
    {"name": "Festival of Lord Shiva", "date": "2024-03-08"},
    {"name": "March Equinox", "date": "2024-03-20"},
    {"name": "Festival of Colors", "date": "2024-03-25"},
    {"name": "Festival of Breaking the Fast", "date": "2024-04-10"},
    {"name": "Nepali New Year's Eve", "date": "2024-04-13"},
    {"name": "Nepali New Year's Day", "date": "2024-04-14"},
    {"name": "Buddha's Birthday", "date": "2024-05-23"},
    {"name": "Feast of the Sacrifice", "date": "2024-06-17"},
    {"name": "June Solstice", "date": "2024-06-20"},
    {"name": "Haritalika Teej", "date": "2024-09-06"},
    {"name": "Constitution Day", "date": "2024-09-20"},
    {"name": "September Equinox", "date": "2024-09-22"},
    {"name": "Phulpati", "date": "2024-10-10"},
    {"name": "Asthami", "date": "2024-10-11"},
    {"name": "Navami", "date": "2024-10-12"},
    {"name": "Dashami", "date": "2024-10-13"},
    {"name": "Laxmi Puja", "date": "2024-11-03"},
    {"name": "Chaath Puja", "date": "2024-11-09"},
    {"name": "Guru Nanak's Birthday", "date": "2024-11-15"},
    {"name": "December Solstice", "date": "2024-12-21"},
    {"name": "Christmas Eve", "date": "2024-12-24"},
    {"name": "Christmas Day", "date": "2024-12-25"}
]
 
    }
    try:
        current_date = datetime(year, 1, 1)
        while current_date.year == year:
            if current_date.weekday() == 5:  # Saturday
                holidays_data["holidays"].append({
                    'name': 'Saturday',
                    'date': current_date.strftime('%Y-%m-%d'),
                    # You can add more details if needed, like 'observed', 'public', 'country', etc.
                })
            current_date += timedelta(days=1)
 
        return holidays_data['holidays']
 
    except Exception as e:
        st.error(f"Error fetching holidays: {str(e)}")
        return []    
    
def calculate_kpis(predictions_data):
    # Calculate KPIs from predictions_data DataFrame
    total_demand = predictions_data['demand'].sum()
    average_demand = predictions_data['demand'].mean()
    max_demand = predictions_data['demand'].max()
    min_demand = predictions_data['demand'].min()

    return total_demand, average_demand, max_demand, min_demand

def display_kpis(total_demand, average_demand, max_demand, min_demand):
    st.subheader("Key Performance Indicators (KPIs)")
    st.info(f"Total Demand: {total_demand:.2f} megawatt")
    st.info(f"Average Demand: {average_demand:.2f} megawatt")
    st.info(f"Maximum Demand: {max_demand:.2f} megawatt")
    st.info(f"Minimum Demand: {min_demand:.2f} megawatt")
    
 
def is_selected_date_holiday(holidays, selected_date):
    selected_date_str = selected_date.strftime("%Y-%m-%d")
    for holiday in holidays:
        if holiday.get('date') == selected_date_str:
            return True, holiday.get('name')
    return False, None
 
def get_day_of_week_number(day_of_week):
    # Map day of the week to a number (1 to 7)
    day_number_mapping = {
        'Monday': 2,
        'Tuesday': 3,
        'Wednesday': 4,
        'Thursday': 5,
        'Friday': 6,
        'Saturday': 7,
        'Sunday': 1,
    }
    return day_number_mapping.get(day_of_week, 0)
 
def prediction():
    st.write("Welcome to prediction!")
 
    # Take input for Nepali month, day, and year
    bs_year = st.number_input("Enter Nepali Year", min_value=1970, max_value=2100, value=2078)
    bs_month = st.selectbox("Select Month", range(1, 13))
    bs_day = st.number_input("Select Day", min_value=1, max_value=32, value=1)
    
  
   
 
 
 
    # st.write("Selected Nepali Date:", f"{bs_month}/{bs_day}/{bs_year}")
 
 
    ad_date = convert_to_ad_date(bs_year, bs_month, bs_day)
    # st.write("Equivalent English Date:", ad_date)
 
   
    day_of_week = ad_date.strftime("%A")
    # st.write(f"Day of the Week for English Date: {day_of_week}")
 
    holidays = get_holidays(ad_date.year)
 
 
    is_holiday_today, holiday_name_today = is_selected_date_holiday(holidays, ad_date)
 
    # Convert day of the week to a number
    day_of_week_number = get_day_of_week_number(day_of_week)
 
    if is_holiday_today:
        # st.write(f"The specified date ({day_of_week}) is a holiday! It's {holiday_name_today}.")
        display_predictions(ad_date, bs_year, bs_month, bs_day, 1)
        
       
    else:
        # st.write(f"The specified date ({day_of_week}) is not a holiday.")
        display_predictions(ad_date, bs_year, bs_month, bs_day, 0)
    
    
    
 
 
    
 
   
 
def display_predictions(ad_date, bs_year, bs_month, bs_day, is_holiday):
    api_endpoint = "http://127.0.0.1:5002/"
 
    selected_model  = "xgboost"
    day_of_week_number = get_day_of_week_number(ad_date.strftime("%A"))
 
    # Data to be sent in the request
    data = {
        "day_of_week_number": day_of_week_number,
        "is_holiday": is_holiday,
        "ad_date": ad_date.strftime("%Y-%m-%d"),
        "bs_year": bs_year,
        "bs_month": bs_month,
        "bs_day": bs_day
    }
 
    response = requests.post(api_endpoint, json=data)
 
    if response.status_code == 200:
        predictions = response.json().get('predictions', [])
        for prediction in predictions:
          temperatures = round(float(prediction['temperature']), 2)
        #   st.write(f"Predicted Temperature: {temperatures}")
        send_to_backend(day_of_week_number, is_holiday, ad_date, bs_year, bs_month, bs_day, predictions, selected_model)
        
    else:
        st.write(f"Failed to get temperature predictions. API responded with status code: {response.status_code}")
   

  







 
def send_to_backend(day_of_week_number, is_holiday, ad_date, bs_year, bs_month, bs_day, predictions, selected_model):
 
    api_endpoint = "http://127.0.0.1:5003/predict_demand"
 
    # Extract the predicted temperatures
    predicted_temperatures = [round(float(prediction['temperature']), 2) for prediction in predictions]
 
    # Data to be sent in the request
    data = {
        'day_of_week_number': day_of_week_number,
        'is_holiday': is_holiday,
        'bs_year': bs_year,
        'bs_month': bs_month,
        'bs_day': bs_day,
        'ad_date': ad_date.strftime("%Y-%m-%d"),
        'selected_model': selected_model,
        'temperatures': predicted_temperatures
    }
 
    # st.write("Data sent to the backend:", data)
 
    try:
        response = requests.post(api_endpoint, json=data)
        # st.write(response)
 
        if response.status_code == 200:
            # st.write("Data sent to the backend successfully.")
            # st.write("Response from the backend:", response.json())
       # Extract the response data
            response_data = response.json()
            

            predictions_data = response_data.get('predictions', [])
          

            # Create a DataFrame for easier plotting
            df_predictions = pd.DataFrame(predictions_data)
            
            # Convert 'hour' column to numerical values
            df_predictions['hour'] = pd.to_numeric(df_predictions['hour'])
            
 
                        # Convert 'hour' column to numerical values
            df_predictions['hour'] = pd.to_numeric(df_predictions['hour'])
            # Plot the line graph using plotly
            fig_line = px.line(df_predictions, x='hour', y='demand', title='Demand Predictions')
            st.plotly_chart(fig_line)
            # Plot the bar chart for demand predictions
            fig_bar = px.bar(df_predictions, x='hour', y='demand', title='Demand Predictions (Bar Chart)')
            st.plotly_chart(fig_bar)
                        # Plot the area plot using plotly
            # fig_area = px.area(df_predictions, x='hour', y='demand', title='Demand Predictions (Area Plot)')
            # st.plotly_chart(fig_area)
            # Calculate KPIs
            total_demand, average_demand, max_demand, min_demand = calculate_kpis(df_predictions)

    # Display KPIs
            display_kpis(total_demand, average_demand, max_demand, min_demand)
            
           
 
        else:
            st.write(f"Failed to send data. API responded with status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error sending data to the backend: {str(e)}")
 
if __name__ == "__main__":
    prediction()


 