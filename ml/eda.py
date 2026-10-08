import pandas as pd

df = pd.read_csv("../dataset/07_smart_campus_digital_twin.csv")

print("Dataset loaded successfully!")
print()

print("Shape of dataset:")
print(df.shape)

print()

print("Columns:")
print(df.columns.tolist())

print()

print("First 5 rows:")
print(df.head())

print()

print("Data types:")
print(df.dtypes)

print()

print("Missing values:")
print(df.isnull().sum())

print()

print("Duplicate rows:")
print(df.duplicated().sum())

print()

print("Basic statistics:")
print(df.describe())
import matplotlib.pyplot as plt

plt.scatter(df["Occupancy"], df["Electricity_Consumption"])

plt.xlabel("Occupancy")
plt.ylabel("Electricity Consumption")
plt.title("Occupancy vs Electricity Consumption")

plt.show()
plt.scatter(df["Temperature"], df["Electricity_Consumption"])

plt.xlabel("Temperature")
plt.ylabel("Electricity Consumption")
plt.title("Temperature vs Electricity Consumption")

plt.show()
# 2. Temperature vs Electricity Consumption
plt.figure(figsize=(8, 5))

plt.scatter(
    df["Temperature"],
    df["Electricity_Consumption"]
)

plt.xlabel("Temperature")
plt.ylabel("Electricity Consumption")
plt.title("Temperature vs Electricity Consumption")

plt.show()
# 3. AC Usage vs Electricity Consumption
plt.figure(figsize=(8, 5))

plt.scatter(
    df["AC_Usage"],
    df["Electricity_Consumption"]
)

plt.xlabel("AC Usage")
plt.ylabel("Electricity Consumption")
plt.title("AC Usage vs Electricity Consumption")

plt.show()
# 4. Correlation Matrix
plt.figure(figsize=(10, 8))

correlation = df.select_dtypes(include="number").corr()

plt.imshow(correlation, cmap="coolwarm")
plt.colorbar()

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=90
)

plt.yticks(
    range(len(correlation.columns)),
    correlation.columns
)

plt.title("Correlation Matrix")
plt.tight_layout()

plt.show()