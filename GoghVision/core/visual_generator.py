import os
import uuid
from core.visual_utils import generate_dominant_colors, generate_heatmap
from utils.classification_visual import generate_classification_diagram

def generate_visuals(image_path, binary_prob):
    uid = uuid.uuid4().hex[:8]
    visual_dir = "visuals"

    dom_path = generate_dominant_colors(image_path, os.path.join(visual_dir, "colors"))
    heatmap_path = generate_heatmap(image_path, os.path.join(visual_dir, "heatmaps"))
    diagram_path = generate_classification_diagram(
        probs=binary_prob,
        labels=["other", "van_gogh"],
        save_dir=os.path.join(visual_dir, "diagrams"),
        filename_prefix=f"class_{uid}"
    )

    return uid, {
        "dominant_colors": dom_path,
        "heatmap": heatmap_path,
        "diagram": diagram_path
    }