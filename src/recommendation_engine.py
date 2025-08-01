def generate_recommendations(df, anomalies):
    tips = []
    if not anomalies.empty:
        tips.append("⚠️ High variation in energy use detected. Check for leaks or faulty devices.")
    if "Hum_avg" in df.columns and df["Hum_avg"].mean() > 80:
        tips.append("💧 High humidity. Consider dehumidifiers.")
    if "Temp_avg" in df.columns and df["Temp_avg"].mean() > 85:
        tips.append("🌡️ High temperature. Use smart cooling strategies.")
    if not tips:
        tips.append("✅ Energy usage is stable. Keep up the good work!")
    return tips
