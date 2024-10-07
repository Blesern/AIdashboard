import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title (this must be the first Streamlit command)
st.set_page_config(page_title="Restaurant Performance Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    data = {
        'Date': ['2024/09/16-2024/09/22', '2024/09/23-2024/09/29', '2024/09/30-2024/10/06', '2024/10/07-2024/10/13', '2024/10/14-2024/10/20'],
        'Labor': [2726.2, 2700.8, 2765.4, 2850.5, 2780.3],
        'Food Cost': [3409.72, 3380.5, 3425.8, 3550.25, 3480.6],
        'Total Sales': [8440.43, 8300.25, 8500.6, 8750.8, 8600.2],
        'Profit': [2304.51, 2218.95, 2309.4, 2350.05, 2339.3],
        'Labor %': [0.322993, 0.3254, 0.3253, 0.3257, 0.3233],
        'Food Cost %': [0.403975, 0.4073, 0.403, 0.4057, 0.4047],
        'Profit %': [0.273032, 0.2673, 0.2717, 0.2686, 0.272]
    }
    return pd.DataFrame(data)

df = load_data()

# Title
st.title("Restaurant Performance Dashboard")

# Display raw data
st.subheader("Raw Data")
st.dataframe(df)

# Create visualizations
st.subheader("Performance Metrics Over Time")

# Line chart for Labor, Food Cost, Total Sales, and Profit
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Labor'], mode='lines+markers', name='Labor'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Food Cost'], mode='lines+markers', name='Food Cost'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Total Sales'], mode='lines+markers', name='Total Sales'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Profit'], mode='lines+markers', name='Profit'))

fig.update_layout(title='Financial Metrics Over Time', xaxis_title='Date', yaxis_title='Amount ($)')
st.plotly_chart(fig, use_container_width=True)

# Bar chart for Labor %, Food Cost %, and Profit %
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=df['Date'], y=df['Labor %'], name='Labor %'))
fig2.add_trace(go.Bar(x=df['Date'], y=df['Food Cost %'], name='Food Cost %'))
fig2.add_trace(go.Bar(x=df['Date'], y=df['Profit %'], name='Profit %'))

fig2.update_layout(title='Percentage Metrics Over Time', xaxis_title='Date', yaxis_title='Percentage', barmode='group')
st.plotly_chart(fig2, use_container_width=True)

# Display key metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Weekly Sales", f"${df['Total Sales'].mean():.2f}")
with col2:
    st.metric("Average Weekly Profit", f"${df['Profit'].mean():.2f}")
with col3:
    st.metric("Average Labor %", f"{df['Labor %'].mean():.2%}")
with col4:
    st.metric("Average Food Cost %", f"{df['Food Cost %'].mean():.2%}")