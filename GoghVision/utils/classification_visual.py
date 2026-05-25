import os
import uuid
import matplotlib.pyplot as plt
import numpy as np

def generate_classification_diagram(probs, labels, save_dir, filename_prefix="diagram"):
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{filename_prefix}_{uuid.uuid4().hex[:6]}.png"
    save_path = os.path.join(save_dir, filename)

    x = np.arange(len(labels))
    width = 0.6
    fig, ax = plt.subplots(figsize=(6, 4))

    bars = ax.bar(x, probs, width, color='#3366cc', edgecolor='black')

    ax.set_ylabel("Probabilitate")
    ax.set_xlabel("Clasă")
    ax.set_title("Probabilități de clasificare")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    for bar, prob in zip(bars, probs):
        ax.annotate(f"{prob:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10)

    fig.tight_layout()
    plt.savefig(save_path)
    plt.close(fig)

    return save_path
