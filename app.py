import streamlit as st
from modules.data_loader import load_and_clean_data, get_latest_metrics
from modules.charts import plot_exchange_trends, plot_real_vs_nominal, plot_inflation_trend

# 1. Page Config & Setup
st.set_page_config(page_title="Kenya Macro Analysis", layout="wide")
data = load_and_clean_data()
metrics = get_latest_metrics(data)

st.title("🇰🇪 Kenya Economic Intelligence Dashboard")

# 2. Top-Level Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Monthly Exports", f"Ksh {metrics['export_val']:,.0f}M", "Real Growth")
col2.metric("USD/KES Rate", f"{metrics['usd_rate']:.2f}", "Currency Trend")
col3.metric("Inflation Rate", f"{metrics['inf_rate']:.1f}%", "Price Stability")

st.divider()

# 3. Interactive Snapshot Tabs
tab1, tab2, tab3 = st.tabs(["Trade Performance", "Currency Health", "Inflation Index"])

with tab1:
    # Pass both exports and exchange data to show Real vs Nominal
    fig_trade = plot_real_vs_nominal(data['exports'], data['exchange'])
    st.plotly_chart(fig_trade, use_container_width=True)

with tab2:
    fig_er = plot_exchange_trends(data['exchange'])
    st.plotly_chart(fig_er, use_container_width=True)

with tab3:
    fig_inf = plot_inflation_trend(data['inflation'])
    st.plotly_chart(fig_inf, use_container_width=True)