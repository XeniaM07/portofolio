import os
import json
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


INPUT_JSON = os.path.join("output_json", "van_gogh_location_features.json")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "location_classifier.pkl")


def train_location_classifier():
    print("Loading features from JSON...")
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    x = [item["features"] for item in data]
    y = [item["locatie"] for item in data]

    x = np.array(x)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    print(f"Loaded {len(x)} samples from {len(set(y))} locations.")

    x_train, x_test, y_train, y_test = train_test_split(
        x, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    clf = SVC(kernel="linear", probability=True, random_state=42)
    clf.fit(x_train, y_train)
    print("Location classifier trained.")

    evaluate_location_classifier(clf, x_test, y_test, le)
    save_location_classifier(clf, le)


def evaluate_location_classifier(model, x_test, y_test, label_encoder):
    y_pred = model.predict(x_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"\nAccuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges',
                xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix - Location Classifier")
    plt.tight_layout()

    os.makedirs(MODEL_DIR, exist_ok=True)
    plt.savefig(os.path.join(MODEL_DIR, "confusion_location_classifier.png"))
    plt.close()


def save_location_classifier(model, label_encoder):
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({
        "model": model,
        "label_encoder": label_encoder
    }, MODEL_PATH)
    print(f"Model + encoder saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_location_classifier()
