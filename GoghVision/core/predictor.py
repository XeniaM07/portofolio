from core.model_loader import load_binary_classifier, load_location_classifier
from core.visual_generator import generate_visuals
from core.feature_extractor import extract_features
from core.visual_utils import generate_dominant_colors, generate_heatmap
from utils.helpers import LOCATION_YEAR_MAP
from cbir import get_similar_paintings

def analyze_image(image_path):
    print(f"Predicting for: {image_path}")
    features = extract_features(image_path)
    features_arr = [features]

    binary_model = load_binary_classifier()
    is_vg_pred = binary_model.predict(features_arr)[0]
    binary_prob = binary_model.predict_proba(features_arr)[0]
    is_van_gogh = is_vg_pred == 1

    location = year = None
    if is_van_gogh:
        location_model, label_encoder = load_location_classifier()
        pred = location_model.predict(features_arr)[0]
        location = label_encoder.inverse_transform(pred.reshape(1))[0]
        year = LOCATION_YEAR_MAP[location]

    uid, visual_paths = generate_visuals(image_path, binary_prob)
    similar_paintings = get_similar_paintings(features.tolist(), top_n=5)

    return {
        "id": uid,
        "features": features.tolist(),
        "is_van_gogh": is_van_gogh,
        "location": location,
        "year": year,
        "binary_prob": binary_prob,
        "similar_paintings": similar_paintings,
        "image_path": image_path,
        "dominant_colors_path": visual_paths["dominant_colors"],
        "heatmap_path": visual_paths["heatmap"],
        "classification_diagram_path": visual_paths["diagram"]
    }
