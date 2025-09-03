import geopandas as gpd
import uuid


def transform_data(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Transforms the raw bike lane GeoDataFrame.

    Args:
        gdf: The raw GeoDataFrame from the ingest step.

    Returns:
        The transformed GeoDataFrame.
    """
    # Rename columns to match the database schema
    gdf = gdf.rename(
        columns={
            "FID": "fid",
            "OBJECTID": "objectid",
            "Obs": "observaciones",
            "Tipologia": "tipologia",
            "Fase": "fase",
            "Estado": "estado",
            "Shape__Length": "shape_length",
        }
    )

    # Add a run_id for tracking and idempotency
    gdf["run_id"] = str(uuid.uuid4())

    # Select and reorder columns to match the database table
    transformed_gdf = gdf[
        [
            "run_id",
            "fid",
            "objectid",
            "observaciones",
            "tipologia",
            "fase",
            "estado",
            "shape_length",
            "geometry",
        ]
    ].copy()

    return transformed_gdf
