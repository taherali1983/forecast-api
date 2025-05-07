import requests
import streamlit as st
import matplotlib.pyplot as plt

# API URL for the forecast (Replace with your actual API endpoint)
url = "https://forecast-api-production-1303.up.railway.app/forecast"

# Fetch the forecast data
try:
    response = requests.get(url)
    # Check if the response is valid and contains JSON data
    response.raise_for_status()  # Will raise an exception for 4xx or 5xx HTTP errors
    data = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data from API: {e}")
    data = None
except requests.exceptions.JSONDecodeError:
    st.error("Error decoding the JSON response from the API. Please check the API.")
    data = None

if data is not None:
    # Continue with processing the data and creating your plots
    st.write("Forecast data:", data)
    # Create your plot here
    plt.plot(data['forecast'])
    plt.show()
else:
    st.warning("No data to display.")
