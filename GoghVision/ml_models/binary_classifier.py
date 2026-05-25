import os
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from db_access import get_all_features_and_labels

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "binary_classifier.pkl")

def train_binary_classifier():
    print("Loading data...")
    features, labels = get_all_features_and_labels()

    if not features:
        print("No features found in database.")
        return

    x = np.array(features)
    y = np.array([1 if label == "van_gogh" else 0 for label in labels])

    print(f"Loaded {len(x)} samples (van_gogh={np.sum(y == 1)}, other={np.sum(y == 0)})")

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = SVC(kernel="linear", probability=True, random_state=42)
    clf.fit(x_train, y_train)
    print("Model trained")

    evaluate_binary_classifier(clf, x_test, y_test)
    save_binary_classifier(clf)

def evaluate_binary_classifier(model, x_test, y_test):
    y_pred = model.predict(x_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"\nAccuracy: {acc:.4f}")
    print(f"\nClassification report:")
    print(classification_report(y_test, y_pred, target_names=["other", "van_gogh"]))

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize = (5,4))
    sns.heatmap(cm, annot = True, cmap = "Blues",
                xticklabels = ["other", "van_gogh"], yticklabels = ["other", "van_gogh"])
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion matrix - Binary Classifier")
    plt.tight_layout()

    os.makedirs(MODEL_DIR, exist_ok = True)
    plt.savefig(os.path.join(MODEL_DIR, "confusion_binary_classifier.png"))
    plt.close()

def save_binary_classifier(model):
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

# if __name__ == "__main__":
#     train_binary_classifier()