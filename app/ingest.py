import geopandas as gpd


def load_geojson_to_geodataframe(file_path: str) -> gpd.GeoDataFrame:
    """
    Loads a GeoJSON file into a GeoDataFrame.

    Args:
        file_path: The path to the GeoJSON file.

    Returns:
        A GeoDataFrame containing the data from the GeoJSON file.
    """
    gdf = gpd.read_file(file_path)
    return gdf
