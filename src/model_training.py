from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def train_model(df):
    features = ["Temp_avg", "Hum_avg", "Wind_avg", "Press_avg"]
    X = df[features]
    y = df["Value (kWh)"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model
