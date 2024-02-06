.PHONY: help build-local up down api db migration
.DEFAULT_GOAL := help

build-local: ## Build docker image to local development(M1 no-chache)
	docker compose -f docker-compose.yml build --no-cache

up: ## Start docker container
	docker compose -f docker-compose.yml up -d

down: ## Stop docker container
	docker compose -f docker-compose.yml down

api: ## Run python container
	docker compose exec -it fastapi /bin/bash

db: ## Run mysql container
	docker compose exec -it mysql  mysql -u root -p

migration: ## Run alembic migration
	docker compose exec -it fastapi alembic upgrade head

migration-rollback: ## Run alembic migration
	docker compose exec -it fastapi alembic downgrade -1

migration-refresh: ## Run alembic migration
	docker compose exec -it fastapi alembic downgrade base
	docker compose exec -it fastapi alembic upgrade head

create-migration: ## Create alembic migration
ifndef filename
	$(error filename is not set)
endif
	docker compose exec -it fastapi alembic revision --autogenerate -m "$(filename)"

cache-clear: ## Clear cache
	docker compose exec -it fastapi find . -type d -name "__pycache__" -exec rm -r {} +