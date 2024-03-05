#df = pd.read_excel("data/CIT_NN.xlsx", sheet_name='files')

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the layout to wide mode
st.set_page_config(layout="wide")

# Load your data
df = pd.read_excel("data/CIT_NN.xlsx", sheet_name='files')
df['datetime'] = pd.to_datetime(df['datetime'])

# Sidebar with the list of tickers
st.sidebar.header('Stock List')
ticker = st.sidebar.radio('Choose a ticker:', df['stocks'].unique())

# Main area
st.title('Stock Data Visualization')

# Filter the DataFrame for the selected ticker
ticker_data = df[df['stocks'] == ticker]


fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    vertical_spacing=0.02,  # You may need to adjust this to achieve the desired spacing
                    subplot_titles=('OHLC', 'Volume', 'Indicators'),
                    row_heights=[0.7, 0.2, 0.1])  # Adjusted heights: more space for OHLC, less for indicators

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

# Customize layout for OHLC and Volume
# Customize layout
fig.update_layout(
    height=1200,  # Increased height for the entire figure
    title='Stock Data Visualization',
    xaxis_title='Date',
    xaxis_rangeslider_visible=False
)


# Indicator checkboxes and chart
st.header('Indicators')
# Place checkboxes below the indicators chart
show_enter = st.checkbox('Show Enter Predicted', True)
show_exit = st.checkbox('Show Exit Predicted', True)
show_attention = st.checkbox('Show Attention Predicted', True)

# Only create and display the indicator chart if any checkbox is ticked
if show_enter or show_exit or show_attention:
    fig_indicators = go.Figure()

    if show_enter:
        fig_indicators.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Enter_predicted'],
                                            mode='lines', name='Enter Predicted',
                                            line=dict(color='green', width=2)))

    if show_exit:
        fig_indicators.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Exit_predicted'],
                                            mode='lines', name='Exit Predicted',
                                            line=dict(color='red', width=2)))

    if show_attention:
        fig_indicators.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Attention_predicted'],
                                            mode='lines', name='Attention Predicted',
                                            line=dict(color='yellow', width=2)))

    # Customize layout for the indicator chart only
    fig_indicators.update_layout(title='Indicators', xaxis_title='Date')
    # Display the indicator figure
    st.plotly_chart(fig_indicators, use_container_width=True)

