# ml/predict.py
import pandas as pd
import joblib
import requests
from preprocess import load_data

def predict_from_api():
    """Fetch latest order via API (replace URL when API is ready)."""
    response = requests.get("http://localhost:8000/orders/latest")
    data = pd.DataFrame([response.json()])
    return data

def predict_from_local(sample):
    model = joblib.load("model/order_total_model.pkl")
    df = pd.get_dummies(sample, drop_first=True)
    # Ensure same feature alignment as training
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in df.columns:
            df[col] = 0
    df = df[model_features]
    prediction = model.predict(df)
    print("Predicted Order Total:", prediction[0])

if __name__ == "__main__":
    # Temporary: load local data and take one random sample
    df = load_data("../data")
    sample = df.sample(1).drop(columns=["total_amount"])
    predict_from_local(sample)