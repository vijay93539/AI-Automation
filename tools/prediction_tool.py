import joblib
import pandas as pd

model = joblib.load("model/predictive_maintenance_model.pkl")

def predict_failure(Type, air_temp, process_temp, rpm, torque, tool_wear):

    sample = pd.DataFrame([{
        "Type": Type,
        "Air temperature [K]": air_temp,
        "Process temperature [K]": process_temp,
        "Rotational speed [rpm]": rpm,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear
    }])

    prediction = model.predict(sample)[0]
    probability = model.predict_proba(sample)[0][1]

    return {
        "failure_prediction": int(prediction),
        "failure_probability": float(probability)
    }