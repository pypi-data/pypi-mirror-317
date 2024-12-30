# Super Synthetic Data Generator

A Python library to generate synthetic datasets for testing machine learning models. It supports:
- Tabular Data
- Text Data
- Categorical Data
- Image Data

## Installation

pip install supersynthetic-data-generator

## Usage
from supersynthetic_data_generator import get_synthetic_data

synthetic_data = get_synthetic_data(
    rows=10, cols=3, categories=["Red", "Green", "Blue"],
    imagefolder_path="image_output_folderpath",
    image_count=10, image_size=(100, 100)
)
print(synthetic_data)
