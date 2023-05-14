import streamlit as st
import pandas as pd
import time
from datetime import datetime

#this will display the time, datetime, and timestamp on the localhost web
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
tiemstamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

#df variables will read the csv file that we have
df = pd.read_csv("attendance/attendance_" + date + ".csv")

#this will set the highlisht of the data we have
st.dataframe(df.style.highlight_max(axis = 0))