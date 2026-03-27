.PHONY: fmt, lint

fmt:
	uv run ruff format .

lint:
	uv run ruff check --fix .

test:
	uv run pytest --cov-report=html --cov=./src