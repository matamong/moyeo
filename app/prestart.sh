#! /usr/bin/env bash

set -e

# Load environment variables from the .env file
source ../.env

# Function to check if the PostgreSQL server is reachable
check_postgres_connection() {
  echo "Checking PostgreSQL connection..."
  if PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -c "SELECT 1" >/dev/null 2>&1; then
    echo "Connected to PostgreSQL server successfully."
  else
    echo "Failed to connect to PostgreSQL server. Please check your database settings."
    exit 1
  fi
}

# Check PostgreSQL connection
check_postgres_connection

# SQL query to check if the database exists
CHECK_DATABASE_QUERY="SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB';"

# SQL query to create the database
CREATE_DATABASE_QUERY="CREATE DATABASE $POSTGRES_DB;"

# SQL query to check if the test database exists
CHECK_TEST_DATABASE_QUERY="SELECT 1 FROM pg_database WHERE datname='test';"


# Check if the database exists
database_exists=$(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -t -c "$CHECK_DATABASE_QUERY")

if [ -z "$database_exists" ]; then
  # Database doesn't exist, create it
  echo "Database does not exist. Creating..."
  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -c "$CREATE_DATABASE_QUERY"
else
  echo "Database already exists. Good to go..."
fi

# Run migrations
alembic upgrade head
