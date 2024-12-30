from setuptools import setup, find_packages

setup(
    name="supersynthetic-data-generator",
    version="0.1.1",
    author="Ujwal Watgule",
    author_email="ujwalwatgule@gmail.com",
    description="A library to generate synthetic datasets for testing ML models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/UjwalWtg/supersynthetic-data-generator",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "faker"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
