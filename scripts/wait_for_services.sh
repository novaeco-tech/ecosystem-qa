#!/bin/sh
# A simple script to wait for services to be healthy
# This is a basic example; a real one would be more robust.

echo "Waiting for services..."

# Wait for Hub API
while! curl -s http://hub-api:8000/health; do
  echo "Waiting for Hub API..."
  sleep 2
done

# Wait for Finance API
while! curl -s http://finance-api:8000/health; do
  echo "Waiting for Finance API..."
  sleep 2
done

echo "All services are up."