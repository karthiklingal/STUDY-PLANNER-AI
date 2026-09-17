"""
classifier.py
-------------
Predicts pass/fail risk from student features:
attendance %, average study hours/day, past marks %.

Uses Logistic Regression as the primary model (interpretable,
fast, good baseline for a small tabular dataset) with a
Decision Tree trained alongside for comparison, as required by
the project's "model selection rationale" documentation.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

FEATURES = ["attendance_pct", "avg_study_hours_per_day", "past_marks_pct"]
TARGET = "result"


def load_data(path):
    df = pd.read_csv(path)
    df["label"] = (df[TARGET] == "Pass").astype(int)
    return df


def train_model(data_path, model_type="logistic", test_size=0.25, random_state=42):
    df = load_data(data_path)
    X = df[FEATURES]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    if model_type == "logistic":
        model = LogisticRegression()
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)
    else:  # decision_tree
        model = DecisionTreeClassifier(max_depth=4, random_state=random_state)
        model.fit(X_train, y_train)  # trees don't need scaling
        preds = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds, zero_division=0),
        "recall": recall_score(y_test, preds, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
    }

    return {
        "model": model,
        "scaler": scaler if model_type == "logistic" else None,
        "model_type": model_type,
        "metrics": metrics,
    }


def predict_risk(student_features, trained):
    """
    student_features: dict with keys matching FEATURES
    trained: dict returned by train_model()
    Returns: {"prediction": "Pass"/"Fail", "risk": "low"/"high"}
    """
    X = pd.DataFrame([student_features])[FEATURES]
    model = trained["model"]
    if trained["model_type"] == "logistic":
        X = trained["scaler"].transform(X)
    pred = model.predict(X)[0]
    label = "Pass" if pred == 1 else "Fail"
    risk = "low" if pred == 1 else "high"
    return {"prediction": label, "risk": risk}


if __name__ == "__main__":
    import os
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_students.csv")

    for model_type in ["logistic", "decision_tree"]:
        result = train_model(data_path, model_type=model_type)
        print(f"\n--- {model_type} ---")
        print("Accuracy: ", round(result["metrics"]["accuracy"], 3))
        print("Precision:", round(result["metrics"]["precision"], 3))
        print("Recall:   ", round(result["metrics"]["recall"], 3))
        print("Confusion Matrix:", result["metrics"]["confusion_matrix"])

    # Example prediction using the logistic model
    trained = train_model(data_path, model_type="logistic")
    sample = {"attendance_pct": 55, "avg_study_hours_per_day": 0.8, "past_marks_pct": 40}
    print("\nSample student risk prediction:", predict_risk(sample, trained))
