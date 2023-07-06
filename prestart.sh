#! /usr/bin/env bash

# Load environment variables from the .env file
echo "Setting env..."
#if [ -f .env ]; then
#  set -a
#  . .env
#  set +a
#fi

set -e

envfile=".env"

if [ -f "$envfile" ]; then
  # Read the .env file and export key-value pairs
  while IFS= read -r line || [ -n "$line" ]; do
    # Exclude comments and empty lines
    if [[ $line != \#* ]] && [[ $line != "" ]]; then
      # Extract the key and value from each line
      key=$(echo "$line" | cut -d '=' -f1)
      value=$(echo "$line" | cut -d '=' -f2-)

      # Remove leading/trailing whitespace and quotation marks from the value
      value=$(echo "$value" | sed 's/^[[:space:]"'\'']\+//' | sed 's/[[:space:]"'\'']\+$//')

      # Check if the value is an array-like structure
      if [[ $value == \[*\] ]]; then
        # Remove the brackets and split the values by comma
        value=$(echo "$value" | sed 's/^\[//' | sed 's/\]$//' | tr ',' '\n')
      fi

      # Export the key-value pairs as environment variables
      export "$key"="$value"
    fi
  done < "$envfile"
fi

# Print the environment variables for verification
echo "POSTGRES_SERVER: $POSTGRES_SERVER"



echo "----------------Done setting env..."

# Function to check if the PostgreSQL server is reachable
check_postgres_connection() {
  echo "Checking PostgreSQL connection...to $"
  if PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -c "SELECT 1" >/dev/null 2>&1; then
    echo "Connected to PostgreSQL server successfully."
  else
    echo "Failed to connect to PostgreSQL server. Please check your database settings."
    exit 1
  fi
}

# Check PostgreSQL connection
#check_postgres_connection

# SQL query to check if the database exists
#CHECK_DATABASE_QUERY="SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB';"

# SQL query to create the database
#CREATE_DATABASE_QUERY="CREATE DATABASE $POSTGRES_DB;"

# SQL query to check if the test database exists
#CHECK_TEST_DATABASE_QUERY="SELECT 1 FROM pg_database WHERE datname='test';"


# Check if the database exists
#database_exists=$(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -t -c "$CHECK_DATABASE_QUERY")

#if [ -z "$database_exists" ]; then
  # Database doesn't exist, create it
#  echo "Database does not exist. Creating..."
#  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_SERVER" -U "$POSTGRES_USER" -p 5432 -c "$CREATE_DATABASE_QUERY"
#else
#  echo "Database already exists. Good to go..."
#fi

# Run migrations
echo "-----------------Run migrations..."
alembic upgrade head
echo "-----------------Done migrations..."
