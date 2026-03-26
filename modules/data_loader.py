import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_and_clean_data():
    """
    Centralized loader for all CBK datasets.
    Handles pathing and initial cleaning for consistency.
    """
    path = "data/cleaned/"
    
    # Helper to map month names to numbers
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # 1. Exchange Rate Cleaning
    df_er = pd.read_csv(os.path.join(path, "exchange_rate.csv"), skiprows=1)
    df_er.columns = [
        'year', 'month_num', 'usd', 'gbp', 'euro', 'sa_rand', 'ugx', 'tzs', 
        'rwf', 'bif', 'ae_dirham', 'dem', 'cad', 'frf', 'chf', 'nlg', 'itl', 
        'bef', 'jpy_100', 'sek', 'nok', 'dkk', 'ats', 'fim', 'esp', 'inr', 
        'hkd', 'sgd', 'sar', 'cny', 'aud'
    ]
    # Filter for numeric years and convert
    df_er = df_er[pd.to_numeric(df_er['year'], errors='coerce').notnull()].copy()
    df_er[['year', 'month_num', 'usd']] = df_er[['year', 'month_num', 'usd']].apply(pd.to_numeric)
    df_er['date'] = pd.to_datetime(df_er['year'].astype(int).astype(str) + '-' + 
                                  df_er['month_num'].astype(int).astype(str) + '-01')

    # 2. Domestic Exports Cleaning
    df_exports = pd.read_csv(os.path.join(path, "value_domestic_exports.csv"))
    df_exports['month_num'] = df_exports['month'].map(month_map)
    df_exports['date'] = pd.to_datetime(df_exports['year'].astype(str) + '-' + 
                                       df_exports['month_num'].astype(str) + '-01')

    # 3. Inflation Cleaning
    df_inf = pd.read_csv(os.path.join(path, "inflation.csv"))
    df_inf['month_num'] = df_inf['Month'].map(month_map)
    df_inf['date'] = pd.to_datetime(df_inf['Year'].astype(str) + '-' + 
                                   df_inf['month_num'].astype(str) + '-01')
    
    # 4. GDP Cleaning
    df_gdp = pd.read_csv(os.path.join(path, "gdp.csv"))

    return {
        "exchange": df_er.sort_values('date'),
        "exports": df_exports.sort_values('date'),
        "inflation": df_inf.sort_values('date'),
        "gdp": df_gdp
    }

def get_latest_metrics(data):
    """Extracts headline figures for the Home Dashboard KPIs"""
    latest_ex = data['exports'].iloc[-1]
    latest_er = data['exchange'].iloc[-1]
    latest_inf = data['inflation'].iloc[-1]
    
    return {
        "export_val": latest_ex['total'],
        "usd_rate": latest_er['usd'],
        "inf_rate": latest_inf['Overall.12.month.inflation']
    }