#df = pd.read_excel("data/CIT_NN.xlsx", sheet_name='files')
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration and layout to wide mode
st.set_page_config(layout="wide")

# Load your data
df = pd.read_excel("data/CIT_NN.xlsx", sheet_name='files')
df['datetime'] = pd.to_datetime(df['datetime'])

# Sidebar for stock ticker selection
st.sidebar.header('Stock List')
ticker = st.sidebar.radio('Choose a ticker:', df['stocks'].unique())

# Filtering data
ticker_data = df[df['stocks'] == ticker]

# Main area
st.title('Stock Data Visualization')

# Create a subplot for OHLC and volume charts
main_fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                         vertical_spacing=0.05,  # Adjust spacing between the charts
                         row_heights=[0.7, 0.3])  # Adjust the relative height of the charts

# OHLC chart
main_fig.add_trace(go.Candlestick(x=ticker_data['datetime'],
                                  open=ticker_data['open'], high=ticker_data['high'],
                                  low=ticker_data['low'], close=ticker_data['close'],
                                  name='OHLC'), row=1, col=1)

# Volume chart
main_fig.add_trace(go.Bar(x=ticker_data['datetime'], y=ticker_data['volume'],
                          name='Volume', marker_color='blue'), row=2, col=1)

# Customizing the layout of the main figure
main_fig.update_layout(height=600,  # You can adjust the height as needed
                       title='OHLC and Volume', xaxis_title='Date',
                       xaxis_rangeslider_visible=False, showlegend=False)

# Display the main figure with OHLC and Volume
st.plotly_chart(main_fig, use_container_width=True)

# Indicators section with checkboxes
st.header('Indicators')
show_enter = st.checkbox('Show Enter Predicted', True)
show_exit = st.checkbox('Show Exit Predicted', True)
show_attention = st.checkbox('Show Attention Predicted', True)

# Create a separate figure for indicators if any checkbox is selected
if show_enter or show_exit or show_attention:
    indicator_fig = go.Figure()

    if show_enter:
        indicator_fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Enter_predicted'],
                                           mode='lines', name='Enter Predicted',
                                           line=dict(color='green', width=2)))

    if show_exit:
        indicator_fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Exit_predicted'],
                                           mode='lines', name='Exit Predicted',
                                           line=dict(color='red', width=2)))

    if show_attention:
        indicator_fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Attention_predicted'],
                                           mode='lines', name='Attention Predicted',
                                           line=dict(color='yellow', width=2)))

    # Customize layout for the indicator chart
    indicator_fig.update_layout(height=300, title='Indicators', xaxis_title='Date')

    # Display the indicator figure
    st.plotly_chart(indicator_fig, use_container_width=True)
