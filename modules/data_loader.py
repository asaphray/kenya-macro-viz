import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_and_clean_data():
    path = "data/cleaned/"
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # 1. Exchange Rate
    df_er = pd.read_csv(os.path.join(path, "exchange_rate.csv"), skiprows=1)
    df_er.columns = df_er.columns.str.strip().str.lower()
    # Handle the specific CBK column name for USD
    df_er = df_er.rename(columns={'united states dollar': 'usd', 'month': 'month_num', 'year': 'year'})
    df_er = df_er[pd.to_numeric(df_er['year'], errors='coerce').notnull()].copy()
    df_er[['year', 'month_num', 'usd']] = df_er[['year', 'month_num', 'usd']].apply(pd.to_numeric)
    df_er['date'] = pd.to_datetime(df_er['year'].astype(int).astype(str) + '-' + 
                                  df_er['month_num'].astype(int).astype(str) + '-01')

    # 2. Exports
    df_exports = pd.read_csv(os.path.join(path, "value_domestic_exports.csv"))
    df_exports.columns = df_exports.columns.str.strip().str.lower()
    df_exports['month_num'] = df_exports['month'].str.capitalize().map(month_map)
    df_exports['date'] = pd.to_datetime(df_exports['year'].astype(str) + '-' + 
                                       df_exports['month_num'].astype(str) + '-01')

    # 3. Inflation (The tricky one)
    df_inf = pd.read_csv(os.path.join(path, "inflation.csv"))
    df_inf.columns = df_inf.columns.str.strip().str.lower()
    
    # Dynamically find the inflation column (look for 'overall' and 'inflation')
    inf_col = [c for c in df_inf.columns if 'overall' in c and 'inflation' in c]
    if inf_col:
        df_inf = df_inf.rename(columns={inf_col[0]: 'inflation_rate'})
    
    df_inf['month_num'] = df_inf['month'].str.capitalize().map(month_map)
    df_inf['date'] = pd.to_datetime(df_inf['year'].astype(str) + '-' + 
                                   df_inf['month_num'].astype(str) + '-01')
    
    return {
        "exchange": df_er.sort_values('date'),
        "exports": df_exports.sort_values('date'),
        "inflation": df_inf.sort_values('date')
    }

def get_latest_metrics(data):
    """Extracts headline figures using the NEW standardized names"""
    latest_ex = data['exports'].iloc[-1]
    latest_er = data['exchange'].iloc[-1]
    latest_inf = data['inflation'].iloc[-1]
    
    return {
        "export_val": latest_ex['total'],
        "usd_rate": latest_er['usd'],
        "inf_rate": latest_inf['inflation_rate'] # Now matches the rename logic above
    }