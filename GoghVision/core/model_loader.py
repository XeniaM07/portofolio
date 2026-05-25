import joblib

def load_binary_classifier(path="models/binary_classifier.pkl"):
    return joblib.load(path)

def load_location_classifier(path="models/location_classifier.pkl"):
    bundle = joblib.load(path)
    return bundle["model"], bundle["label_encoder"]