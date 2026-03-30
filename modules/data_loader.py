import pandas as pd
import streamlit as st
import os

def clean_column_names(df):
    """Strip spaces and lowercase all column names for consistency"""
    df.columns = df.columns.str.strip().str.lower()
    return df

@st.cache_data
def load_and_clean_data():
    path = "data/cleaned/"
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # --- 1. Exchange Rate ---
    df_er = pd.read_csv(os.path.join(path, "exchange_rate.csv"), skiprows=1)
    df_er = clean_column_names(df_er)
    df_er = df_er.rename(columns={'united states dollar': 'usd', 'month': 'month_num', 'year': 'year'})
    df_er = df_er[pd.to_numeric(df_er['year'], errors='coerce').notnull()].copy()
    df_er['date'] = pd.to_datetime(df_er['year'].astype(int).astype(str) + '-' + 
                                  df_er['month_num'].astype(int).astype(str) + '-01')

    # --- 2. Exports ---
    df_exports = pd.read_csv(os.path.join(path, "value_domestic_exports.csv"))
    df_exports = clean_column_names(df_exports)
    # Ensure we handle 'month' or 'month '
    df_exports['month_num'] = df_exports['month'].str.capitalize().map(month_map)
    df_exports['date'] = pd.to_datetime(df_exports['year'].astype(str) + '-' + 
                                       df_exports['month_num'].astype(str) + '-01')

    # --- 3. Inflation ---
    df_inf = pd.read_csv(os.path.join(path, "inflation.csv"))
    df_inf = clean_column_names(df_inf)
    df_inf['month_num'] = df_inf['month'].str.capitalize().map(month_map)
    df_inf['date'] = pd.to_datetime(df_inf['year'].astype(str) + '-' + 
                                   df_inf['month_num'].astype(str) + '-01')
    
    # Fuzzy find inflation rate
    inf_target = next((c for c in df_inf.columns if 'overall' in c or '12' in c), df_inf.columns[-1])
    df_inf['inflation_rate'] = df_inf[inf_target]

    # --- 4. Africa & ROW ---
    df_af = clean_column_names(pd.read_csv(os.path.join(path, "value_exports_african.csv")))
    df_row = clean_column_names(pd.read_csv(os.path.join(path, "value_exports_restofworld.csv")))
    
    # Add dates to these as well for the Regional page
    for df in [df_af, df_row]:
        df['month_num'] = df['month'].str.capitalize().map(month_map)
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month_num'].astype(str) + '-01')

    return {
        "exchange": df_er.sort_values('date'),
        "exports": df_exports.sort_values('date'),
        "inflation": df_inf.sort_values('date'),
        "africa": df_af.sort_values('date'),
        "row": df_row.sort_values('date')
    }

def get_latest_metrics(data):
    """Safely extract metrics using lowercase keys"""
    try:
        # We use .iloc[-1] to get the most recent month's data
        latest_ex = data['exports'].iloc[-1]
        latest_er = data['exchange'].iloc[-1]
        latest_inf = data['inflation'].iloc[-1]
        
        return {
            "export_val": float(latest_ex['total']),
            "usd_rate": float(latest_er['usd']),
            "inf_rate": float(latest_inf['inflation_rate'])
        }
    except Exception as e:
        # If columns are STILL missing, this prevents the app from crashing
        st.warning(f"Note: Some metrics couldn't be loaded. Check CSV column names.")
        return {"export_val": 0.0, "usd_rate": 0.0, "inf_rate": 0.0}