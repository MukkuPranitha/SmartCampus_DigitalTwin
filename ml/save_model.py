import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor


# Load dataset
df = pd.read_csv("../dataset/07_smart_campus_digital_twin.csv")


# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["DayOfWeek"] = df["Date"].dt.dayofweek

df = df.drop("Date", axis=1)


# Features and target
X = df.drop("Electricity_Consumption", axis=1)

# Building_ID is only an identifier
X = X.drop("Building_ID", axis=1)

y = df["Electricity_Consumption"]


# Encode Building_Type
X = pd.get_dummies(
    X,
    columns=["Building_Type"],
    drop_first=True
)


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Train the best model
model = GradientBoostingRegressor(
    random_state=42
)

model.fit(X_train, y_train)


# Save model
joblib.dump(model, "gradient_boosting_model.pkl")

# Save feature names
joblib.dump(X.columns.tolist(), "model_features.pkl")


print("Gradient Boosting model trained successfully!")
print("Model saved as gradient_boosting_model.pkl")
print("Feature list saved as model_features.pkl")