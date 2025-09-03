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

---

## How to Use This Project

### Local Execution

For detailed instructions on how to run the project locally, please see the [Local Execution Guide](docs/local_execution.md).

### Makefile Commands

This project uses a `Makefile` to automate common tasks:

*   `make install`: Installs all the necessary Python dependencies from `requirements.txt`.
*   `make run`: Runs the main ETL pipeline in batch mode.
*   `make test`: Runs the unit tests using `pytest`.
*   `make lint`: Checks the code for style issues and potential errors using `ruff` and `black`.
*   `make fmt`: Automatically formats the code to be consistent.
*   `make docker-build`: Builds the Docker image for the application.
*   `make docker-run`: Runs the application inside a Docker container.
*   `make docker-prune`: Cleans up unused Docker images and containers.

---

## Deploying with Terraform

This project uses Terraform to manage and deploy the necessary Google Cloud infrastructure.

> **Prerequisites:**
> * You need to have [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed.
> * You need to have the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated (`gcloud auth login`).

### 1. Build and Push the Docker Image

Before running Terraform, you need to build the Docker image and push it to Google Artifact Registry. Terraform will create the repository for you, but you need to push the image manually for the first deployment.

**First, set these environment variables:**

```bash
# Replace with your GCP Project ID
export PROJECT_ID=<your_project_id>

# You can change these if you want
export REGION_GCP=us-central1
export REPO=roda-repo
export IMAGE=roda-microservice
```

**Then, run these commands to build and push the image:**

```bash
gcloud builds submit --tag $REGION_GCP-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest .
```

### 2. Configure Terraform

1.  Navigate to the `terraform` directory:
    ```bash
    cd terraform
    ```

2.  Create a file named `terraform.tfvars` and add the following content, replacing `<your_project_id>` with your GCP Project ID:
    ```terraform
    gcp_project_id = "<your_project_id>"
    ```

3.  **Important:** You also need to update the database credentials in the `terraform/main.tf` file. For a real project, you should use a secure method like Google Secret Manager to handle these credentials.

### 3. Initialize, Plan, and Apply

1.  **Initialize Terraform:** This will download the necessary providers.
    ```bash
    terraform init
    ```

2.  **Plan the deployment:** This will show you what resources Terraform is going to create.
    ```bash
    terraform plan
    ```

3.  **Apply the configuration:** This will create the resources in your GCP project.
    ```bash
    terraform apply
    ```

After the `apply` command is finished, Terraform will output the URL of your new Cloud Run service.