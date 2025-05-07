import streamlit as st
import matplotlib.pyplot as plt
import requests
import numpy as np
import pandas as pd

st.set_page_config(page_title="BiLSTM Load Forecast", layout="wide")
st.title("⚡ Load Forecast Dashboard (BiLSTM)")

# Get API response
url = "https://forecast-api-production-1303.up.railway.app/forecast"
response = requests.get(url)
data = response.json()
actual = np.array(data["actual"])
forecast = np.array(data["forecast"])
total_length = len(actual)

# Tabs
tab1, tab2 = st.tabs(["📈 Forecast View", "📊 Daily Averages"])

with tab1:
    st.subheader("Forecast Visualization")

    # Horizon selection
    horizon = st.selectbox("📆 Forecast horizon", options=[24, 48, 72, total_length], index=0)
    horizon = min(horizon, total_length)

    # Time slider
    start, end = st.slider("⏱ Time Window", 0, total_length - 1, (0, horizon - 1), 1)

    # Chart toggle
    chart_type = st.radio("📊 Chart Type", ["Line", "Bar"], horizontal=True)

    # RMSE
    rmse = np.sqrt(np.mean((forecast[start:end+1] - actual[start:end+1]) ** 2))
    st.markdown(f"**RMSE:** <span style='color:green'>{rmse:.2f}</span> MW", unsafe_allow_html=True)

    # Plot
    fig, ax = plt.subplots()
    x = np.arange(start, end + 1)
    if chart_type == "Line":
        ax.plot(x, actual[start:end+1], label="Actual", linewidth=2)
        ax.plot(x, forecast[start:end+1], label="Forecast", linestyle="--")
    else:
        ax.bar(x - 0.2, actual[start:end+1], width=0.4, label="Actual")
        ax.bar(x + 0.2, forecast[start:end+1], width=0.4, label="Forecast")

    ax.set_xlabel("Time Step")
    ax.set_ylabel("Load (MW)")
    ax.set_title("Forecast vs Actual Load")
    ax.legend()
    st.pyplot(fig)

    # CSV Export
    csv_data = pd.DataFrame({
        "TimeStep": x,
        "Actual (MW)": actual[start:end+1],
        "Forecast (MW)": forecast[start:end+1]
    })
    st.download_button("📥 Download Forecast CSV", csv_data.to_csv(index=False), "forecast.csv", "text/csv")

with tab2:
    st.subheader("Daily Mean Load (Forecast vs Actual)")
    
    days = total_length // 24
    daily_actual = actual[:days*24].reshape(-1, 24).mean(axis=1)
    daily_forecast = forecast[:days*24].reshape(-1, 24).mean(axis=1)
    
    fig2, ax2 = plt.subplots()
    ax2.plot(daily_actual, label="Actual Daily Avg", linewidth=2)
    ax2.plot(daily_forecast, label="Forecast Daily Avg", linestyle="--")
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Average Load (MW)")
    ax2.set_title("Daily Average Load")
    ax2.legend()
    st.pyplot(fig2)
