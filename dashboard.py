import streamlit as st
import requests
import matplotlib.pyplot as plt

# Call your FastAPI endpoint
url = "http://127.0.0.1:8000/forecast"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    forecast = data['forecast']
    actual = data['actual']
    rmse = data['rmse']

    st.title("???? Load Forecast Dashboard (BiLSTM)")
    st.markdown(f"**RMSE**: `{rmse}` MW")

    st.line_chart({
        "Forecast": forecast,
        "Actual": actual
    })

else:
    st.error("Failed to load data from API")
import streamlit as st
import requests
import pandas as pd

# Call the API
url = "http://127.0.0.1:8000/forecast"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    forecast = data['forecast']
    actual = data['actual']
    rmse = data['rmse']

    st.title("???? Load Forecast Dashboard (BiLSTM)")
    st.markdown(f"**RMSE**: `{rmse:.2f}` MW")

    # Combine into DataFrame
    df = pd.DataFrame({
        "Time": list(range(len(actual))),
        "Actual": actual,
        "Forecast": forecast
    })

    # Time range slider
    time_range = st.slider("Select time range", 0, len(df)-1, (0, len(df)-1))
    df_range = df.iloc[time_range[0]:time_range[1]+1]

    st.line_chart(df_range.set_index("Time"))

else:
    st.error("Failed to load forecast from API.")
