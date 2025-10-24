# --------------------------------------------------------------------- # 
#                               Library
# --------------------------------------------------------------------- # 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt
import os

# --------------------------------------------------------------------- # 
#                               Datasets
# --------------------------------------------------------------------- # 
# Fetch current working directory
current_path = os.getcwd()

# Define file name
file_1 = 'Plant1.csv'
file_2 = 'Plant2.csv'

# Define path
path_1 = os.path.join(current_path,file_1)
path_2 = os.path.join(current_path,file_2)

# Read datasets
df_1 = pd.read_csv(path_1)
df_2 = pd.read_csv(path_2)

# Drop from all datasets
df_1.drop('DATE',axis=1,inplace=True)
df_2.drop('DATE',axis=1,inplace=True)
df_1.drop('TIME',axis=1,inplace=True)
df_2.drop('TIME',axis=1,inplace=True)

# Reformat the date-time accordingly
df_1['DATE_TIME'] = pd.to_datetime(df_1['DATE_TIME'], infer_datetime_format=True)
df_2['DATE_TIME'] = pd.to_datetime(df_2['DATE_TIME'], infer_datetime_format=True)
df_1['DATE'] = pd.to_datetime(df_1['DATE_TIME'].dt.date)
df_2['DATE'] = pd.to_datetime(df_2['DATE_TIME'].dt.date)
df_1['TIME'] = df_1['DATE_TIME'].dt.time
df_2['TIME'] = df_2['DATE_TIME'].dt.time

# Streamlit
st.set_page_config("Solar Energy",page_icon="🌞", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='color: white; text-align: center; font-weight: bold;'>Data Analysis | Solar Energy</h1>",
            unsafe_allow_html=True)

# --------------------------------------------------------------------- # 
#                  Plant I - Power Generation - Yield
# --------------------------------------------------------------------- # 
st.markdown("<h1 style='color: white; text-align: center; text-decoration: underline;'>Plant I - Yield</h1>", 
            unsafe_allow_html=True)

# Daily Yield
# Daily Production Density per Source
daily_yield  = df_1.groupby(df_1['DATE'])['TOTAL_YIELD'].sum().reset_index()

# Create an Altair chart
chart = alt.Chart(daily_yield).mark_bar(color='#FF8C00').encode(x=alt.X('DATE:T',        title='Date'),
                                                                y=alt.Y('TOTAL_YIELD:Q', title='Energy Production (kW)')
                                                                ).properties(title='Total Yield Over Time').configure_title(
                                                                anchor='middle')

# Display the Altair chart in Streamlit
st.altair_chart(chart, use_container_width=True)

# Line plot
# Get sum DAILY_YIELD per inverter per day
daily_energy_per_inverter = df_1.groupby(['SOURCE_KEY', 'DATE'])['DAILY_YIELD'].sum().reset_index()

# Pivot for inverter-by-date table (optional)
pivot_table = daily_energy_per_inverter.pivot(index='DATE', columns='SOURCE_KEY', values='DAILY_YIELD')

# Plot selected inverters
selected_inverters = pivot_table.columns[:]  # pick first 3 inverters (or specify)

st.line_chart(pivot_table[selected_inverters], x_label='Date', y_label='Energy Production (kW)')

# Box plot
# datasets
df = df_1[['SOURCE_KEY','DAILY_YIELD']]

# enable large dataset
alt.data_transformers.disable_max_rows()

# Define a custom color list similar to Seaborn's "autumn"
autumn_palette = ['#f59b2d', '#b15928', '#ffd700', '#f4794e']

chart = alt.Chart(df).mark_boxplot().encode(
                                        x=alt.X('SOURCE_KEY:N',        title='Source Key'),
                                        y=alt.Y('DAILY_YIELD:Q',       title='Energy Production (kW)'),
                                        color=alt.Color('category:N', scale=alt.Scale(range=autumn_palette), legend=None)
                                        ).properties(
                                            title='Daily Yield Per Inverter'
                                        ).configure_title(
                                            anchor='middle'
                                        )

# Display the Altair chart in Streamlit
st.altair_chart(chart, use_container_width=True)
