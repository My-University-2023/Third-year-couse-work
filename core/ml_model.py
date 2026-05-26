from joblib import load
from core.ml_features import extract_features


model = load("core/stego_model.pkl")


def predict_image(image_path):

    features = extract_features(image_path)

    prob = model.predict_proba([features])[0][1]

    if prob < 0.3:
        decision = "SAFE"
    elif prob < 0.7:
        decision = "SUSPICIOUS"
    else:
        decision = "HIGH RISK"

    return {
        "risk": round(prob * 100, 2),
        "decision": decision
    }