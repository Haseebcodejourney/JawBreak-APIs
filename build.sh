#!/bin/bash
# Build script for Render deployment

# Install dependencies
pip install -r requirements.txt

# Change to the APIs directory
cd APIs

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

echo "Build completed successfully!"
