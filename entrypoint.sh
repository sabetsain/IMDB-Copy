#!/bin/bash
set -e

echo "Waiting for database..."
sleep 5
# flask init-db
exec flask run --host=0.0.0.0 --port=5001