from pysheds.grid import Grid
import matplotlib.pyplot as plt
import numpy as np
import os
import rasterio
from scipy.ndimage import binary_erosion
from shapely.ops import unary_union, polygonize
from shapely.geometry import LineString
from rasterio.features import shapes
import geopandas as gpd
import json
import folium


def calculate_flow_direction_and_accumulation(dem_path, dirmap=(64, 128, 1, 2, 4, 8, 16, 32)):
    """
    Calculate flow direction and accumulation for a given DEM.

    Args:
        dem_path (str): Path to the DEM file.
        dirmap (tuple): Directional mapping for flow direction (default: D8).

    Returns:
        tuple: Grid object, flow direction array, and accumulation array.
    """
    grid = Grid.from_raster(dem_path)
    dem = grid.read_raster(dem_path)

    pit_filled_dem = grid.fill_pits(dem)
    flooded_dem = grid.fill_depressions(pit_filled_dem)
    inflated_dem = grid.resolve_flats(flooded_dem)

    fdir = grid.flowdir(inflated_dem, dirmap=dirmap)
    acc = grid.accumulation(fdir, dirmap=dirmap)

    print("Flow direction and accumulation calculated successfully.")
    return grid, fdir, acc


def extract_and_save_river_network(grid, fdir, acc, river_threshold, dirmap, raster_path, plot_path, geojson_path):
    """
    Extract the river network and save it as a GeoJSON, raster (GeoTIFF), and visualization (PNG).

    Args:
        grid (Grid): PySheds Grid object.
        fdir (np.ndarray): Flow direction.
        acc (np.ndarray): Flow accumulation.
        river_threshold (int): Minimum accumulation for river network.
        dirmap (tuple): Directional mapping for flow direction.
        raster_path (str): Path to save the river network as a raster.
        plot_path (str): Path to save the river network visualization.
        geojson_path (str): Path to save the river network as a GeoJSON file.
    """
    branches = grid.extract_river_network(fdir, acc > river_threshold, dirmap=dirmap)

    river_mask = acc > river_threshold
    grid.to_raster(river_mask, raster_path)
    print(f"River network raster saved at: {raster_path}")

    line_strings = [
        LineString(branch['geometry']['coordinates'])
        for branch in branches['features']
    ]

    gdf = gpd.GeoDataFrame(geometry=line_strings, crs=grid.crs)
    gdf.to_file(geojson_path, driver="GeoJSON")
    print(f"River network GeoJSON saved at: {geojson_path}")

    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    plt.xlim(grid.bbox[0], grid.bbox[2])
    plt.ylim(grid.bbox[1], grid.bbox[3])
    ax.set_aspect('equal')

    for branch in branches['features']:
        line = np.asarray(branch['geometry']['coordinates'])
        plt.plot(line[:, 0], line[:, 1])

    plt.title('D8 Channels', size=14)
    plt.savefig(plot_path)
    plt.close()
    print(f"River network visualization saved at: {plot_path}")


def delineate_and_export_watershed_with_river(dem_path, x, y, bassinname, accumulation_threshold=1000, river_threshold=80, output_dir="output"):
    """
    Full pipeline to delineate a watershed and extract river networks, saving outputs as raster and visualization.

    Args:
        dem_path (str): Path to the DEM file.
        x, y (float): Coordinates of the point of interest.
        bassinname (str): Name for the output files.
        accumulation_threshold (int): Threshold for snapping to high-flow cells.
        river_threshold (int): Threshold for river network extraction.
        output_dir (str): Directory to save the outputs.
    """
    os.makedirs(output_dir, exist_ok=True)

    grid, fdir, acc = calculate_flow_direction_and_accumulation(dem_path)
    dirmap = (64, 128, 1, 2, 4, 8, 16, 32)

    x_snap, y_snap = grid.snap_to_mask(acc > accumulation_threshold, (x, y))
    catch = grid.catchment(x=x_snap, y=y_snap, fdir=fdir, dirmap=dirmap, xytype='coordinate')

    raster_path = os.path.join(output_dir, f"{bassinname}_watershed.tif")
    grid.clip_to(catch)
    grid.to_raster(acc, raster_path)

    plot_path = os.path.join(output_dir, f"{bassinname}_river.png")
    geojson_path = os.path.join(output_dir, f"{bassinname}_river.geojson")
    extract_and_save_river_network(grid, fdir, acc, river_threshold, dirmap, raster_path, plot_path, geojson_path)


def convert_watershed_tif_to_geojson_with_edges(tif_path, output_geojson_path):
    """
    Convert a GeoTIFF file to GeoJSON by detecting edges and polygonizing the raster.

    Args:
        tif_path (str): Path to the input GeoTIFF file.
        output_geojson_path (str): Path to save the output GeoJSON file.
    """
    with rasterio.open(tif_path) as src:
        raster = src.read(1)
        transform = src.transform
        crs = src.crs

        mask = raster > 0
        edges = mask & ~binary_erosion(mask)

        edges_shapes = shapes(edges.astype('uint8'), transform=transform)

        polylines = [
            LineString(shape[0]['coordinates'][0])
            for shape in edges_shapes if shape[1] == 1
        ]

        merged_line = unary_union(polylines)
        polygons = list(polygonize([merged_line]))

        if len(polygons) > 0:
            largest_polygon = max(polygons, key=lambda p: p.area)
        else:
            raise ValueError("No valid polygons found in the raster.")

        gdf = gpd.GeoDataFrame(geometry=[largest_polygon], crs=crs)
        gdf.to_file(output_geojson_path, driver='GeoJSON')
        print(f"GeoJSON saved at: {output_geojson_path}")


def show_geojson(file):
    """
    Display a GeoJSON file on an interactive Folium map and show the centroid.
    """
    df = gpd.read_file(file)
    geom = df.geometry[0]
    centroid = geom.centroid
    centroid_coords = (centroid.y, centroid.x)

    geoJSON = json.loads(df.to_json())
    m = folium.Map(location=centroid_coords, zoom_start=12)
    folium.GeoJson(geoJSON).add_to(m)
    folium.Marker(
        location=centroid_coords,
        popup=f"Centroid: {centroid_coords}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    m.add_child(folium.LayerControl())
    display(m)


def show_tiff_on_map(tiff_path):
    """
    Display a GeoTIFF file on a Folium map.
    """
    with rasterio.open(tiff_path) as src:
        raster = src.read(1)
        bounds = src.bounds

        min_lon, min_lat, max_lon, max_lat = bounds.left, bounds.bottom, bounds.right, bounds.top
        raster_min = raster.min()
        raster_max = raster.max()
        raster = (255 * (raster - raster_min) / (raster_max - raster_min)).astype('uint8')

        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

        folium.raster_layers.ImageOverlay(
            image=raster,
            bounds=[[min_lat, min_lon], [max_lat, max_lon]],
            opacity=0.6,
            colormap=lambda x: (x, x, x),
        ).add_to(m)
        m.add_child(folium.LayerControl())
        display(m)
