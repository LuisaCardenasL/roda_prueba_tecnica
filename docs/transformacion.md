# Data Transformation

The raw data from the GeoJSON file is transformed before being loaded into the PostgreSQL database. The following transformations are applied:

## 1. Column Renaming

The original column names from the GeoJSON file are renamed to be more "Pythonic" (lowercase and using underscores) and to match the schema of the destination table in the database.

The mapping is as follows:

| Original Name   | New Name        |
|-----------------|-----------------|
| `FID`           | `fid`           |
| `OBJECTID`      | `objectid`      |
| `Obs`           | `observaciones` |
| `Tipologia`     | `tipologia`     |
| `Fase`          | `fase`          |
| `Estado`        | `estado`        |
| `Shape__Length` | `shape_length`  |

## 2. Addition of `run_id`

A new column named `run_id` is added to the dataset. This column contains a unique identifier (UUID) for each execution of the ETL pipeline.

The `run_id` is useful for:
*   **Tracking:** It allows us to track which records were loaded in each run of the pipeline.
*   **Idempotency:** It can be used to prevent the same data from being loaded multiple times. The primary key of the destination table is `(run_id, objectid)`, which ensures that each record is unique per run.
