import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load your data
df = pd.read_excel("data/CIT_NN.xlsx", sheet_name='files')
df['datetime'] = pd.to_datetime(df['datetime'])

ticker = st.selectbox('Select a stock ticker:', df['stocks'].unique())
# Filter the DataFrame for the selected ticker
ticker_data = df[df['stocks'] == ticker]



# Create the figure with subplots
fig = go.Figure()

# Add traces for Enter, Exit, and Attention Predictions
fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['enter_predicted'],
                         mode='markers', name='Enter Predicted',
                         marker=dict(color='green', size=10)))

fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['exit_predicted'],
                         mode='markers', name='Exit Predicted',
                         marker=dict(color='red', size=10)))

fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['attention_predicted'],
                         mode='markers', name='Attention Predicted',
                         marker=dict(color='yellow', size=10)))

# Customize the layout
fig.update_layout(title='Predictions Chart',
                  xaxis_title='Date',
                  yaxis_title='Prediction Value',
                  yaxis=dict(range=[0, 1]))  # Assuming binary (0 or 1) predictions

# Display the figure in Streamlit
st.plotly_chart(fig)