import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from scipy import stats

# Set page title
st.set_page_config(page_title="Advanced Restaurant Performance Dashboard", layout="wide")

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
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'].apply(lambda x: x.split('-')[0]))  # Convert to datetime
    return df

df = load_data()

# Sidebar for configuration
st.sidebar.title("Dashboard Configuration")

# Date Range Selector
start_date = st.sidebar.date_input("Start Date", min(df['Date']))
end_date = st.sidebar.date_input("End Date", max(df['Date']))

# Filter data based on date range
mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# Metric Selector
metrics = st.sidebar.multiselect("Select Metrics for Analysis", ['Labor', 'Food Cost', 'Total Sales', 'Profit'], default=['Total Sales', 'Profit'])

# Main dashboard
st.title("Advanced Restaurant Performance Dashboard")

# KPI Cards
st.subheader("Key Performance Indicators")
kpi_cols = st.columns(4)
kpis = ['Total Sales', 'Profit', 'Labor %', 'Food Cost %']
for i, kpi in enumerate(kpis):
    kpi_cols[i].metric(kpi, f"${filtered_df[kpi].mean():.2f}" if '$' in kpi else f"{filtered_df[kpi].mean():.2%}")

# Create visualizations
st.subheader("Performance Metrics Over Time")

# Line chart for selected metrics
fig = go.Figure()
for metric in metrics:
    fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[metric], mode='lines+markers', name=metric))

fig.update_layout(title='Financial Metrics Over Time', xaxis_title='Date', yaxis_title='Amount ($)')
st.plotly_chart(fig, use_container_width=True)

# Stacked Area Chart
st.subheader("Expense Breakdown")
fig_area = px.area(filtered_df, x='Date', y=['Labor', 'Food Cost'], title='Labor and Food Cost Over Time')
st.plotly_chart(fig_area, use_container_width=True)

# Pie Chart for average expense distribution
st.subheader("Average Expense Distribution")
avg_expenses = filtered_df[['Labor', 'Food Cost']].mean()
fig_pie = px.pie(values=avg_expenses.values, names=avg_expenses.index, title='Average Expense Distribution')
st.plotly_chart(fig_pie, use_container_width=True)

# Advanced Statistical Analysis
st.subheader("Advanced Statistical Analysis")

selected_metric = st.selectbox("Select Metric for Statistical Analysis", metrics)

# Calculate basic statistics
mean = filtered_df[selected_metric].mean()
median = filtered_df[selected_metric].median()
std_dev = filtered_df[selected_metric].std()

st.write(f"Mean {selected_metric}: ${mean:.2f}")
st.write(f"Median {selected_metric}: ${median:.2f}")
st.write(f"Standard Deviation of {selected_metric}: ${std_dev:.2f}")

# Perform linear regression
X = filtered_df.index.values.reshape(-1, 1)
y = filtered_df[selected_metric].values
slope, intercept, r_value, p_value, std_err = stats.linregress(X.flatten(), y)

st.write(f"Linear Regression Results for {selected_metric}:")
st.write(f"Slope: {slope:.2f}")
st.write(f"Intercept: {intercept:.2f}")
st.write(f"R-squared: {r_value**2:.2f}")
st.write(f"P-value: {p_value:.4f}")

# Plot regression line
fig_regression = px.scatter(filtered_df, x=filtered_df.index, y=selected_metric, trendline="ols", title=f'{selected_metric} Trend with Regression Line')
st.plotly_chart(fig_regression, use_container_width=True)

# What-if Scenario Analysis
st.subheader("What-if Scenario Analysis")

st.write("Adjust the parameters below to see how they affect the profit:")

labor_change = st.slider("Change in Labor Cost (%)", -50, 50, 0)
food_cost_change = st.slider("Change in Food Cost (%)", -50, 50, 0)
sales_change = st.slider("Change in Total Sales (%)", -50, 50, 0)

# Calculate new values
new_labor = filtered_df['Labor'].mean() * (1 + labor_change/100)
new_food_cost = filtered_df['Food Cost'].mean() * (1 + food_cost_change/100)
new_sales = filtered_df['Total Sales'].mean() * (1 + sales_change/100)
new_profit = new_sales - new_labor - new_food_cost

st.write(f"Estimated New Profit: ${new_profit:.2f}")
st.write(f"Current Average Profit: ${filtered_df['Profit'].mean():.2f}")
st.write(f"Profit Change: ${new_profit - filtered_df['Profit'].mean():.2f}")

# Data Download
st.subheader("Download Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="restaurant_performance_data.csv",
    mime="text/csv",
)

# Display raw data
st.subheader("Raw Data")
st.dataframe(filtered_df)