#!/bin/bash

set -e

# Function to wait for postgres
wait_for_postgres() {
    until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
        >&2 echo "Postgres is unavailable - sleeping"
        sleep 1
    done
    >&2 echo "Postgres is up - executing command"
}

# Function to wait for redis
wait_for_redis() {
    until redis-cli -h "$REDIS_HOST" ping; do
        >&2 echo "Redis is unavailable - sleeping"
        sleep 1
    done
    >&2 echo "Redis is up - executing command"
}

# Wait for dependencies
if [ -n "$DB_HOST" ]; then
    wait_for_postgres
fi

if [ -n "$REDIS_HOST" ]; then
    wait_for_redis
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create cache tables
echo "Creating cache tables..."
python manage.py createcachetable

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
fi

# Load initial data if LOAD_FIXTURES is set
if [ "$LOAD_FIXTURES" = "true" ]; then
    echo "Loading initial data..."
    python manage.py loaddata initial_data
fi

# Start Celery worker if running worker container
if [ "$CONTAINER_ROLE" = "worker" ]; then
    echo "Starting Celery worker..."
    celery -A crm_project worker --loglevel=info
    exit 0
fi

# Start Celery beat if running beat container
if [ "$CONTAINER_ROLE" = "beat" ]; then
    echo "Starting Celery beat..."
    celery -A crm_project beat --loglevel=info
    exit 0
fi

# Start development server if running in development
if [ "$DJANGO_SETTINGS_MODULE" = "crm_project.settings_dev" ]; then
    echo "Starting development server..."
    python manage.py runserver 0.0.0.0:8000
    exit 0
fi

# Execute the passed command (default: gunicorn)
exec "$@"