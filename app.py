import streamlit as st
import pandas as pd
from src import data_processing, anomaly_detection, recommendation_engine, forecast_service
from transformers import pipeline

# ---------- Setup ----------
st.set_page_config(page_title="Residential Energy Analytics", layout="wide")
st.title("🏡 Residential Energy Analytics Platform")

# ---------- Sidebar Navigation ----------
page = st.sidebar.radio("🔍 Select a Page", [
    "Energy Dashboard", "Chat with LLM"
])

# ---------- Page 1: Energy Dashboard ----------
if page == "Energy Dashboard":
    energy_file = st.sidebar.file_uploader("📂 Upload Energy Data CSV", type=["csv"])

    if energy_file:
        df_energy_preview = pd.read_csv(energy_file, nrows=5)
        st.sidebar.write("📁 Columns:", df_energy_preview.columns.tolist())
        energy_file.seek(0)

        try:
            energy_df = data_processing.load_data(energy_file)

            st.sidebar.markdown("---")
            st.sidebar.write("📊 Energy Summary")
            st.sidebar.write(energy_df.describe())

            st.subheader("📈 Energy Consumption Trend")
            data_processing.plot_energy_usage(energy_df)

            st.subheader("🔍 Anomaly Detection")
            anomalies = anomaly_detection.detect_anomalies(energy_df)
            anomaly_detection.plot_anomalies(energy_df, anomalies)

            st.subheader("📉 Forecasting")
            forecast_df = forecast_service.forecast_energy(energy_df)
            forecast_service.plot_forecast(energy_df, forecast_df)

            st.subheader("💡 Recommendations")
            tips = recommendation_engine.generate_recommendations(energy_df, anomalies)
            for tip in tips:
                st.success(tip)

        except Exception as e:
            st.error(f"❌ Error while processing file: {e}")
    else:
        st.info("📌 Please upload an Energy CSV file to begin.")

# ---------- Page 2: Chat with LLM (Offline GPT-2) ----------
elif page == "Chat with LLM":
    st.header("💬 Chat with Energy Assistant (Offline)")

    @st.cache_resource
    def load_local_gpt2():
        return pipeline("text-generation", model="gpt2")

    generator = load_local_gpt2()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask me anything about energy usage, forecasting, savings tips...")

    if prompt:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.spinner("Generating response..."):
            raw_output = generator(
                prompt,
                max_length=80,  # limit to concise response
                min_length=40,
                temperature=0.8,
                top_p=0.9,
                do_sample=True,
                pad_token_id=50256
            )[0]['generated_text']

        # Remove the prompt from start of generated text
        response = raw_output.replace(prompt, "").strip()

        # Cleanup: Remove repeated or unrelated text if present
        response = response.split("\n")[0].strip()  # Take first line

        # Add punctuation if missing
        if not response.endswith(('.', '!', '?')):
            response += "."

        # Show assistant reply
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
