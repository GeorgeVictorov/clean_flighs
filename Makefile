.PHONY: all build up down test unit-tests integration-tests e2e-tests logs

all: down build up test

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down --remove-orphans

test: up
	docker compose run --rm --no-deps api pytest tests

unit-tests:
	docker compose run --rm --no-deps api pytest tests/unit

integration-tests: up
	docker compose run --rm --no-deps api pytest tests/integration

e2e-tests: up
	docker compose run --rm --no-deps api pytest tests/e2e
logs:
	docker compose logs -f api