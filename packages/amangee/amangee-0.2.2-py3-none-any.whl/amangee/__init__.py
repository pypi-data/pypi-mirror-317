# __init__.py
from .gee import download_satellite_data
from .ai import train_model
# amangee/__init__.py

# Import functions from hydrology.py
from .hydrology import (
    calculate_flow_direction_and_accumulation,
    extract_and_save_river_network,
    delineate_and_export_watershed_with_river,
    convert_watershed_tif_to_geojson_with_edges,
    delineate_and_save_watershed,
    show_geojson,
    show_tiff_on_map
)

# Optional: Define the package's public API
__all__ = [
    "calculate_flow_direction_and_accumulation",
    "extract_and_save_river_network",
    "delineate_and_export_watershed_with_river",
    "convert_watershed_tif_to_geojson_with_edges",
    "delineate_and_save_watershed",
    "show_geojson",
    "show_tiff_on_map"
]
