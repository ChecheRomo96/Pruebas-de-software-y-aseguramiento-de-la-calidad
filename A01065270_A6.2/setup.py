"""
setup.py

Setup script for packaging and installing the 'app' module.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="app",
    version="0.1",
    author="José Manuel Romo",
    description="A hotel management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically finds 'app' and sub-packages
    install_requires=[  # Add dependencies if needed
        "jsonschema",  # Example dependency, replace or add more as necessary
    ],
    python_requires=">=3.8",  # Ensures compatibility with Python 3.8+
    classifiers=[  # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  # Includes non-Python files (e.g., JSON, configs)
)
