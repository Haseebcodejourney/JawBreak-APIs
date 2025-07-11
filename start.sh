#!/bin/bash
# Start script for Render deployment

# Change to the APIs directory
cd APIs

# Start the Gunicorn server
exec gunicorn APIs.wsgi:application --bind 0.0.0.0:$PORT
