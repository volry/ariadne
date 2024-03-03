import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Stock Data Visualization 2")
df = pd.read_excel(r"data/CIT_NN.xlsx", sheet_name='files')

df['datetime'] = pd.to_datetime(df['datetime'])



# Allow user to select a ticker
ticker = st.selectbox('Select a stock ticker:', df['stocks'].unique())

# Filter the DataFrame for the selected ticker
ticker_data = df[df['stocks'] == ticker]

# Plot and display the data for the selected ticker
fig = px.line(ticker_data, x='datetime', y='close', title=f'Closing Price of {ticker} Over Time')
st.plotly_chart(fig)
