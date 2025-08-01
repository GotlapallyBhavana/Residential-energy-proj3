import pandas as pd
import streamlit as st

def load_data(energy_path):
    try:
        df = pd.read_csv(energy_path)

        # Auto-detect date column
        date_col = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        if not date_col:
            raise ValueError("❌ No datetime column found in energy file.")
        
        df[date_col[0]] = pd.to_datetime(df[date_col[0]])
        df.set_index(date_col[0], inplace=True)

        # Drop duplicate columns if any
        df = df.loc[:, ~df.columns.duplicated()]

        # 👉 Keep only numeric columns before resampling
        numeric_df = df.select_dtypes(include='number')

        # Resample and interpolate
        numeric_df = numeric_df.resample('D').mean().interpolate(method='time')

        return numeric_df

    except Exception as e:
        raise ValueError(f"❌ Error while processing file: {e}")

def plot_energy_usage(df):
    st.line_chart(df["Value (kWh)"])  # or change column name as needed
