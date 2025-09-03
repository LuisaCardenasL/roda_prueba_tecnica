# Architecture and Design Decisions

This document provides a high-level overview of the project's architecture and the key design decisions made during its implementation.

## Architecture

The project is implemented as a simple and robust ETL (Extract, Transform, Load) pipeline. This architecture was chosen for its simplicity and effectiveness in processing data in batches.

The pipeline consists of three main stages:

1.  **Extract:** The data is extracted from a local GeoJSON file containing information about temporary bike lanes in Bogotá.
2.  **Transform:** The raw data is transformed using the `geopandas` and `pandas` libraries. The transformations include data cleaning, column renaming, and the addition of a `run_id` for traceability.
3.  **Load:** The transformed data is loaded into a PostgreSQL database with the PostGIS extension, which allows for storing and querying geospatial data.

## Technology Stack

The following technologies were used in this project:

*   **Python 3.10:** The programming language used for the application logic.
*   **Geopandas & Pandas:** For data manipulation and analysis, especially for geospatial data.
*   **SQLAlchemy:** For connecting to the PostgreSQL database.
*   **PostgreSQL + PostGIS:** As the destination database for storing the transformed data. PostGIS is used for its powerful geospatial capabilities.
*   **Docker:** For containerizing the PostgreSQL database, which ensures a reproducible and isolated development environment.

## Design Decisions

*   **Batch Mode:** We chose to implement the application in "Batch" mode, as recommended in the project description for the MVP. This approach is simpler to implement and operate for data that is updated periodically.
*   **GeoJSON as Data Source:** We chose to use the GeoJSON format for the data source because it contains both the descriptive attributes and the essential geometry data, which is crucial for any geospatial analysis.
*   **Local Development with Docker:** We used Docker to run the PostgreSQL/PostGIS database locally. This makes the development environment easy to set up and consistent across different machines.
*   **Modular Code:** The application code is organized into modules with clear responsibilities (`ingest`, `transform`, `load_pg`, `db`), which makes the code easier to understand, maintain, and test.
