#!/bin/bash

# WiFi Portal Backend Startup Script for Render

echo "Starting WiFi Portal Backend..."

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Initialize database with sample data if needed
echo "Checking if database needs initialization..."
python -c "
from app import app, db, User
with app.app_context():
    if User.query.count() == 0:
        print('Initializing database with sample data...')
        from app import init_db
        init_db()
    else:
        print('Database already has data, skipping initialization.')
"

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:$PORT app:app
