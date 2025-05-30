#!/bin/bash
set -e

echo "Waiting for database..."
sleep 5
exec flask run --debug --host=0.0.0.0 --port=5001