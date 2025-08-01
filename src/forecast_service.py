import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_energy(df):
    series = df["Value (kWh)"]
    model = ExponentialSmoothing(series, trend="add", seasonal=None)
    fitted = model.fit()
    forecast = fitted.forecast(7)
    forecast_df = pd.DataFrame({"Forecast": forecast})
    return forecast_df

def plot_forecast(df, forecast_df):
    fig, ax = plt.subplots()
    df["Value (kWh)"].plot(ax=ax, label="Historical")
    forecast_df["Forecast"].plot(ax=ax, style="--", label="Forecast", color="orange")
    ax.legend()
    st.pyplot(fig)
