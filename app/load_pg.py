import geopandas as gpd
from sqlalchemy.engine import Engine

def load_geodataframe_to_postgres(gdf: gpd.GeoDataFrame, engine: Engine):
    """
    Loads a GeoDataFrame into a PostgreSQL table using a synchronous engine.

    Args:
        gdf: The GeoDataFrame to load.
        engine: The SQLAlchemy synchronous engine.
    """
    gdf.to_postgis(
        name="ciclovias_temporales",
        con=engine,
        schema="roda",
        if_exists="replace",  # 'replace' will drop the table first, 'append' will add data
        index=False
    )
