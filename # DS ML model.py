import numpy as np
import rasterio
import matplotlib.pyplot as plt

def calculate_indices(nir, red, green, swir):
    ndvi = (nir - red) / (nir + red)
    ndmi = (nir - swir) / (nir + swir)
    ndre = (nir - green) / (nir + green)
    msavi = (2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 8 * (nir - red))) / 2
    return ndvi, ndmi, ndre, msavi

def generate_recommendations(ndvi, ndmi, ndre, msavi):
    recommendations = {}
    if ndvi < 0.2:
        recommendations['NDVI'] = "Low vegetation cover, consider soil improvement."
    elif ndvi < 0.5:
        recommendations['NDVI'] = "Moderate vegetation cover, consider irrigation."
    else:
        recommendations['NDVI'] = "Healthy vegetation, maintain current practices."

    if ndmi < 0:
        recommendations['NDMI'] = "Dry conditions, consider irrigation."
    else:
        recommendations['NDMI'] = "Sufficient moisture, maintain current practices."

    if ndre < 0.2:
        recommendations['NDRE'] = "Low crop health, consider pest control."
    else:
        recommendations['NDRE'] = "Healthy crops, maintain current practices."

    if msavi < 0.2:
        recommendations['MSAVI'] = "Low vegetation density, consider fertilization."
    else:
        recommendations['MSAVI'] = "Good vegetation density, maintain current practices."

    return recommendations

def analyze_satellite_image(image_path):
    with rasterio.open(image_path) as src:
        band_red = src.read(1)
        band_green = src.read(2)
        band_nir = src.read(3)
        band_swir = src.read(4)

    ndvi, ndmi, ndre, msavi = calculate_indices(band_nir, band_red, band_green, band_swir)
    recommendations = generate_recommendations(np.nanmean(ndvi), np.nanmean(ndmi), np.nanmean(ndre), np.nanmean(msavi))

    return recommendations

image_path = 'path_to_your_satellite_image.tif'
recommendations = analyze_satellite_image(image_path)
print(recommendations)
