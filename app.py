#%%
import pandas as pd
import streamlit as st

#%%
st.title("Stock Data Visualization")
df = pd.read_excel(r"data/CIT_NN.xlsx", sheet_name='files')
# %%
##df.info()
##st.dataframe(df)

# Get the minimum and maximum dates from your DataFrame
min_date = df['datetime'].min()
max_date = df['datetime'].max()

# Add a date range slider
start_date, end_date = st.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="MM/DD/YYYY"
)

# Filter the DataFrame based on the selected date range
filtered_df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

# Display the filtered DataFrame
st.dataframe(filtered_df)