# Prueba Técnica – Jr. Machine Learning Engineer en Roda

> Microservicio de datos en GCP (Cloud Run) con ingesta desde fuente pública, transformación y carga a PostgreSQL local. Este README documenta arquitectura, decisiones, despliegue y pruebas.

---

## 🧭 Resumen

* **Objetivo**: Ingerir datos públicos relevantes para Roda, transformarlos (enriquecimiento/agregación) y **cargarlos a PostgreSQL local**. El servicio **corre en Cloud Run** (Docker + Artifact Registry) y puede ejecutarse **batch** (Scheduler) o **real-time** (endpoint HTTP) según se elija.
* **Stack sugerido**: Python 3.10+, FastAPI (opcional), Pandas/PyArrow, SQLAlchemy (async + `asyncpg`), Docker, Google Cloud Run, Artifact Registry.

> El foco está en **infra** (GCP/Cloud Run) y en una **transformación no trivial** que responda una pregunta útil para Roda (movilidad, gig economy, seguridad, clima, energía, etc.).

---

## 🏗️ Arquitectura

```
[Fuente Pública] --(HTTP/CSV/JSON/GeoJSON/BigQuery Público)--> [Cloud Run Service]
                                    |                              |
                                    | Transformación (pandas/SQL)  |  
                                    v                              v
                             [Opcional: BigQuery]            [PostgreSQL Local]

Modo batch: Cloud Scheduler (HTTP) ---> Cloud Run (con parámetros)
Modo real-time: Cliente (curl/httpie) ---> Endpoint HTTP (valida payload)
```

* **Cloud Run**: contenedor stateless, escalable bajo demanda.
* **Artifact Registry**: almacenamiento de imágenes Docker.
* **PostgreSQL local**: destino final (conexión segura vía internet o túnel; para pruebas locales se puede exponer en `localhost`).
* **Opcional**: BigQuery para persistencia analítica adicional.

---

## 🎯 Decisión de ejecución (elige 1 y ajusta)

### Opción A – Batch (recomendado para MVP)

* **Cuándo**: fuentes públicas con ventanas diarias/horarias; pipelines repetibles.
* **Por qué**: más simple de operar y controlar costos. Idóneo para cálculos agregados y puntuaciones periódicas.
* **Cómo**: Cloud Scheduler → HTTP a Cloud Run con parámetros (rango de fechas, ciudad, etc.).

### Opción B – Real-time (si necesitas endpoint)

* **Cuándo**: validaciones bajo demanda, consultas ad-hoc, webhooks.
* **Por qué**: visibilidad inmediata para pruebas y demos.
* **Cómo**: FastAPI/Starlette exponiendo `POST /run` y `GET /health`.

> Justifica brevemente tu elección en este README.

---

## 📚 Selección de fuente de datos (guía)

Escoge **1+** fuentes con aplicación real para Roda y documéntalo:

* **Movilidad**: ciclorutas/accidentes/transporte (OSM/Overpass, datos abiertos de Bogotá, etc.).
* **Economía/Ingreso**: DANE/INEGI/World Bank (empleo independiente, estratos, densidad negocio).
* **Seguridad**: robos de bici/moto por zona/fecha.
* **Clima/Energía**: precipitación/temperatura (impacto en demanda), tarifas energía.
* **Comercio**: densidad de restaurantes/tiendas (última milla).

En `docs/fuente.md` explica: origen, licenciamiento, cobertura temporal/espacial, campos, calidad y **por qué ayuda a Roda**.

---

## 🧠 Transformación mínima requerida

Incluye **al menos una** de estas operaciones (o combinaciones):

* **Join geográfico** (p.ej., puntos a barrios/localidades).
* **Ventanas** (rolling, ranking por zona/hora).
* **Scoring heurístico** (ej.: potencial de demanda por barrio con ponderaciones).
* **Feature engineering** (densidades, índices, normalizaciones).
* **Detección simple de outliers** (IQR, z-score) si aplica.

Documenta la lógica en `docs/transformacion.md` con fórmulas/casos.

---

## 📦 Estructura del repositorio

```
.
├── app/
│   ├── main.py                # FastAPI/CLI entrypoint (batch o real-time)
│   ├── ingest.py              # Descarga/lectura de fuente(s) públicas
│   ├── transform.py           # Limpieza, joins, features, scoring
│   ├── load_pg.py             # Carga a PostgreSQL (SQLAlchemy async)
│   ├── db.py                  # Conexión/engine y helpers
│   └── schemas.py             # Pydantic (si endpoint) / modelos internos
├── sql/
│   └── init.sql               # DDL destino en Postgres
├── examples/
│   ├── sample_payload.json    # Ejemplo request para /run (si real-time)
│   └── sample_response.json   # Ejemplo de respuesta
├── docs/
│   ├── fuente.md              # Descripción detallada de la(s) fuente(s)
│   ├── transformacion.md      # Diseño de features/joins/score
│   └── arquitectura.md        # Diagramas y decisiones
├── Dockerfile
├── requirements.txt
├── .env.example
├── Makefile                   # Atajos: test, build, run, deploy, seed
└── README.md
```

---

## 🔑 Variables de entorno

Crea `.env` (no lo subas) a partir de `.env.example`:

```
# Base de datos local
PG_HOST=localhost
PG_PORT=5432
PG_DB=roda
PG_USER=roda
PG_PASSWORD=roda
PG_SSLMODE=disable

# Parámetros de ejecución
REGION=bogota
START_DATE=2025-01-01
END_DATE=2025-01-31

# Opcional BigQuery
BQ_PROJECT_ID=<tu_proyecto>
BQ_DATASET=roda_analytics
```

---

## 🗄️ Esquema destino (PostgreSQL)

Archivo `sql/init.sql` (ajusta nombres/campos según tu fuente):

```sql
CREATE SCHEMA IF NOT EXISTS roda;

CREATE TABLE IF NOT EXISTS roda.demanda_zona (
  run_id           TEXT,
  region           TEXT,
  zona_id          TEXT,
  zona_nombre      TEXT,
  fecha            DATE,
  hora             INT,
  densidad_comercio NUMERIC,
  clima_lluvia     NUMERIC,
  robos_bici       INT,
  score_demanda    NUMERIC,
  inserted_at      TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (run_id, region, zona_id, fecha, hora)
);
```

* **Clave primaria compuesta** para **idempotencia** (evita duplicados por reintentos).
* Agrega índices según tus consultas (`region, fecha`, etc.).

---

## ▶️ Ejecución local (sin GCP)

1. **Crear y poblar Postgres**

```bash
psql -h $PG_HOST -U $PG_USER -d $PG_DB -f sql/init.sql
```

2. **Crear entorno y deps**

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

3. **Run batch por CLI**

```bash
export $(grep -v '^#' .env | xargs)
python -m app.main --mode batch --region "$REGION" --start "$START_DATE" --end "$END_DATE"
```

4. **Run API (real-time)**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
# Healthcheck
curl -s http://localhost:8080/health
# Ejecutar
http POST :8080/run region=$REGION start=$START_DATE end=$END_DATE
```

---

## 🐳 Docker (local)

```bash
# Build
docker build -t roda-microservice:local .

# Run con .env y red para llegar a Postgres local
docker run --rm -it \
  --env-file .env \
  --network host \
  roda-microservice:local
```

> En Windows sin `--network host`, mapea `-p 8080:8080` y ajusta `PG_HOST` a la IP de tu host.

---

## ☁️ Despliegue en GCP (Cloud Run + Artifact Registry)

> Requiere tener el **SDK de GCP** configurado y facturación activa.

```bash
# Variables
PROJECT_ID=<tu_proyecto>
REGION_GCP=us-central1
REPO=roda-repo
IMAGE=roda-microservice

# 1) Habilitar servicios (una vez)
gcloud services enable artifactregistry.googleapis.com run.googleapis.com

# 2) Crear repo de contenedores (una vez)
gcloud artifacts repositories create $REPO \
  --repository-format=docker \
  --location=$REGION_GCP \
  --description="Roda microservice images"

# 3) Build & Push
gcloud builds submit --tag $REGION_GCP-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest .

# 4) Deploy a Cloud Run
gcloud run deploy $IMAGE \
  --image $REGION_GCP-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest \
  --platform managed \
  --region $REGION_GCP \
  --allow-unauthenticated \
  --set-env-vars PG_HOST=$PG_HOST,PG_PORT=$PG_PORT,PG_DB=$PG_DB,PG_USER=$PG_USER,PG_PASSWORD=$PG_PASSWORD,PG_SSLMODE=$PG_SSLMODE

# 5) Obtener URL
SERVICE_URL=$(gcloud run services describe $IMAGE --region $REGION_GCP --format='value(status.url)')
echo $SERVICE_URL
```

> **Seguridad**: considera usar **Secret Manager** para credenciales de Postgres (evita exponerlas en variables públicas/Cloud Run si es público).

---

## ⏱️ Programación (Batch) con Cloud Scheduler

```bash
# Programar ejecución diaria 06:00 (hora de la región del servicio)
SVC_URL=$SERVICE_URL

# Ejemplo de payload
cat > examples/scheduler_payload.json << 'EOF'
{
  "region": "bogota",
  "start": "2025-01-01",
  "end": "2025-01-31"
}
EOF

# Crear job Scheduler (una vez)
gcloud scheduler jobs create http roda-daily \
  --schedule="0 6 * * *" \
  --uri="$SVC_URL/run" \
  --http-method=POST \
  --message-body-from-file=examples/scheduler_payload.json \
  --headers="Content-Type=application/json"
```

---

## 🔌 Endpoints (si usas FastAPI)

* `GET /health` → 200 OK
* `POST /run` → Ejecuta ingesta → transformación → carga a Postgres

  * **Body** (JSON): `{ "region": "bogota", "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" }`
  * **200**: `{ "run_id": "...", "rows_loaded": 1234 }`
  * **4xx/5xx**: mensaje de error con trazabilidad

Incluye ejemplos en `/examples`.

---

## 🧪 Tests & calidad

* Pruebas unitarias de funciones de transformación.
* Validaciones de esquema (tipos/campos obligatorios).
* **Idempotencia**: reintentos no deben duplicar.
* **Logs estructurados** (JSON) con `run_id`, `region`, `rangos`, `rows_loaded`.

Ejemplo (Makefile):

```make
.PHONY: test fmt lint

test:
	pytest -q
fmt:
	ruff check --fix . && black .
lint:
	ruff check . && black --check .
```

---

## 🧩 Plus opcionales

* **BigQuery**: escribir dataframe transformado en `BQ_PROJECT_ID:BQ_DATASET.tabla`, útil para BI.
* **Workflows**: orquestar pasos (ingest → transform → load).
* **Terraform**: reproducir infra (Artifact Registry, Cloud Run, Scheduler, permisos).

Documenta cualquier plus en `docs/arquitectura.md`.

---

## 🧯 Troubleshooting

* **`permission denied` al desplegar**: verifica `gcloud auth login` y `roles/run.admin`, `roles/artifactregistry.admin`.
* **`cannot connect to Postgres`**: revisa firewall, `PG_HOST`, `PG_SSLMODE`, y si Cloud Run puede alcanzar tu DB (exponer temporalmente, túnel, o usa un **Cloud SQL** como alternativa para demo).
* **Timeouts en ingesta**: añade paginación/reintentos, timeouts y límites de tamaño.
* **Memoria/CPU en Cloud Run**: sube `--memory` o `--cpu` en el deploy si transformaciones pesadas.

---

## ✅ Checklist de entrega

* [ ] Cloud Run **activo** con logs y evidencias (capturas o URL ofuscada en `docs/`)
* [ ] **Fuente** documentada y justificada (por qué sirve a Roda)
* [ ] Transformación **no trivial** explicada
* [ ] **Carga a Postgres** demostrada (conteo de filas, esquema)
* [ ] README claro con **cómo correr local** y **cómo desplegar**
* [ ] `/examples` con payload y respuesta
* [ ] `sql/init.sql` incluido
* [ ] Opcional: BigQuery / Scheduler / Terraform

---

## 📫 Entrega

Envía el enlace del repo y notas de despliegue a **[santiago@roda.xyz](mailto:santiago@roda.xyz)** con asunto: **Prueba Técnica – Jr ML Engineer**. Tiempo sugerido: **1–3 días efectivos**. Prioriza un servicio que **funcione** y decisiones bien **justificadas**.

---

## 📄 Licencia

MIT (o agrega la que prefieras).

---

**¡Gracias!** ⚡️🚲 Conviertes datos abiertos en decisiones que mejoran ingresos, reducen costos y hacen la vida urbana más fácil.
