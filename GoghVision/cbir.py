import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from db_access import (
    get_all_features_and_labels,
    get_all_paintings_metadata,
    get_all_metadata_full
)

def get_similar_paintings(query_features, top_n=5):
    features, _ = get_all_features_and_labels()
    metadata = get_all_paintings_metadata()

    feature_matrix = np.array(features)
    query_vector = np.array(query_features).reshape(1, -1)

    distances = cosine_distances(query_vector, feature_matrix)[0]
    closest_indices = np.argsort(distances)[:top_n]

    similar_paintings = []
    for idx in closest_indices:
        similar_paintings.append({
            "title": metadata[idx]["title"],
            "image_path": metadata[idx]["image_path"],
            "location": metadata[idx]["location"],
            "year": metadata[idx]["year"],
            "distance": float(distances[idx])
        })

    return similar_paintings


def get_similar_vangogh_paintings(query_features, top_n=5):
    from db_access import get_all_metadata_full

    features, labels = get_all_features_and_labels()
    metadata = get_all_metadata_full()

    filtered = [
        (f, m) for f, m, l in zip(features, metadata, labels)
        if l.lower() == "van_gogh"
    ]

    if not filtered:
        return []

    filtered_features, filtered_metadata = zip(*filtered)

    feature_matrix = np.array(filtered_features)
    query_vector = np.array(query_features).reshape(1, -1)

    distances = cosine_distances(query_vector, feature_matrix)[0]
    closest_indices = np.argsort(distances)[:top_n]

    results = []
    for idx in closest_indices:
        meta = filtered_metadata[idx]
        results.append({
            "title": meta["title"],
            "image_path": meta["image_path"],
            "location": meta["location"],
            "year": meta["year"],
            "dominant_colors_path": meta.get("dominant_colors_path", ""),
            "heatmap_path": meta.get("heatmap_path", ""),
            "classification_diagram_path": meta.get("classification_diagram_path", ""),
            "author": meta.get("author", "van_gogh"),
            "distance": float(distances[idx])
        })

    return results
