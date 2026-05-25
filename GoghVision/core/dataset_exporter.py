import os
import sqlite3
import json
from typing import List, Dict

def fetch_paintings_by_author_with_location(db_path: str, author: str) -> List[Dict]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT title, features, location
    FROM paintings
    where author = ? AND location IS NOT NULL
    """
    cursor.execute(query, (author,))
    rows = cursor.fetchall()
    conn.close()

    dataset = []
    for title, features_json, location in rows:
        try:
            features = json.loads(features_json)
            dataset.append({
                "title": title,
                "features": features,
                "locatie": location,
                "artist": author
            })
        except json.JSONDecodeError:
            continue

    return dataset

def export_dataset_to_json(dataset: List[Dict], output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with  open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"Saved {len(dataset)} samples to {output_path}")

def generate_location_dataset(
        db_path: str = "db/paintings.db",
        author: str = "van_gogh",
        output_path: str = "output_json\van_gogh_location_features.json"
) -> None:
    dataset = fetch_paintings_by_author_with_location(db_path, author)
    export_dataset_to_json(dataset, output_path)

# if __name__ == "__main__":
#     generate_location_dataset()