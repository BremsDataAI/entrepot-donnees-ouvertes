.PHONY: install lint format test ingest dbt-build check

install:
	uv sync
	uv run pre-commit install

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .

ingest:
	uv run python -m ingestion.load_pam
	uv run python -m ingestion.load_ansd
	uv run python -m ingestion.load_world_bank

dbt-build:
	uv run dbt build

test:
	uv run pytest

check: lint ingest dbt-build test

docker:
	docker build -t entrepot-donnees-ouvertes .
	docker run --rm entrepot-donnees-ouvertes
