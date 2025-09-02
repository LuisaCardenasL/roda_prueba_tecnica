CREATE SCHEMA IF NOT EXISTS roda;

CREATE TABLE IF NOT EXISTS roda.ciclovias_temporales (
  run_id TEXT,
  fid INT,
  objectid INT,
  observaciones TEXT,
  tipologia TEXT,
  fase TEXT,
  estado TEXT,
  shape_length NUMERIC,
  inserted_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (run_id, objectid)
);
