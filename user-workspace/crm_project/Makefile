# Development Commands
.PHONY: install dev test lint clean build run migrate

# Variables
PYTHON = python3
PIP = pip3
MANAGE = $(PYTHON) manage.py
DOCKER_COMPOSE = docker-compose

# Development setup
install:
	$(PIP) install -r requirements.txt

dev:
	$(MANAGE) runserver 0.0.0.0:8000

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

shell:
	$(MANAGE) shell

# Testing and Linting
test:
	pytest

coverage:
	pytest --cov=. --cov-report=html

lint:
	flake8 .
	black . --check
	isort . --check-only

format:
	black .
	isort .

# Cleaning
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

# Docker Commands
docker-build:
	$(DOCKER_COMPOSE) build

docker-up:
	$(DOCKER_COMPOSE) up -d

docker-down:
	$(DOCKER_COMPOSE) down

docker-logs:
	$(DOCKER_COMPOSE) logs -f

docker-ps:
	$(DOCKER_COMPOSE) ps

docker-shell:
	$(DOCKER_COMPOSE) exec web bash

docker-test:
	$(DOCKER_COMPOSE) run --rm web pytest

docker-migrate:
	$(DOCKER_COMPOSE) run --rm web python manage.py migrate

# Database Commands
createdb:
	$(MANAGE) reset_db --noinput
	$(MANAGE) migrate
	$(MANAGE) createsuperuser

dumpdata:
	$(MANAGE) dumpdata --exclude auth.permission --exclude contenttypes > fixtures/initial_data.json

loaddata:
	$(MANAGE) loaddata fixtures/initial_data.json

# Celery Commands
celery-worker:
	celery -A crm_project worker --loglevel=info

celery-beat:
	celery -A crm_project beat --loglevel=info

# Production Commands
collect-static:
	$(MANAGE) collectstatic --noinput

check-deploy:
	$(MANAGE) check --deploy

prod-migrate:
	$(MANAGE) migrate --noinput

prod-setup: prod-migrate collect-static

# Backup Commands
backup-db:
	$(MANAGE) dbbackup
	$(MANAGE) mediabackup

restore-db:
	$(MANAGE) dbrestore
	$(MANAGE) mediarestore

# Documentation Commands
docs-build:
	cd docs && make html

docs-serve:
	cd docs/_build/html && python -m http.server 8000

# Help Command
help:
	@echo "Available commands:"
	@echo "Development:"
	@echo "  install         - Install project dependencies"
	@echo "  dev            - Run development server"
	@echo "  migrate        - Run database migrations"
	@echo "  shell          - Open Django shell"
	@echo ""
	@echo "Testing and Linting:"
	@echo "  test           - Run tests"
	@echo "  coverage       - Run tests with coverage report"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Format code"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build   - Build Docker images"
	@echo "  docker-up      - Start Docker containers"
	@echo "  docker-down    - Stop Docker containers"
	@echo "  docker-logs    - View Docker logs"
	@echo "  docker-shell   - Open shell in web container"
	@echo ""
	@echo "Database:"
	@echo "  createdb       - Create and set up database"
	@echo "  dumpdata       - Export database data"
	@echo "  loaddata       - Import database data"
	@echo ""
	@echo "Celery:"
	@echo "  celery-worker  - Start Celery worker"
	@echo "  celery-beat    - Start Celery beat"
	@echo ""
	@echo "Production:"
	@echo "  collect-static - Collect static files"
	@echo "  check-deploy   - Check deployment settings"
	@echo "  prod-setup     - Run production setup"
	@echo ""
	@echo "Backup:"
	@echo "  backup-db      - Backup database and media"
	@echo "  restore-db     - Restore database and media"
	@echo ""
	@echo "Documentation:"
	@echo "  docs-build     - Build documentation"
	@echo "  docs-serve     - Serve documentation"