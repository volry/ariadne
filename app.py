import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load your data
df = pd.read_excel("data/CIT_NN.xlsx", sheet_name='files')
df['datetime'] = pd.to_datetime(df['datetime'])

# Allow user to select a ticker
ticker = st.selectbox('Select a stock ticker:', df['stocks'].unique())

# Filter the DataFrame for the selected ticker
ticker_data = df[df['stocks'] == ticker]

# Create and display an OHLC chart
fig = go.Figure(data=go.Ohlc(x=ticker_data['datetime'],
                             open=ticker_data['open'],
                             high=ticker_data['high'],
                             low=ticker_data['low'],
                             close=ticker_data['close']))
fig.update_layout(title=f'OHLC Chart for {ticker}',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  xaxis_rangeslider_visible=False)
st.plotly_chart(fig)

