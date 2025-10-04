#!/bin/bash

# Set environment variables
export DOCKERHUB_USERNAME=${DOCKERHUB_USERNAME}
export OPENAI_API_KEY=${OPENAI_API_KEY}

# Start the application using docker-compose
docker-compose -f docker-compose.production.yml up