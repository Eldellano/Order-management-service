include .env
export

dev.build:
	docker compose --env-file .env -f "docker/dev/main.yml" build --pull --no-cache

dev.down:
	docker compose --env-file .env -f "docker/dev/main.yml" down

dev.up:
	docker compose --env-file .env -f "docker/dev/main.yml" up -d

dev.log:
	docker compose --env-file .env -f "docker/dev/main.yml" logs -f

dev.network:
	docker network create order-management-service.private

dev.rebuild: dev.build dev.down dev.up

local.run:
	PYTHONPATH=src uvicorn main:app --reload --host $(APP_HOST) --port $(APP_PORT)