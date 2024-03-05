import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the layout to wide mode
st.set_page_config(layout="wide")

# Load your data
# Replace with your actual file path and ensure the CSV has 'datetime', 'open', 'high', 'low', 'close', 'volume'

df = pd.read_excel("data/CIT_NN.xlsx", sheet_name='files')
df['datetime'] = pd.to_datetime(df['datetime'])

# Use the sidebar for a list-like selection of tickers
st.sidebar.header('Stock List')
selected_ticker = st.sidebar.radio('Choose a ticker:', df['stocks'].unique())

# Filter the DataFrame for the selected ticker
ticker_data = df[df['stocks'] == selected_ticker]

# Create the subplots
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=('OHLC', 'Volume', 'Indicators'))

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
                     name='Volume',
                     marker_color='blue'), row=2, col=1)

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
fig.update_layout(height=1000,
                  title='Stock Data Visualization',
                  xaxis_title='Date',
                  xaxis_rangeslider_visible=False)

# Display the figure in Streamlit, using the full width of the container
st.plotly_chart(fig, use_container_width=True)
