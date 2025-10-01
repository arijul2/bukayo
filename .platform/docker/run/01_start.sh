#!/bin/bash

# Start the application
docker-compose up -d

# Keep the container running
tail -f /dev/null
