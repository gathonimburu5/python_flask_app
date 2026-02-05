#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL with proper connection check
max_attempts=30
attempt=0

until PGPASSWORD="@Paulmburu5" psql -h "book_db" -U "postgres" -d "SkoteDb" -c '\q' 2>/dev/null; do
  attempt=$((attempt + 1))
  if [ $attempt -ge $max_attempts ]; then
    echo "ERROR: PostgreSQL did not become ready in time"
    exit 1
  fi
  echo "PostgreSQL is unavailable - attempt $attempt/$max_attempts - sleeping"
  sleep 2
done

echo "PostgreSQL is up and ready!"

echo "Running database migrations..."
flask db upgrade

if [ $? -ne 0 ]; then
  echo "ERROR: Database migration failed"
  exit 1
fi

echo "Migrations completed successfully!"
echo "Starting Flask application on port 8080..."

exec flask run --host=0.0.0.0 --port=8080
