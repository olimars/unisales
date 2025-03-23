# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directories
RUN mkdir -p /app/logs /app/media /app/staticfiles

# Create a non-root user
RUN useradd -m crm_user && \
    chown -R crm_user:crm_user /app

# Switch to non-root user
USER crm_user

# Expose port
EXPOSE 8000

# Set up entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]

# Default command (can be overridden)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4", "crm_project.wsgi:application"]