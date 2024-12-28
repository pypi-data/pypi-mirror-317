import os
from setuptools import setup, find_packages

# Directory where the script is located
PACKAGE_NAME = "HierarTree"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=PACKAGE_NAME,
    version="0.1",
    author="Leonardo Biral",
    author_email="leonardo.biral@duke.edu",
    description="A Python package for hierarchical decision tree and random forest classifiers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lbiral/HierarTree",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "joblib",
        "matplotlib",
        "sklearn"
    ],
)
