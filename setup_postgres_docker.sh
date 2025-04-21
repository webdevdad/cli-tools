#!/bin/bash
# Script to launch a Postgres test database using Docker

docker run --name test-postgres -e POSTGRES_USER=testuser -e POSTGRES_PASSWORD=testpass -e POSTGRES_DB=testdb -p 5432:5432 -d postgres:15

echo "Postgres test database started on localhost:5432 with user=testuser, password=testpass, dbname=testdb"
