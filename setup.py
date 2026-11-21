# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="xids",
    version="1.0.0",
    description="Explainable AI Network Intrusion Detection System (X-IDS)",
    author="Ahmed Khaled",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "scikit-learn>=1.0.0",
        "xgboost>=1.5.0",
        "ipykernel>=6.0.0",
    ],
    python_requires=">=3.8",
)
