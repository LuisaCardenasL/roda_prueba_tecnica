# Local Execution Guide

This guide explains how to run the ETL pipeline locally.

## 0. Start the PostgreSQL Container

This project requires a PostgreSQL database with the PostGIS extension. You can start a container with the following command:

```bash
docker run --name roda-postgres -e POSTGRES_DB=roda -e POSTGRES_USER=roda -e POSTGRES_PASSWORD=roda -p 5432:5432 -d postgis/postgis
```

## 1. Create your `.env` file

Copy the `.env.example` file and rename it to `.env`.

```bash
cp .env.example .env
```

The default values in the file should work with the provided Docker setup.

## 2. Install Dependencies

Make sure you have a Python virtual environment activated. Then, install the required libraries:

```bash
pip install -r requirements.txt
```

## 3. Create the Database Table

This step uses the running PostgreSQL container. The following command will execute the `sql/init.sql` script to create the necessary table.

On Windows:
```bash
type sql\init.sql | docker exec -i roda-postgres psql -U roda -d roda -f -
```

On macOS/Linux:
```bash
cat sql/init.sql | docker exec -i roda-postgres psql -U roda -d roda -f -
```

## 4. Run the Application

Now you can run the ETL pipeline:

```bash
python -m app.main --mode batch
```

You should see output in your terminal indicating the progress of the ETL process.