import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Load dataset
df = pd.read_csv("../dataset/07_smart_campus_digital_twin.csv")

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Extract date features
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["DayOfWeek"] = df["Date"].dt.dayofweek

# Remove original Date
df = df.drop("Date", axis=1)

# Separate features and target
X = df.drop("Electricity_Consumption", axis=1)
y = df["Electricity_Consumption"]

# Identify categorical columns
# Building_ID is only an identifier, so we don't use it for prediction
X = X.drop("Building_ID", axis=1)

categorical_columns = ["Building_Type"]

# One-hot encode categorical columns
X = pd.get_dummies(
    X,
    columns=categorical_columns,
    drop_first=True
)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Preprocessing completed successfully!")

print()
print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)

print()
print("All features are now numeric:")
print(X.dtypes)

print()
print("Target:")
print("Electricity_Consumption")