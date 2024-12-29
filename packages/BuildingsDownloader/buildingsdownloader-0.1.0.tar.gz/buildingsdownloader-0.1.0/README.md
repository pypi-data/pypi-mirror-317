# Building Footprints Downloader

This script downloads building footprints within a specified area of interest (AOI), which can be defined either by a shapefile or by a bounding box (min/max latitude and longitude coordinates). It uses the `mercantile` library to handle tile-based requests and fetches building footprint data from a global dataset. The results are saved as a GeoJSON file.

## Features
- Fetch building footprints within a specified AOI.
- Support for AOI input as a shapefile or bounding box (minx, miny, maxx, maxy).
- Supports querying building footprint data from a global dataset by tile using quadkeys.
- Outputs results as a GeoJSON file.

## Requirements
- Python 3.6+
- Required Python libraries:
  - pandas
  - geopandas
  - shapely
  - mercantile
  - tqdm
  - argparse

You can install the required libraries using `pip`:

```bash
pip install pandas geopandas shapely mercantile tqdm
```

## Usage

### Command Line Arguments

- `--shp` (optional): Path to the input shapefile defining the AOI. If not provided, you must provide bounding box coordinates (`--minx`, `--miny`, `--maxx`, `--maxy`).
- `--minx` (optional): Minimum X coordinate (longitude) of the bounding box.
- `--miny` (optional): Minimum Y coordinate (latitude) of the bounding box.
- `--maxx` (optional): Maximum X coordinate (longitude) of the bounding box.
- `--maxy` (optional): Maximum Y coordinate (latitude) of the bounding box.
- `--output`: Required. Output file path (GeoJSON format) for the result.

### Example Usage

1. **Using a shapefile to define the AOI:**

```bash
python download_buildings.py --shp path_to_shapefile.shp --output output.geojson
```

2. **Using a bounding box to define the AOI:**

```bash
python download_buildings.py --minx -122.5 --miny 37.5 --maxx -122.0 --maxy 38.0 --output output.geojson
```

In this case, the bounding box is defined by:
- `minx`: Minimum longitude
- `miny`: Minimum latitude
- `maxx`: Maximum longitude
- `maxy`: Maximum latitude

### Notes

- If both a shapefile (`--shp`) and bounding box coordinates are provided, the shapefile will be used.
- The `mercantile` library is used to divide the requested area into tiles. Each tile is fetched by its quadkey from the global dataset.
- The output is saved as a `.geojson` file, which can be opened in GIS software such as QGIS.
