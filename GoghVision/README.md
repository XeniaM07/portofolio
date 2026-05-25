# GoghVision

GoghVision is a desktop application developed as part of my Bachelor's Thesis in Computer Science, focused on the analysis and classification of Vincent van Gogh artworks using image processing and machine learning techniques.

The purpose of the project is to determine whether an uploaded image represents a painting created by Vincent van Gogh and, if the prediction is positive, provide additional contextual and visual information related to the artwork.

The application combines concepts from:
- Computer Vision
- Content-Based Image Retrieval (CBIR)
- Image Processing
- Feature Extraction
- Machine Learning
- Deep Learning

---

# Thesis Information

### Thesis title
**Analysis and Classification of Vincent van Gogh Artworks Using Image Processing and Machine Learning Techniques**

---

# Project Overview

The application was designed around a complete image analysis pipeline.

A dataset containing Van Gogh paintings organized by artistic periods/locations, together with non-Van Gogh artworks, is processed in order to:
- extract visual features
- train machine learning models
- classify paintings
- retrieve visually similar artworks

The project includes both:
- an image analysis and classification system
- a graphical desktop interface for interacting with the models and visualizations

---

# Main Functionalities

## 1. Binary Artwork Classification

The application determines whether an image belongs to:
- Vincent van Gogh
or
- another artist

A binary classification model is trained using extracted image features.

---

## 2. Location / Period Classification

If the painting is classified as a Van Gogh artwork, the application predicts the artistic period/location associated with the painting, such as:
- Arles
- Paris
- Saint-Remy
- Auvers-sur-Oise
- Nuenen

The predicted location is further associated with the approximate creation period of the artwork.

---

## 3. Content-Based Image Retrieval (CBIR)

The system implements a CBIR component capable of retrieving visually similar paintings from the internal dataset.

Similarity is computed using feature vectors extracted from images and cosine distance metrics.

---

## 4. Visual Image Analysis

For each analyzed painting, the application generates additional visual information, including:
- dominant color extraction
- heatmap visualizations
- classification probability diagrams

These visualizations help interpret the model predictions and the visual characteristics of the artwork.

---

## 5. Interactive Desktop Application

The project includes a desktop graphical user interface that allows the user to:
- upload and analyze paintings
- search paintings by title
- visualize prediction results
- inspect generated diagrams and visualizations
- retrieve similar artworks from the database

---

# Machine Learning and Image Processing Techniques

The project combines both classical image processing techniques and deep learning-based feature extraction.

The implemented methods include:
- EfficientNetB0 deep feature extraction
- Content-Based Image Retrieval (CBIR)
- LBP (Local Binary Patterns)
- HOG (Histogram of Oriented Gradients)
- Color histogram analysis
- Support Vector Machine (SVM) classification

---

# Technologies Used

The application was developed using the following technologies and libraries:
- Python
- TensorFlow / Keras
- OpenCV
- Scikit-learn
- NumPy
- Matplotlib
- Seaborn
- SQLite
- PySide6

---

# Project Structure

The project is organized into several main components:
- dataset preprocessing and feature extraction
- machine learning model training
- database generation and management
- CBIR similarity search
- prediction and analysis pipeline
- graphical user interface

The architecture separates:
- feature extraction
- classification logic
- database operations
- visualization utilities
- UI components

making the project modular and extensible.

---

# Dataset and Database

The dataset and the generated SQLite database are not included in this repository because of their large size.

The final dataset used in this project is a custom dataset created by combining, reorganizing, and preprocessing images collected from multiple public sources.

The project uses:
- a custom image dataset
- generated feature vectors
- a SQLite database containing extracted metadata and image features

Additional preprocessing and restructuring operations were performed in order to adapt the dataset to the classification and CBIR pipeline.

Because these resources exceed GitHub storage limitations, they are not included in this repository.

---

# Additional Materials

The folder:

```txt
.GoghVision-presentation/
```

contains:
- a demonstration presentation of the application
- the PowerPoint presentation used during the Bachelor Thesis defense

---
