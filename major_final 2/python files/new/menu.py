import pandas as pd
import streamlit as st
import nepali_datetime
from datetime import datetime, timedelta
import requests
from nepali_datetime import date as nepali_date
import plotly.express as px
import os
 
def convert_to_ad_date(date_str):
    try:
        bs_year, bs_month, bs_day = map(int, date_str.split('-'))
        bs_date = nepali_datetime.date(bs_year, bs_month, bs_day)
        ad_date = bs_date.to_datetime_date()
        return ad_date
    except ValueError:
        raise ValueError("Invalid date format. Please use 'YYYY-MM-DD' format.")
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
    
 
def get_holidays(year):
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
            if current_date.weekday() == 7:  # Saturday
                holidays_data["holidays"].append({
                    'name': 'Saturday',
                    'date': current_date.strftime('%Y-%m-%d'),
                })
            current_date += timedelta(days=1)
        return holidays_data['holidays']
    except Exception as e:
        st.error(f"Error fetching holidays: {str(e)}")
        return []
 
def is_selected_date_holiday(holidays, selected_date):
    selected_date_str = selected_date.strftime("%Y-%m-%d")
    for holiday in holidays:
        if holiday.get('date') == selected_date_str:
            return True, holiday.get('name')
    return False, None
 
def get_day_of_week_number(day_of_week):
    day_number_mapping = {
        'Monday': 2, 'Tuesday': 3, 'Wednesday': 4,
        'Thursday': 5, 'Friday': 6, 'Saturday': 7, 'Sunday': 1,
    }
    return day_number_mapping.get(day_of_week, 0)
 
def menu():
    st.write("Welcome to prediction!")
    # selected_model = st.selectbox("Select Model", ["linear_regression", "xgboost", "svm", "knn"])
    selected_model = "xgboost"
    start_date_bs = st.text_input("Enter Start Date (BS) in 'YYYY-MM-DD' format:")
    end_date_bs = st.text_input("Enter End Date (BS) in 'YYYY-MM-DD' format:")
 
    if st.button("Submit"):
        try:
            combined_data = pd.read_excel("/Users/paweshashrestha/Downloads/major_final 2/python files/new/combined_predictions.xlsx")
 
            excel_filename = "combined_predictions.xlsx"
            if os.path.exists(excel_filename):
                os.remove(excel_filename)
                        # Filter data based on selected date range
            mask = (pd.to_datetime(combined_data['date']) >= start_date_bs) & \
                   (pd.to_datetime(combined_data['date']) <= end_date_bs)
            filtered_data = combined_data.loc[mask]
 
            for current_date in pd.date_range(start=start_date_bs, end=end_date_bs):
                bs_year, bs_month, bs_day = current_date.year, current_date.month, current_date.day
                day_of_week = current_date.strftime("%A")
                holidays = get_holidays(current_date.year)
                is_holiday_today, _ = is_selected_date_holiday(holidays, current_date)
                day_of_week_number = get_day_of_week_number(day_of_week)
                display_predictions(current_date, bs_year, bs_month, bs_day, is_holiday_today, selected_model)
            # # Calculate KPIs based on the selected date range
            # total_demand, average_demand, max_demand, min_demand = calculate_kpis(filtered_data)
 
            # # Display KPIs
            # display_kpis(total_demand, average_demand, max_demand, min_demand)
 
            display_aggregated_graph_line()
            display_aggregated_graph_bar()
 
        except ValueError as e:
            st.error(str(e))
 
def display_predictions(ad_date, bs_year, bs_month, bs_day, is_holiday, selected_model):
    api_endpoint = "http://127.0.0.1:5002/"
    day_of_week_number = get_day_of_week_number(ad_date.strftime("%A"))
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
        send_to_backend(day_of_week_number, is_holiday, ad_date, bs_year, bs_month, bs_day, predictions, selected_model)
        return predictions
    return []
 
def display_aggregated_graph_line():
    try:
        excel_filename = "combined_predictions.xlsx"
        combined_data = pd.read_excel(excel_filename)
        aggregated_data_line = combined_data.groupby('date')['demand'].mean().reset_index()
        
        # Check if the range of dates is more than 2 years
        date_range = pd.to_datetime(aggregated_data_line['date'])
        if (date_range.max() - date_range.min()).days > 365 * 2:
            # Format tick labels to display only months
            tickformat = '%m\n%Y'
        else:
            # Format tick labels to display days when the range is within 2 years
            tickformat = '%d-%m-%Y'
        
        fig_demand_aggregated_line = px.line(aggregated_data_line, x='date', y='demand', title='Aggregated Demand vs. Date')
        
        # Update x-axis tick format
        fig_demand_aggregated_line.update_xaxes(tickformat=tickformat)
        
        st.plotly_chart(fig_demand_aggregated_line)
    except Exception as e:
        st.error(f"Error displaying aggregated graph: {str(e)}")
 
 
def display_aggregated_graph_bar():
    try:
        excel_filename = "combined_predictions.xlsx"
        combined_data = pd.read_excel(excel_filename)
        aggregated_data = combined_data.groupby('date')['demand'].mean().reset_index()
        
        # Simplify date format for every label if the difference between months is more than 2
        aggregated_data['date'] = pd.to_datetime(aggregated_data['date'])
        min_date = aggregated_data['date'].min()
        max_date = aggregated_data['date'].max()
        if (max_date - min_date).days / 30 > 2:
            aggregated_data['date'] = aggregated_data['date'].dt.strftime('%Y-%m')
        else:
            aggregated_data['date'] = aggregated_data['date'].dt.strftime('%Y-%m-%d')
 
        fig_demand_bar = px.bar(aggregated_data, x='date', y='demand', title='Aggregated Demand vs. Date')
        fig_demand_bar.update_xaxes(type='category', tickmode='linear', dtick=1)
        st.plotly_chart(fig_demand_bar)
    except Exception as e:
        st.error(f"Error displaying aggregated bar graph: {str(e)}")
 
 
 
 
def send_to_backend(day_of_week_number, is_holiday, ad_date, bs_year, bs_month, bs_day, predictions, selected_model):
    api_endpoint = "http://127.0.0.1:5003/predict_demand"
    predicted_temperatures = [round(float(prediction['temperature']), 2) for prediction in predictions]
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
    try:
        response = requests.post(api_endpoint, json=data)
        if response.status_code == 200:
            response_data = response.json()
            predictions_data = response_data.get('predictions', [])
            df_predictions = pd.DataFrame(predictions_data)
            bs_date_format = [nepali_datetime.date(bs_year, bs_month, bs_day).strftime("%Y-%m-%d") for _ in range(len(df_predictions))]
            df_predictions['date'] = bs_date_format
            excel_filename = "combined_predictions.xlsx"
            if os.path.exists(excel_filename):
                existing_data = pd.read_excel(excel_filename)
                combined_data = pd.concat([existing_data, df_predictions], ignore_index=True)
            else:
                combined_data = df_predictions.copy()
            combined_data.to_excel(excel_filename, index=False)
        else:
            st.write(f"Failed to send data. API responded with status code: {response.status_code}")
    except Exception as e:
        # st.error(f"Error sending data to the backend: {str(e)}")
        print("Error sending data to the backend:" ,e)
 
if __name__ == "__main__":
    menu()