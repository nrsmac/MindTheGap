import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

DATE_TIME = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache() # This decorator makes the function "remember" its output, memoization
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data=load_data(10000)
hour = st.sidebar.slider('hour', 0,23, 10)
data = data[data[DATE_TIME].dt.hour == hour]

'## Geo data at %sh' % hour
st.map(data) # Make this not autocenter

if st.checkbox('Show raw data'):
    '## Raw data at %sh' % hour, data
