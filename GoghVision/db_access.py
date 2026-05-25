import sqlite3
import json
import os

DB_PATH = os.path.join("db", "paintings.db")

def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS paintings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        year TEXT,
        location TEXT,
        author TEXT,
        image_path TEXT,
        features TEXT,
        dominant_colors_path TEXT,
        heatmap_path TEXT,
        classification_diagram_path TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_painting(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO paintings (
        title,
        year,
        location,
        author,
        image_path,
        features,
        dominant_colors_path,
        heatmap_path,
        classification_diagram_path
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["year"],
        data["location"],
        data["author"],
        data["image_path"],
        json.dumps(data["features"]),
        data["dominant_colors_path"],
        data["heatmap_path"],
        data["classification_diagram_path"]
    ))

    conn.commit()
    conn.close()

def search_by_keyword(keyword):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT * FROM paintings
    WHERE LOWER(title) LIKE '%' || LOWER(?) || '%'
    """
    cursor.execute(query, (keyword,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_features_and_labels():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT features, author FROM paintings")
    rows = cursor.fetchall()
    conn.close()

    features = []
    labels = []
    for f_json, label in rows:
        try:
            vector = json.loads(f_json)
            features.append(vector)
            labels.append(label)
        except json.JSONDecodeError:
            continue
    return features, labels

def get_all_paintings_metadata():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, image_path, location, year FROM paintings")
    rows = cursor.fetchall()
    conn.close()

    metadata = []
    for row in rows:
        metadata.append({
            "title": row[0],
            "image_path": row[1],
            "location": row[2],
            "year": row[3]
        })

    return metadata

def search_by_keyword_vangogh(keyword):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT * FROM paintings
    WHERE LOWER(title) LIKE '%' || LOWER(?) || '%'
    AND LOWER(author) = 'van_gogh'
    """
    cursor.execute(query, (keyword,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_metadata_full():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, year, location, image_path,
               dominant_colors_path, heatmap_path,
               classification_diagram_path, author
        FROM paintings
    """)
    rows = cursor.fetchall()
    conn.close()

    metadata = []
    for row in rows:
        metadata.append({
            "title": row[0],
            "year": row[1],
            "location": row[2],
            "image_path": row[3],
            "dominant_colors_path": row[4],
            "heatmap_path": row[5],
            "classification_diagram_path": row[6],
            "author": row[7]
        })

    return metadata

if __name__ == "__main__":
    init_db()
    print("Baza de date a fost creată (sau deja exista):", DB_PATH)
