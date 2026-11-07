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

check: lint test

docker:
	docker build -t modele-projet .
	docker run --rm modele-projet
