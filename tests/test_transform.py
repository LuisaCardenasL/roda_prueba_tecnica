import geopandas as gpd
from shapely.geometry import LineString
from app.transform import transform_data


def test_transform_data():
    # Create a sample GeoDataFrame
    data = {
        "FID": [1],
        "OBJECTID": [1],
        "Obs": ["Observation 1"],
        "Tipologia": ["Tipo 1"],
        "Fase": ["Fase 1"],
        "Estado": ["Estado 1"],
        "Shape__Length": [100.0],
        "geometry": [LineString([(0, 0), (1, 1)])],
    }
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # Transform the data
    transformed_gdf = transform_data(gdf)

    # Check that columns are renamed
    expected_columns = [
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
    assert all(col in transformed_gdf.columns for col in expected_columns)

    # Check that run_id is added
    assert "run_id" in transformed_gdf.columns
    assert transformed_gdf["run_id"].iloc[0] is not None
