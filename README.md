# Roda Technical Challenge - Jr. Machine Learning Engineer

This repository contains the solution for the Roda technical challenge. It's a data microservice that ingests data about temporary bike lanes in Bogotá, transforms it, and loads it into a PostgreSQL database.

## Architecture

The project follows a simple ETL (Extract, Transform, Load) architecture:

```
[GeoJSON File] -> [Python Script] -> [PostgreSQL Database]
```

*   **Extract:** The data is extracted from a local GeoJSON file (`dataset/Ciclovias_Temporales.geojson`).
*   **Transform:** The data is transformed using `geopandas` and `pandas` (see `docs/transformacion.md` for details).
*   **Load:** The transformed data is loaded into a PostgreSQL database with PostGIS support (see `sql/init.sql` for the schema).

## How to Run Locally

For detailed instructions on how to run the project locally, please see the [Local Execution Guide](docs/local_execution.md).

## Data Source

The data used in this project is the "Ciclovías Temporales" dataset from the city of Bogotá. For more details, see the [Data Source Documentation](docs/fuente.md).

## Data Transformation

The raw data is transformed before being loaded into the database. For a detailed explanation of the transformations, see the [Data Transformation Documentation](docs/transformacion.md).

## Project Structure

```
.
├── app/
│   ├── main.py                # Main entry point for the ETL pipeline
│   ├── ingest.py              # Ingestion logic
│   ├── transform.py           # Transformation logic
│   ├── load_pg.py             # Loading logic
│   └── db.py                  # Database connection setup
├── dataset/
│   └── Ciclovias_Temporales.geojson # The raw data file
├── docs/
│   ├── local_execution.md     # Guide for running the project locally
│   ├── fuente.md              # Data source documentation
│   └── transformacion.md      # Data transformation documentation
├── sql/
│   └── init.sql               # Database schema definition
├── .env.example               # Example environment variables
├── Makefile                   # Makefile for common tasks
└── requirements.txt           # Python dependencies
```