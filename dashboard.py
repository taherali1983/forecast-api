import requests
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="BiLSTM Load Forecast", layout="wide")
st.title("⚡ Load Forecast Dashboard (BiLSTM)")

# Fetch the forecast data
url = "https://forecast-api-production-1303.up.railway.app/forecast"

try:
    response = requests.get(url)
    response.raise_for_status()  # Check if the response is valid
    data = response.json()  # Parse the JSON response

    # Extract forecast, actual data and RMSE
    forecast = np.array(data['forecast'])
    actual = np.array(data['actual'])
    rmse = data['rmse']

except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data from API: {e}")
    data = None
except requests.exceptions.JSONDecodeError:
    st.error("Error decoding the JSON response from the API. Please check the API.")
    data = None

if data is not None:
    # Display RMSE
    st.markdown(f"**RMSE:** <span style='color:green'>{rmse:.2f}</span> MW", unsafe_allow_html=True)

    # Time slider to select forecast horizon
    horizon = st.selectbox("📆 Forecast horizon", options=[24, 48, 72, len(forecast)], index=0)
    horizon = min(horizon, len(forecast))

    # Time window selection (slider for specific time steps)
    start, end = st.slider(
        "⏱ Select Time Window",
        min_value=0,
        max_value=len(forecast) - 1,
        value=(0, horizon - 1),
        step=1
    )

    # Plotting the data
    chart_type = st.radio("📊 Choose chart type", ["Line", "Bar"], horizontal=True)

    fig, ax = plt.subplots()
    x = np.arange(start, end + 1)

    if chart_type == "Line":
        ax.plot(x, actual[start:end + 1], label="Actual", linewidth=2)
        ax.plot(x, forecast[start:end + 1], label="Forecast", linestyle="--")
    else:
        ax.bar(x - 0.2, actual[start:end + 1], width=0.4, label="Actual")
        ax.bar(x + 0.2, forecast[start:end + 1], width=0.4, label="Forecast")

    ax.set_xlabel("Time Step")
    ax.set_ylabel("Load (MW)")
    ax.set_title("Forecast vs Actual Load")
    ax.legend()
    st.pyplot(fig)

    # CSV Export Button
    import pandas as pd
    csv_data = pd.DataFrame({
        "TimeStep": x,
        "Actual (MW)": actual[start:end + 1],
        "Forecast (MW)": forecast[start:end + 1]
    })
    st.download_button("📥 Download Forecast CSV", csv_data.to_csv(index=False), "forecast.csv", "text/csv")
else:
    st.warning("No data to display.")
