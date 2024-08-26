import rasterio
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def calculate_indices(red, nir, swir, green):
    ndvi = (nir - red) / (nir + red)
    ndmi = (nir - swir) / (nir + swir)
    ndre = (nir - green) / (nir + green)
    msavi = (2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 8 * (nir - red))) / 2
    return ndvi, ndmi, ndre, msavi

def load_geotiff(file_path):
    with rasterio.open(file_path) as src:
        red = src.read(1)
        green = src.read(2)
        nir = src.read(3)
        swir = src.read(4)
    return red, green, nir, swir

def create_dataset(red, green, nir, swir):
    ndvi, ndmi, ndre, msavi = calculate_indices(red, nir, swir, green)
    data = {
        'NDVI': ndvi.flatten(),
        'NDMI': ndmi.flatten(),
        'NDRE': ndre.flatten(),
        'MSAVI': msavi.flatten()
    }
    return pd.DataFrame(data)

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    return model

def main(file_path, labels):
    red, green, nir, swir = load_geotiff(file_path)
    dataset = create_dataset(red, green, nir, swir)
    model = train_model(dataset, labels)
    return model

# Example usage
# file_path = 'path_to_your_geotiff_file.tif'
# labels = np.array([...])  # Your labels for training
# model = main(file_path, labels)
