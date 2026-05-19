import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load traffic data
data = pd.read_csv("traffic_data.csv")

# Features (input)
X = data[["vehicle_count"]]

# Target (output)
y = data["signal_timer"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy check
error = mean_absolute_error(y_test, predictions)

print("\nAI Traffic Prediction System")
print("-----------------------------")

print(f"Model Error: {round(error, 2)}")

# Predict future signal timing
future_traffic = int(input("\nEnter vehicle count: "))

predicted_signal = model.predict([[future_traffic]])

print(
    f"\nRecommended Signal Time: "
    f"{round(predicted_signal[0], 2)} seconds"
)