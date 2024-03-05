import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load your data
df = pd.read_excel("data/CIT_NN.xlsx", sheet_name='files')


df['datetime'] = pd.to_datetime(df['datetime'])

# Use the sidebar for ticker selection
ticker = st.sidebar.selectbox('Select a stock ticker:', df['stocks'].unique())

# Filter the DataFrame for the selected ticker
ticker_data = df[df['stocks'] == ticker]

# Create the subplots
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                    subplot_titles=('OHLC', 'Volume', 'Indicators'),
                    row_heights=[0.5, 0.2, 0.3])

# OHLC chart
fig.add_trace(go.Candlestick(x=ticker_data['datetime'],
                             open=ticker_data['open'],
                             high=ticker_data['high'],
                             low=ticker_data['low'],
                             close=ticker_data['close'],
                             name='OHLC'), row=1, col=1)

# Volume chart
fig.add_trace(go.Bar(x=ticker_data['datetime'],
                     y=ticker_data['volume'],
                     name='Volume'), row=2, col=1)

# Indicator chart
fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Enter_predicted'],
                         mode='lines', name='Enter Predicted',
                         line=dict(color='green', width=2)), row=3, col=1)

fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Exit_predicted'],
                         mode='lines', name='Exit Predicted',
                         line=dict(color='red', width=2)), row=3, col=1)

fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Attention_predicted'],
                         mode='lines', name='Attention Predicted',
                         line=dict(color='yellow', width=2)), row=3, col=1)

# Customize layout
fig.update_layout(height=800, title='Stock Data Visualization', xaxis_title='Date')

# Display the figure in Streamlit
st.plotly_chart(fig)
