import streamlit as st
import base64
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit import session_state as ss
from  google.cloud import storage
from io import StringIO
from io import BytesIO
from google.oauth2 import service_account
import google.auth
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(layout="wide", page_title="Ariadne v.0.1.3", page_icon=":chart_with_upwards_trend:")

# local key
key_path = "/home/vova/Downloads/bionic-run-419111-4b5d62a9fac3.json"
storage_client = storage.Client.from_service_account_json(key_path)

# Use credentials from st.secrets
# credentials_info = st.secrets["gcp_service_account"]
# credentials = service_account.Credentials.from_service_account_info(credentials_info)
# storage_client = storage.Client(credentials=credentials)

# Function to generate HTML for TradingView widget
def tradingview_widget(ticker):
    return f'''
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_{ticker}"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
        "width": "100%",
        "height": 610,
        "symbol": "{ticker}",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "light",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_{ticker}"
      }}
      );
      </script>
    </div>
    <!-- TradingView Widget END -->
    '''



#%%
# Function to convert dataframe to CSV and then encode it
def to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()

# Function to generate a download link
def get_download_link(df, filename='data.csv', text='Download CSV file'):
    csv = to_csv(df)
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


# Create a storage client

bucket_name = 'assets-monitoring-1'
folder_prefix = 'monitoring_runtime/'

# Access the bucket
bucket = storage_client.bucket(bucket_name)


#%%

#%%

# Function to check user credentials (simple placeholder, not secure for production use)
USER_CREDENTIALS = {
    "test1": "test1",
    "test2": "test2",
    "test3": "test3",
    # Add more users as needed
}

def check_credentials(username, password):
    return USER_CREDENTIALS.get(username) == password


def filter_recent_signals(df, days):
    lookback_date = pd.Timestamp.today() - pd.Timedelta(days=days)
    filtered_df = df.copy()
    # Filter the DataFrame for recent 'Enter_class' signals
    filtered_df = df[(df['Enter_class'] == 1) & (df['datetime'] > lookback_date)]
    # Format 'datetime' to show only the date part
    filtered_df['datetime'] = filtered_df['datetime'].dt.date
    # Reset the index without adding an index column in the new DataFrame
    filtered_df = filtered_df.reset_index(drop=True)
    return filtered_df

@st.cache_data(ttl=3600)
def load_data_from_gcs(bucket_name, folder_prefix):
   
    # List all blobs that start with the folder prefix
    blobs = list(bucket.list_blobs(prefix=folder_prefix))

    # Initialize an empty list to hold all DataFrames
    df_list = []

    # Iterate over the blobs (files) and load them as DataFrames
    for blob in blobs:
        # Make sure to process files (blobs ending with '.csv')
        if blob.name.endswith('.csv'):
            # Download the contents of the blob as a string
            data = blob.download_as_text()
            
            # Convert string to StringIO object and load into DataFrame
            df = pd.read_csv(StringIO(data))
            
            # Add a column with the name of the file
            file_name = blob.name.split('/')[-1].replace('.csv', '')
            df['stocks'] = file_name
            
            # Append the DataFrame to the list
            df_list.append(df)

#    Concatenate all the DataFrames in the list into one
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df['datetime'] = pd.to_datetime(combined_df['datetime'])
    
    return combined_df
    

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Check if 'data' is already loaded into session state
if 'data' not in st.session_state or 'filtered_df' not in st.session_state:
    # If not, load the data and cache it in the session state
    st.session_state['data'] = load_data_from_gcs(bucket_name, folder_prefix)
    st.session_state['filtered_df'] = filter_recent_signals(st.session_state['data'], 10)  # Initializing with a default lookback period of 10 days

# Sidebar for login/logout and data refresh
with st.sidebar:
    if st.session_state.logged_in:
        st.title("Data Refresh")
        if st.button('Refresh Data'):
            # Clear the cache and rerun the app to load fresh data
            load_data_from_gcs.clear()  # This will clear the memoized function's cache
            st.rerun()  # Rerun the app to reflect the changes

        st.title("Logout")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        # Sidebar widget to get the number of days for the filter
        days = st.sidebar.number_input('Enter the number of days to look back for Enter_class signals:', min_value=1, value=10)
        if st.sidebar.button('OK'):
            # Update the filtered data based on the new number of days
            st.session_state['filtered_df'] = filter_recent_signals(st.session_state['data'], days)
            st.rerun()  # Optionally rerun to refresh the data shown on the page

    else:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect username or password. Please try again.")

# Display login message if not logged in
if not ss.logged_in:
    st.info("Please login to view the dashboard.")

# Main app content (only shown if logged in)
if ss.logged_in:
    df = load_data_from_gcs(bucket_name, folder_prefix)

    st.header('Indicators')
    # Place indicator checkboxes below the main chart
    show_enter = st.checkbox('Show Enter Predicted', True)
    show_exit = st.checkbox('Show Exit Predicted', True)
    show_attention = st.checkbox('Show Attention Predicted', True)

    
    st.header('Recent Enter Signals')
    if 'filtered_df' in st.session_state and not st.session_state['filtered_df'].empty:
        st.dataframe(st.session_state['filtered_df'][['stocks', 'datetime']])
    else:
        st.write(f"No recent Enter_class signals found in the last {days} days.")
    


    st.sidebar.header('Stock List')
    ticker = st.sidebar.radio('Choose a ticker:', df['stocks'].unique())

    st.title('Stock Data Visualization')
    components.html(tradingview_widget(ticker), height=610)
    ticker_data = df[df['stocks'] == ticker]

    main_fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                             vertical_spacing=0.05, row_heights=[0.7, 0.3])

    main_fig.add_trace(go.Candlestick(x=ticker_data['datetime'],
                                      open=ticker_data['open'], high=ticker_data['high'],
                                      low=ticker_data['low'], close=ticker_data['close'],
                                      name='OHLC'), row=1, col=1)

    main_fig.add_trace(go.Bar(x=ticker_data['datetime'], y=ticker_data['volume'],
                              name='Volume', marker_color='blue'), row=2, col=1)

    main_fig.update_layout(height=600,
                            title='OHLC and Volume',
                            xaxis_title='Date',
                            hovermode='x',
                            xaxis_rangeslider_visible=False,
                            showlegend=False,
                            xaxis_type='category')

    

    main_fig.update_xaxes(type='category', row=2, col=1)

    if show_enter or show_exit or show_attention:
        indicator_fig = go.Figure()

        if show_enter:
            indicator_fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Enter_predicted'],
                                               mode='lines', name='Enter Predicted',
                                               line=dict(color='green', width=3)))

        if show_exit:
            indicator_fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Exit_predicted'],
                                               mode='lines', name='Exit Predicted',
                                               line=dict(color='red', width=3)))

        if show_attention:
            indicator_fig.add_trace(go.Scatter(x=ticker_data['datetime'], y=ticker_data['Attention_predicted'],
                                               mode='lines', name='Attention Predicted',
                                               line=dict(color='blue', width=3)))

        indicator_fig.update_layout(height=300, title='Indicators', hovermode='x',
                                    legend=dict(yanchor="top", y=-0.3, xanchor="center", x=0.5))

        st.plotly_chart(indicator_fig, use_container_width=True)

    st.plotly_chart(main_fig, use_container_width=True)
    # Button to download CSV
    st.sidebar.download_button(
        label="Download data as CSV",
        data=to_csv(df),
        file_name='combined_data.csv',
        mime='text/csv',
    )