.PHONY: install lint format test check docker

install:
	uv sync
	uv run pre-commit install

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

dbt-build:
	uv run dbt build

check: lint test dbt-build

docker:
	docker build -t entrepot-donnees-ouvertes .
	docker run --rm entrepot-donnees-ouvertes
