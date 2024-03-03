import pandas as pd
import streamlit as st

st.title("Stock Data Visualization 2")
df = pd.read_excel(r"data/CIT_NN.xlsx", sheet_name='files')

df['datetime'] = pd.to_datetime(df['datetime'])

# Get the minimum and maximum dates from your DataFrame
min_date = df['datetime'].min()
max_date = df['datetime'].max()

# Use two date_input widgets for start and end dates
start_date = st.date_input('Start date', min_date)
end_date = st.date_input('End date', max_date)

# Ensure end_date is after start_date
if start_date > end_date:
    st.error('Error: End date must fall after start date.')

# Filter the DataFrame based on the selected date range
filtered_df = df[(df['datetime'] >= pd.to_datetime(start_date)) & (df['datetime'] <= pd.to_datetime(end_date))]

# Display the filtered DataFrame
st.dataframe(filtered_df)
