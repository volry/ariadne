import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
from io import StringIO

# Set page configuration
st.set_page_config(layout="wide", page_title="Ariadne v.0.1.2", page_icon=":chart_with_upwards_trend:")

# local key
key_path = "/home/vova/Downloads/bionic-run-419111-4b5d62a9fac3.json"
storage_client = storage.Client.from_service_account_json(key_path)

# Use credentials from st.secrets
# credentials_info = st.secrets["gcp_service_account"]
# credentials = service_account.Credentials.from_service_account_info(credentials_info)
# storage_client = storage.Client(credentials=credentials)

@st.experimental_memo(ttl=3600)
def load_data_from_gcs(bucket_name, folder_prefix):
    # Your data loading logic
    # ...

# Function to dynamically generate the TradingView widget HTML based on selected stock ticker
def tradingview_html(ticker_symbol):
    return f'''
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_{ticker_symbol}"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
        "width": "100%",
        "height": 610,
        "symbol": "{ticker_symbol}",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "light",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_{ticker_symbol}"
      }}
      );
      </script>
    </div>
    <!-- TradingView Widget END -->
    '''

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar for login/logout and data refresh
with st.sidebar:
    if st.session_state.logged_in:
        if st.button('Refresh Data'):
            load_data_from_gcs.clear()
            st.experimental_rerun()

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()
    
    else:
        if st.button("Login"):
            # Simulated login logic
            st.session_state.logged_in = True
            st.experimental_rerun()

if st.session_state.logged_in:
    df = load_data_from_gcs("your-bucket-name", "your-folder-prefix")
    st.sidebar.header('Stock List')
    ticker = st.sidebar.selectbox('Choose a ticker:', df['stocks'].unique())

    # Dynamically generate and inject the TradingView widget HTML
    components.html(tradingview_html(ticker), height=610)
