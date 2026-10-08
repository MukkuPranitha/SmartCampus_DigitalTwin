from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib


app = FastAPI(title="Smart Campus Digital Twin API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://smartcampusdigitaltwin-frontend.vercel.app"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load trained model
model = joblib.load("../ml/gradient_boosting_model.pkl")
model_features = joblib.load("../ml/model_features.pkl")


# Input data structure
class CampusData(BaseModel):
    Building_Type: str
    Hour: int
    Occupancy: int
    Temperature: float
    Humidity: float
    Lighting_Usage: float
    AC_Usage: float
    Computer_Usage: float
    Water_Consumption: float
    Waste_Generated: float
    Year: int
    Month: int
    Day: int
    DayOfWeek: int


@app.get("/")
def home():
    return {
        "message": "Smart Campus Digital Twin API is running!"
    }


@app.post("/predict")
def predict(data: CampusData):

    # Convert input into DataFrame
    input_data = pd.DataFrame([data.model_dump()])

    # Encode Building_Type
    input_data = pd.get_dummies(
        input_data,
        columns=["Building_Type"],
        drop_first=True
    )

    # Make sure input has exactly the same features as training
    input_data = input_data.reindex(
        columns=model_features,
        fill_value=0
    )

    # Prediction
    prediction = model.predict(input_data)[0]

    return {
        "predicted_electricity": round(float(prediction), 2)
    }
@app.get("/trend")
def trend():

    df = pd.read_csv("../dataset/07_smart_campus_digital_twin.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    trend_data = (
        df.groupby("Date")["Electricity_Consumption"]
        .mean()
        .reset_index()
    )

    return {
        "dates": trend_data["Date"].dt.strftime("%Y-%m-%d").tolist(),
        "electricity": trend_data["Electricity_Consumption"]
        .round(2)
        .tolist()
    }