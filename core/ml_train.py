import os
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import classification_report

from joblib import dump

from core.ml_features import extract_features


def load_dataset(normal_dir, stego_dir):

    X = []
    y = []

    for f in os.listdir(normal_dir):

        path = os.path.join(normal_dir, f)

        try:

            features = extract_features(path)

            X.append(features)
            y.append(0)

        except Exception as e:

            print("NORMAL ERROR:", path)
            print(e)

    for f in os.listdir(stego_dir):

        path = os.path.join(stego_dir, f)

        try:

            features = extract_features(path)

            X.append(features)
            y.append(1)

        except Exception as e:

            print("STEGO ERROR:", path)
            print(e)

    return np.array(X), np.array(y)


def train_model():
    print("TRAIN STARTED")

    X, y = load_dataset(
        "dataset/normal",
        "dataset/stego"
    )

    if len(X) == 0:
        raise ValueError("DATASET EMPTY")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(n_estimators=100)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    report_dict = classification_report(
        y_test,
        predictions,
        output_dict=True
    )

    accuracy = accuracy_score(y_test, predictions)

    dump(model, "core/stego_model.pkl")

    return {
        "accuracy": accuracy,
        "metrics": {
            "0": report_dict.get("0", {...}),
            "1": report_dict.get("1", {...})
        }
    }