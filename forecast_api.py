from fastapi import FastAPI
from scipy.io import loadmat
from typing import List
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="BiLSTM Load Forecast API")

# Load MATLAB forecast
data = loadmat('bilstm_forecast_output.mat')
forecast = data['YPred'].flatten().tolist()
true_values = data['YTrue'].flatten().tolist()

class ForecastResponse(BaseModel):
    forecast: List[float]
    actual: List[float]
    rmse: float

@app.get("/forecast", response_model=ForecastResponse)
def get_forecast():
    rmse = np.sqrt(np.mean((np.array(forecast) - np.array(true_values))**2))
    return ForecastResponse(forecast=forecast, actual=true_values, rmse=round(rmse, 2))