import matplotlib.pyplot as plt
import streamlit as st

def detect_anomalies(df):
    q1 = df["Value (kWh)"].quantile(0.25)
    q3 = df["Value (kWh)"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return df[(df["Value (kWh)"] < lower) | (df["Value (kWh)"] > upper)]

def plot_anomalies(df, anomalies):
    fig, ax = plt.subplots()
    ax.plot(df.index, df["Value (kWh)"], label="Energy Usage")
    ax.scatter(anomalies.index, anomalies["Value (kWh)"], color="red", label="Anomalies")
    ax.set_xlabel("Date")
    ax.set_ylabel("Energy (kWh)")
    ax.legend()
    st.pyplot(fig)
