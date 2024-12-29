# Download Building

**Download Building** is a Python package for downloading and processing building footprint data within a specified bounding box or area of interest (AOI). It leverages global datasets and outputs geospatial data files for further analysis.

## Features

- Process building footprints from a bounding box or shapefile.
- Automatically download and filter building data using `mercantile` and `shapely`.
- Save output as a GeoJSON file for GIS workflows.

## Installation

You can install the package using `pip`:

```bash
pip install getbuildings
```

## Usage

### Command-Line Interface (CLI)

You can use the package from the command line by providing either a shapefile (`.shp`) or bounding box coordinates.

```bash
python -m getbuildings \
  --shp /path/to/aoi.shp \
  --output /path/to/output.geojson
```

Or, use bounding box coordinates:

```bash
python -m getbuildings \
  --minx <min_x> --miny <min_y> \
  --maxx <max_x> --maxy <max_y> \
  --output /path/to/output.geojson
```

### Parameters

- `--shp`: Path to the input shapefile defining the AOI (optional).
- `--minx`, `--miny`, `--maxx`, `--maxy`: Bounding box coordinates (required if `--shp` is not provided).
- `--output`: Path to save the output GeoJSON file (required).

### Example

To process a bounding box:

```bash
python -m getbuildings \
  --minx -123.5 --miny 45.0 \
  --maxx -122.5 --maxy 46.0 \
  --output output.geojson
```

## Development

### Clone the Repository

To work on the project locally:

```bash
git clone https://github.com/arazshah/get_buildings.git
cd getbuildings
```

### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Run Locally

Run the script using sample inputs:

```bash
python main.py --minx -123.5 --miny 45.0 --maxx -122.5 --maxy 46.0 --output output.geojson
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [mercantile](https://github.com/mapbox/mercantile) for tile processing.
- [Shapely](https://shapely.readthedocs.io) for geometry operations.
- [GeoPandas](https://geopandas.org) for geospatial data handling.
