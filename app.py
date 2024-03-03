#%%
import pandas as pd
import streamlit as st

#%%
st.title("Stock Data Visualization 2")
df = pd.read_excel(r"data/CIT_NN.xlsx", sheet_name='files')
# %%
df['datetime'] = pd.to_datetime(df['datetime'])

# Get the minimum and maximum dates from your DataFrame
min_date = df['datetime'].min()
max_date = df['datetime'].max()

# Use a slider to select the date range, using datetime objects directly
start_date, end_date = st.slider(
    'Select Date Range',
    value=(min_date, max_date),
    format='MM/DD/YYYY'
)

# Filter the DataFrame based on the selected date range
filtered_df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

# Display the filtered DataFrame
st.dataframe(filtered_df)