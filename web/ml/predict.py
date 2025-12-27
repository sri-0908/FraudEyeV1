import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "xgb_fraud_model.pkl")

model = joblib.load(MODEL_PATH)

def predict_fraud(data):
    features = np.array([[
        data["amount"] / data["avg_user_amount"],
        data["txn_count_5min"],
        data["location_changed"],
        data["is_night"],
        data["new_device"],
        data["merchant_risk"]
    ]])

    prob = model.predict_proba(features)[0][1]

    if prob > 0.85:
        decision = "BLOCK"
    elif prob > 0.65:
        decision = "REVIEW"
    else:
        decision = "ALLOW"

    return {
        "fraud_probability": round(float(prob), 3),
        "decision": decision
    }

