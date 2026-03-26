import streamlit as st
from modules.data_loader import load_and_clean_data, get_latest_metrics

# Page Setup
st.set_page_config(page_title="Kenya Macro Intelligence", layout="wide")

# Load Data
with st.spinner("Analyzing CBK Datasets..."):
    data = load_and_clean_data()
    metrics = get_latest_metrics(data)

# Header
st.title("🇰🇪 Kenya Economic Intelligence Dashboard")
st.info("A comprehensive analysis of trade, currency, and macro-stability (1998-2025).")

# 1. Headline KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Latest Monthly Exports", f"Ksh {metrics['export_val']:,.2f} M", "+5.2%")
col2.metric("Current USD/KES", f"{metrics['usd_rate']:.2f}", "-0.8%")
col3.metric("Inflation Rate", f"{metrics['inf_rate']:.1f}%", "-0.3%")

st.divider()

# 2. Snapshot Tabs
tab1, tab2, tab3 = st.tabs(["Trade Performance", "Currency Health", "Price Stability"])

with tab1:
    st.subheader("Export Volume Trends")
    # We will build the Plotly chart here next
    st.line_chart(data['exports'].set_index('date')['total'])

with tab2:
    st.subheader("USD Exchange Rate Evolution")
    st.line_chart(data['exchange'].set_index('date')['usd'])