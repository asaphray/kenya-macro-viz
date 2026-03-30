import plotly.express as px
import plotly.graph_objects as go

def plot_exchange_trends(df):
    """Line chart for USD, GBP, and Euro trends"""
    fig = px.line(df, x='date', y=['usd', 'gbp', 'euro'],
                  title='<b>Currency Volatility Trends</b>',
                  labels={'value': 'KES per Unit', 'variable': 'Currency', 'date': 'Year'},
                  color_discrete_map={'usd': '#2c3e50', 'gbp': '#e74c3c', 'euro': '#27ae60'})
    
    fig.update_layout(
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )
    return fig

def plot_real_vs_nominal(df_exports, df_er):
    """Calculates and plots the Nominal vs Real export growth"""
    # Merge datasets internally
    df_merged = df_exports.merge(df_er[['date', 'usd']], on='date')
    df_merged['total_usd'] = df_merged['total'] / df_merged['usd']
    
    fig = go.Figure()
    # Nominal KES Line
    fig.add_trace(go.Scatter(x=df_merged['date'], y=df_merged['total'],
                             name='Nominal (KES Millions)',
                             line=dict(color='#2c3e50', width=2)))
    # Real USD Line (Scaled for visual trend comparison)
    fig.add_trace(go.Scatter(x=df_merged['date'], y=df_merged['total_usd'] * 100,
                             name='Real (USD Millions x 100)',
                             line=dict(color='#e74c3c', width=2, dash='dash')))
    
    fig.update_layout(
        title='<b>Export Growth: Nominal (KES) vs. Real (USD)</b>',
        xaxis_title='Year',
        yaxis_title='Value',
        hovermode='x unified',
        template="plotly_white",
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

def plot_inflation_trend(df_inf):
    """Visualizes the 12-month inflation rate"""
    fig = px.area(df_inf, x='date', y='Overall.12.month.inflation',
                  title='<b>Consumer Price Stability (Inflation)</b>',
                  labels={'Overall.12.month.inflation': 'Inflation %', 'date': 'Year'},
                  color_discrete_sequence=['#f39c12'])
    
    # Add a 'Target Range' horizontal band (usually 5-7.5% for Kenya)
    fig.add_hrect(y0=5, y1=7.5, line_width=0, fillcolor="green", opacity=0.1, 
                  annotation_text="CBK Target Range", annotation_position="top left")
    
    fig.update_layout(template="plotly_white")
    return fig