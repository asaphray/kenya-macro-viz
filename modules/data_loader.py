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

    # --- 1. Exchange Rate ---
    df_er = pd.read_csv(os.path.join(path, "exchange_rate.csv"), skiprows=1)
    df_er.columns = df_er.columns.str.strip().str.lower()
    df_er = df_er.rename(columns={'united states dollar': 'usd', 'month': 'month_num', 'year': 'year'})
    df_er = df_er[pd.to_numeric(df_er['year'], errors='coerce').notnull()].copy()
    df_er['date'] = pd.to_datetime(df_er['year'].astype(int).astype(str) + '-' + 
                                  df_er['month_num'].astype(int).astype(str) + '-01')

    # --- 2. Exports ---
    df_exports = pd.read_csv(os.path.join(path, "value_domestic_exports.csv"))
    df_exports.columns = df_exports.columns.str.strip().str.lower()
    df_exports['month_num'] = df_exports['month'].str.capitalize().map(month_map)
    df_exports['date'] = pd.to_datetime(df_exports['year'].astype(str) + '-' + 
                                       df_exports['month_num'].astype(str) + '-01')

    # --- 3. Inflation (High Stability Mode) ---
    df_inf = pd.read_csv(os.path.join(path, "inflation.csv"))
    df_inf.columns = df_inf.columns.str.strip().str.lower()
    
    # Map months and years
    df_inf['month_num'] = df_inf['month'].str.capitalize().map(month_map)
    df_inf['date'] = pd.to_datetime(df_inf['year'].astype(str) + '-' + 
                                   df_inf['month_num'].astype(str) + '-01')
    
    # Identify the inflation rate column safely
    # If a column has 'overall' or '12' (for 12-month) use it, otherwise take the last column
    cols = df_inf.columns.tolist()
    target_col = next((c for c in cols if 'overall' in c or '12' in c), cols[-1])
    df_inf['inflation_rate'] = df_inf[target_col]

    return {
        "exchange": df_er.sort_values('date'),
        "exports": df_exports.sort_values('date'),
        "inflation": df_inf.sort_values('date')
    }

def get_latest_metrics(data):
    """Safely extract metrics with default fallbacks to prevent KeyError crashes"""
    try:
        latest_ex = data['exports'].iloc[-1]
        latest_er = data['exchange'].iloc[-1]
        latest_inf = data['inflation'].iloc[-1]
        
        # Use .get() or check keys to be 100% safe
        return {
            "export_val": latest_ex.get('total', 0),
            "usd_rate": latest_er.get('usd', 0),
            "inf_rate": latest_inf.get('inflation_rate', 0)
        }
    except Exception as e:
        # If this fails, the app still runs but shows 0s
        return {"export_val": 0, "usd_rate": 0, "inf_rate": 0}