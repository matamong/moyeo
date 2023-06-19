#! /usr/bin/env bash

set -e

# Load environment variables from the .env file
source .env

# SQL query to check if the database exists
CHECK_DATABASE_QUERY="SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB';"

# SQL query to create the database
CREATE_DATABASE_QUERY="CREATE DATABASE $POSTGRES_DB;"

# SQL query to check if the test database exists
CHECK_TEST_DATABASE_QUERY="SELECT 1 FROM pg_database WHERE datname='test';"

# SQL query to create the test database
CREATE_TEST_DATABASE_QUERY="CREATE DATABASE test;"

# Check if the database exists
database_exists=$(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -t -c "$CHECK_DATABASE_QUERY")

if [ -z "$database_exists" ]; then
  # Database doesn't exist, create it
  echo "Database does not exist. Creating..."
  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -c "$CREATE_DATABASE_QUERY"
else
  echo "Database already exists. Good to go..."
fi

# Check if the test database exists
test_database_exists=$(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -t -c "$CHECK_TEST_DATABASE_QUERY")

if [ -z "$test_database_exists" ]; then
  # Test database doesn't exist, create it
  echo "Test database does not exist. Creating..."
  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -c "$CREATE_TEST_DATABASE_QUERY"
else
  echo "Test database already exists. Good to go..."
fi

# Run migrations
alembic upgrade head
alembic -x dbname=test upgrade head