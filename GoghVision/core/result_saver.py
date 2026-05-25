import os
from shutil import copyfile
from db_access import insert_painting

def save_analysis_result(image_path, result):
    author = "van_gogh" if result["is_van_gogh"] else "other"
    location_folder = result["location"] if result["is_van_gogh"] else "other"

    dataset_dir = os.path.join(
        "dataset", "vanGogh" if result["is_van_gogh"] else "non-vanGogh", location_folder
    )
    os.makedirs(dataset_dir, exist_ok=True)

    new_image_path = os.path.join(dataset_dir, f"{result['id']}.jpg")
    copyfile(image_path, new_image_path)

    new_visual_paths = _move_visuals(result)
    _save_similar_image(result)

    record = {
        "title": "unknown",
        "year": result["year"],
        "location": result["location"] if result["is_van_gogh"] else None,
        "author": author,
        "image_path": new_image_path,
        "features": result["features"],
        "dominant_colors_path": new_visual_paths["dominant_colors_path"],
        "heatmap_path": new_visual_paths["heatmap_path"],
        "classification_diagram_path": new_visual_paths["classification_diagram_path"],
    }

    insert_painting(record)
    print(f"Saved to database and moved files.")

def _move_visuals(result):
    suffixes = {
        "dominant_colors_path": ("visuals/colors", "_colors.png"),
        "heatmap_path": ("visuals/heatmap", "_heatmap.png"),
        "classification_diagram_path": ("visuals/diagrams", "_diagram.png")
    }

    updated_paths = {}
    for key, (folder, suffix) in suffixes.items():
        os.makedirs(folder, exist_ok=True)
        new_path = os.path.join(folder, f"{result['id']}.{suffix}")
        copyfile(result[key], new_path)
        updated_paths[key] = new_path

    return updated_paths

def _save_similar_image(result):
    if "selected_similar_index" not in result:
        return

    index = result["selected_similar_index"]
    if 0 <= index < len(result.get("similar_paintings", [])):
        sim_img_path = result["similar_paintings"][index]["image_path"]
        sim_dst_dir = os.path.join("visuals", "similar")
        os.makedirs(sim_dst_dir, exist_ok=True)
        new_path = os.path.join(sim_dst_dir, f"{result['id']}_similar.jpg")
        copyfile(sim_img_path, new_path)
        print(f"Similar painting saved: {new_path}")