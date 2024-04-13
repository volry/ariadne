#%%
#%%
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit import session_state as ss
from  google.cloud import storage
from io import StringIO
from google.oauth2 import service_account
import google.auth
# Set page configuration
st.set_page_config(layout="wide", page_title="Ariadne v.0.1.0", page_icon=":chart_with_upwards_trend:")

# Use credentials from st.secrets if GOOGLE_APPLICATION_CREDENTIALS not set
credentials_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Use the credentials to create a storage client
storage_client = storage.Client(credentials=credentials)


#%%

# Create a storage client

bucket_name = 'assets-monitoring-1'
folder_prefix = 'monitoring_runtime_test/'

# Access the bucket
bucket = storage_client.bucket(bucket_name)




#%%
#combined_df.head()
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

#@st.cache_data
def load_data():
    
    blobs = list(bucket.list_blobs(prefix=folder_prefix))

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

# Sidebar for login/logout
with st.sidebar:

    st.title("Data Refresh")
    if st.button('Refresh Data'):
        # This will clear the cache and reload the data
        st.caching.clear_cache()
        st.experimental_rerun()

    if not st.session_state.logged_in:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully.")
            else:
                st.error("Incorrect username or password. Please try again.")
    else:
        if st.button("Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

# Display login message if not logged in
if not ss.logged_in:
    st.info("Please login to view the dashboard.")

# Main app content (only shown if logged in)
if ss.logged_in:
    df = load_data()
    st.header('Indicators')
    # Place indicator checkboxes below the main chart
    show_enter = st.checkbox('Show Enter Predicted', True)
    show_exit = st.checkbox('Show Exit Predicted', True)
    show_attention = st.checkbox('Show Attention Predicted', True)

    st.sidebar.header('Stock List')
    ticker = st.sidebar.radio('Choose a ticker:', df['stocks'].unique())

    st.title('Stock Data Visualization')

    ticker_data = df[df['stocks'] == ticker]

    main_fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                             vertical_spacing=0.05, row_heights=[0.7, 0.3])

    main_fig.add_trace(go.Candlestick(x=ticker_data['datetime'],
                                      open=ticker_data['open'], high=ticker_data['high'],
                                      low=ticker_data['low'], close=ticker_data['close'],
                                      name='OHLC'), row=1, col=1)

    main_fig.add_trace(go.Bar(x=ticker_data['datetime'], y=ticker_data['volume'],
                              name='Volume', marker_color='blue'), row=2, col=1)

    main_fig.update_layout(height=600, title='OHLC and Volume', xaxis_title='Date',
                           hovermode='x', xaxis_rangeslider_visible=False, showlegend=False)

    st.plotly_chart(main_fig, use_container_width=True)

  

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

        indicator_fig.update_layout(height=300, title='Indicators', hovermode='x',
                                    legend=dict(yanchor="top", y=-0.3, xanchor="center", x=0.5))

        st.plotly_chart(indicator_fig, use_container_width=True)
