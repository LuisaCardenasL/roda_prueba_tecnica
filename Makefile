.PHONY: install run test fmt lint docker-build docker-run docker-prune

install:
	pip install -r requirements.txt

run:
	# On Windows, you might need to set environment variables manually
	# or use a library like python-dotenv in the code.
	# This command is intended for Unix-like shells (e.g., Git Bash, WSL).
	export $(grep -v '^#' .env | xargs) && python -m app.main --mode batch

test:
	python -m pytest

fmt:
	python -m ruff check --fix . && python -m black .

lint:
	python -m ruff check . && python -m black --check .

docker-build:
	docker build -t roda-microservice:local .

docker-run:
	docker run --rm -it \
	  --env-file .env \
	  --network host \
	  roda-microservice:local


docker-prune:
	docker system prune -f