import os
import uuid

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def generate_dominant_colors(image_path, save_dir, num_colors=5):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_small = cv2.resize(image, (64, 64))
    pixels = image_small.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors, random_state=42).fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_

    _, counts = np.unique(labels, return_counts=True)

    fig, ax = plt.subplots()
    ax.pie(counts, colors=[c /255 for c in colors], startangle=90)
    ax.axis('equal')

    os.makedirs(save_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_colors.png"
    save_path = os.path.join(save_dir, filename)
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

    return save_path

def generate_heatmap(image_path, save_dir):
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (224, 224))
    heatmap = cv2.applyColorMap(image_resized, cv2.COLORMAP_JET)

    os.makedirs(save_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_heatmap.png"
    save_path = os.path.join(save_dir, filename)
    cv2.imwrite(save_path, heatmap)

    return save_path