#%%
import pandas as pd
import streamlit as st

#%%
st.title("Stock Data Visualization")
df = pd.read_excel(r"data/CIT_NN.xlsx", sheet_name='files')
# %%
##df.info()
st.dataframe(df)
