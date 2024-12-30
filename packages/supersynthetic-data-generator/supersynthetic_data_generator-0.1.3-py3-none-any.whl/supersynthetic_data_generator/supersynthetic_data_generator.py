#!/usr/bin/env python
# coding: utf-8

# In[14]:


# Import required libraries
import pandas as pd
import numpy as np
import random
from faker import Faker
from PIL import Image, ImageDraw
import string

def generate_tabular_data(rows=100, cols=5):
    """
    Generate a synthetic tabular dataset.

    Parameters:
        rows (int): Number of rows in the dataset.
        cols (int): Number of columns in the dataset.

    Returns:
        pd.DataFrame: A DataFrame containing synthetic tabular data.
    """
    data = np.random.rand(rows, cols)
    columns = [f"Feature_{i+1}" for i in range(cols)]
    return pd.DataFrame(data, columns=columns)

# Test the function
tabular_data = generate_tabular_data(10, 3)
print(tabular_data)

fake = Faker()

def generate_text_data(rows=100):
    """
    Generate synthetic text data.

    Parameters:
        rows (int): Number of text entries.

    Returns:
        list: A list of synthetic text data.
    """
    return [fake.sentence() for _ in range(rows)]

# Test the function
text_data = generate_text_data(5)
print(text_data)

def generate_categorical_data(rows=100, categories=None):
    """
    Generate synthetic categorical data.

    Parameters:
        rows (int): Number of rows.
        categories (list): List of category names.

    Returns:
        list: A list of categorical data.
    """
    if categories is None:
        categories = ["Category_A", "Category_B", "Category_C"]
    return [random.choice(categories) for _ in range(rows)]

# Test the function
categorical_data = generate_categorical_data(10, ["Red", "Green", "Blue"])
print(categorical_data)

def generate_images(output_dir="images", count=10, image_size=(100, 100)):
    """
    Generate synthetic images and save them to the output directory.

    Parameters:
        output_dir (str): Directory to save the generated images.
        count (int): Number of images to generate.
        image_size (tuple): Size of each image (width, height).

    Returns:
        list: List of file paths for the generated images.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []

    for i in range(count):
        img = Image.new("RGB", image_size, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        draw = ImageDraw.Draw(img)
        text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        draw.text((10, 10), text, fill=(255, 255, 255))
        
        image_path = f"{output_dir}/image_{i + 1}.png"
        img.save(image_path)
        image_paths.append(image_path)

    return image_paths

# Test the function
images = generate_images(count=5)
print(images)


def generate_synthetic_dataset(rows=100, cols=5, categories=None, imagefolder_path="images", image_count=10, image_size=(100, 100)):
    """
    Generate a complete synthetic dataset with tabular, text, categorical, and image data.

    Parameters:
        rows (int): Number of rows for tabular and categorical data.
        cols (int): Number of numerical features.
        categories (list): List of category names.
        image_count (int): Number of synthetic images to generate.
        image_size (tuple): Size of each synthetic image.

    Returns:
        dict: A dictionary containing the synthetic dataset and paths to generated images.
    """
    tabular = generate_tabular_data(rows, cols)
    text = generate_text_data(rows)
    categorical = generate_categorical_data(rows, categories)
    images = generate_images(imagefolder_path,count=image_count, image_size=image_size)
    
    # Combine into a single DataFrame
    dataset = tabular.copy()
    dataset["Text"] = text
    dataset["Category"] = categorical
    dataset["Image_Path"] = images[:rows]  # Map images to rows if count exceeds

    return {"dataset": dataset, "images": images}

# Test the function
#synthetic_data = generate_synthetic_dataset(10, 3, ["Red", "Green", "Blue"], "imagepath",20, (100, 100))
#print(synthetic_data["dataset"])
#print("Generated Images:", synthetic_data["images"])

def get_synthetic_data(rows, cols, categories, imagefolder_path, image_count, image_size):
    return generate_synthetic_dataset(rows, cols, categories, imagefolder_path, image_count, image_size)


# In[ ]:




