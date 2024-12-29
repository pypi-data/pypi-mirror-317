# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="BuildingsDownloader",
    version="0.1.0",
    author="Araz Shahkarami",
    author_email="araz.shah@gmail.com",
    description="A package to download and process building footprints from bounding box data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arazshah/get_buildings",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "shapely",
        "geopandas",
        "mercantile",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "buildingsDownloader=BuildingsDownloader.main:main",
        ],
    },
)
