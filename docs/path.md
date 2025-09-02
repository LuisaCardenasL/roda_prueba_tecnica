# Project Plan: Roda Technical Challenge

This document outlines the path to successfully complete the technical challenge.

### 1. Setup your Environment
*   Install necessary tools like Python 3.10+, Docker, and the Google Cloud SDK.
*   Set up a local PostgreSQL instance.
*   Create a Python virtual environment.

### 2. Initialize the Project
*   Create the directory structure as recommended in the `README.md`.
*   Initialize a `git` repository to track your changes.

### 3. Choose Execution Mode
*   Decide between a "Batch" or "Real-time" service. The document recommends starting with "Batch".

### 4. Select Data Source
*   Choose a public dataset that is relevant to Roda's business (e.g., mobility, security, economics).
*   Document your choice in `docs/fuente.md`.

### 5. Develop the Application (`app/`)
*   **`sql/init.sql`**: Define your PostgreSQL table schema.
*   **`app/db.py`**: Set up the database connection.
*   **`app/ingest.py`**: Write code to fetch data from your chosen source.
*   **`app/transform.py`**: Implement the core transformation logic (e.g., joins, feature engineering, scoring).
*   **`app/load_pg.py`**: Write the code to load the transformed data into PostgreSQL.
*   **`app/main.py`**: Create the entry point for your application (CLI or API).

### 6. Document Your Work
*   Explain your transformation logic in `docs/transformacion.md`.
*   Detail your design choices in `docs/arquitectura.md`.
*   Fill out the `README.md` with setup and deployment instructions.

### 7. Test and Validate
*   Write unit tests for your transformation functions.
*   Use a `Makefile` to automate testing, linting, and formatting.

### 8. Containerize with Docker
*   Write a `Dockerfile` for your application.
*   Build and test the Docker image locally.

### 9. Deploy to GCP
*   Push your Docker image to Google Artifact Registry.
*   Deploy the image to Cloud Run.
*   (Optional) Set up Cloud Scheduler for batch jobs.

### 10. Final Submission
*   Review the checklist in the `prueba.md` file.
*   Submit your work as instructed.
