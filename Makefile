.PHONY: install run test lint

install:
	pip install -r requirements.txt

run:
	# On Windows, you might need to set environment variables manually
	# or use a library like python-dotenv in the code.
	# This command is intended for Unix-like shells (e.g., Git Bash, WSL).
	export $(grep -v '^#' .env | xargs) && python -m app.main --mode batch

test:
	# Placeholder for running tests
	@echo "No tests yet."

lint:
	# Placeholder for linting
	@echo "No linter configured yet."
