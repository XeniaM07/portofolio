import os
import glob
import uuid
import gc
from db_access import insert_painting
# feature_extractor.py (rămâne neschimbat din perspectiva init_db...)

from core.feature_extractor import extract_features
from core.visual_utils import generate_dominant_colors, generate_heatmap

DATASET_PATH = "dataset"
VISUALS_PATH = "visuals"
COLORS_PATH = os.path.join(VISUALS_PATH, "colors")
HEATMAPS_PATH = os.path.join(VISUALS_PATH, "heatmaps")

LOCATION_YEAR_MAP = {
    "Arles": "1888–1889",
    "Paris": "1886–1888",
    "Saint Remy": "1889–1890",
    "Auvers sur Oise": "1890",
    "Nuenen": "1883–1885",
    "Unknown location": None
}


def infer_year_and_location(image_path):
    parts = image_path.split(os.sep)
    if "vanGogh" in parts:
        location = parts[-2]
        return location, LOCATION_YEAR_MAP.get(location, None)
    return None, None


def get_author(image_path):
    return "van_gogh" if "vanGogh" in image_path else "other"


def get_title(image_path):
    return os.path.splitext(os.path.basename(image_path))[0]


def process_dataset():
    pattern = os.path.join(DATASET_PATH, "**", "*.jpg")
    image_paths = sorted(glob.glob(pattern, recursive=True))

    print(f"\nFound {len(image_paths)} images.\n")

    previous_folder = None

    for img_path in image_paths:
        current_folder = os.path.dirname(img_path)

        if current_folder != previous_folder:
            print(f"\nProcessing folder: {current_folder}")
            previous_folder = current_folder

        try:
            uid = uuid.uuid4().hex

            features = extract_features(img_path)
            dominant_color_path = generate_dominant_colors(img_path, COLORS_PATH)
            heatmap_path = generate_heatmap(img_path, HEATMAPS_PATH)

            author = get_author(img_path)
            location, year = infer_year_and_location(img_path)
            title = get_title(img_path) if author == "van_gogh" else f"nonvg_{uid}"

            record = {
                "title": title,
                "year": year,
                "location": location,
                "author": author,
                "image_path": img_path,
                "features": features.tolist(),
                "dominant_colors_path": dominant_color_path,
                "heatmap_path": heatmap_path,
                "classification_diagram_path": None
            }

            insert_painting(record)
            print(f"Saved: {title}")

            del features
            gc.collect()

        except Exception as e:
            print(f"Error: {img_path} → {e}")


if __name__ == "__main__":
    os.makedirs(COLORS_PATH, exist_ok=True)
    os.makedirs(HEATMAPS_PATH, exist_ok=True)
    process_dataset()
