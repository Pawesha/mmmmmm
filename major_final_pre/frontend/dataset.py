import streamlit as st
import pandas as pd
import os
import warnings

def remove_zeros_and_format_date(date_value):
    if isinstance(date_value, str):
        date_value = pd.to_datetime(date_value, errors='coerce')

    if pd.notna(date_value) and date_value.hour == 0 and date_value.minute == 0 and date_value.second == 0:
        return date_value.strftime('%Y/%m/%d')
    return pd.NaT

def filter_by_year_month(df, year, month):
    start_date = pd.to_datetime(f"{year}-{month}-01", format='%Y-%m-%d')
    end_date = start_date + pd.offsets.MonthEnd(0)
    return df[(df["Date"] >= start_date) & (df["Date"] <= end_date)].copy()

def dataset():
    st.write("Welcome to dataset!")

    warnings.filterwarnings('ignore')

    st.title(" :bar_chart: Electricity ")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))

    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_excel(fl)

        date_column = 'Date'
        df[date_column] = df[date_column].apply(remove_zeros_and_format_date)

        df = df.dropna(subset=[date_column])

        st.dataframe(df)

        col1, col2 = st.columns(2)
        startDate = pd.to_datetime(df["Date"]).min()
        endDate = pd.to_datetime(df["Date"]).max()
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

        filtered_df = df[(pd.to_datetime(df["Date"]) >= date1) & (pd.to_datetime(df["Date"]) <= date2)].copy()

        st.dataframe(filtered_df)

        year = st.text_input("Enter Year (BS):")
        month = st.text_input("Enter Month (BS):")

        if year and month:
            year = int(year)
            month = int(month)
            year_month_filtered_df = filter_by_year_month(df, year, month)
            st.dataframe(year_month_filtered_df)

    else:
        
        df = pd.read_excel("./dataset/input/dataset.xlsx")

        date_column = 'Date'
        df[date_column] = df[date_column].apply(remove_zeros_and_format_date)

        df = df.dropna(subset=[date_column])

        st.dataframe(df)

        col1, col2 = st.columns(2)
        startDate = pd.to_datetime(df["Date"]).min()
        endDate = pd.to_datetime(df["Date"]).max()
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

        filtered_df = df[(pd.to_datetime(df["Date"]) >= date1) & (pd.to_datetime(df["Date"]) <= date2)].copy()

        st.dataframe(filtered_df)

# Call the dataset function when needed
if hasattr(st.session_state, 'show_dataset') and st.session_state.show_dataset:
    dataset()
