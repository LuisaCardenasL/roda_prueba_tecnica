import argparse
from app.ingest import load_geojson_to_geodataframe
from app.transform import transform_data
from app.load_pg import load_geodataframe_to_postgres
from app.db import sync_engine


def main():
    """
    Main function to run the ETL pipeline.
    """
    parser = argparse.ArgumentParser(
        description="Roda Technical Challenge - Batch Mode"
    )
    parser.add_argument(
        "--mode", type=str, required=True, help="Execution mode (batch or real-time)"
    )
    parser.add_argument("--region", type=str, help="Region to process")
    parser.add_argument("--start", type=str, help="Start date")
    parser.add_argument("--end", type=str, help="End date")

    args = parser.parse_args()

    if args.mode == "batch":
        print("Running in batch mode...")

        # 1. Ingest
        print("Ingesting data...")
        file_path = "dataset/Ciclovias_Temporales.geojson"
        raw_gdf = load_geojson_to_geodataframe(file_path)
        print(f"Loaded {len(raw_gdf)} features.")

        # 2. Transform
        print("Transforming data...")
        transformed_gdf = transform_data(raw_gdf)
        print("Data transformed.")

        # 3. Load
        print("Loading data to PostgreSQL...")
        load_geodataframe_to_postgres(transformed_gdf, sync_engine)
        print("Data loaded successfully.")

        print("ETL pipeline finished.")
    else:
        print(f"Mode '{args.mode}' is not supported yet.")


if __name__ == "__main__":
    main()
