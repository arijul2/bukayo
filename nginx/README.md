# Nginx Configuration for Bukayo App

This directory contains nginx configuration files for the Bukayo application deployment on AWS Elastic Beanstalk.

## Files Overview

- `default.conf` - Production configuration with HTTPS redirect
- `default-dev.conf` - Development configuration without HTTPS redirect
- `default-production.conf` - Optimized production configuration for Elastic Beanstalk
- `common.conf` - Shared configuration for all environments
- `Dockerfile` - Development Docker image
- `Dockerfile.production` - Production Docker image with optimizations
- `apple-app-site-association` - Apple App Site Association file

## Deployment Configuration

### For Elastic Beanstalk Production:

Use `Dockerfile.production` and `default-production.conf`:

```bash
# Build production image
docker build -f Dockerfile.production -t bukayo-nginx:production .

# Run locally for testing
docker run -p 80:80 bukayo-nginx:production
```

### For Development:

Use `Dockerfile` and `default-dev.conf`:

```bash
# Build dev image
docker build -f Dockerfile -t bukayo-nginx:dev .

# Run locally
docker run -p 80:80 bukayo-nginx:dev
```

## Architecture

The nginx server acts as a reverse proxy:

- **Frontend (React)**: Served on port 3000, accessible at `/`
- **API (FastAPI)**: Served on port 8000, accessible at `/api/*`
- **WebSocket**: Supported for real-time features at `/ws`

## Environment Variables

The configuration expects the following services to be running:

- Frontend service on `127.0.0.1:3000`
- API service on `127.0.0.1:8000`

## Health Checks

The production configuration includes a health check endpoint at `/health` that returns a simple "healthy" response.

## Security Features

- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- Gzip compression for better performance
- Static file caching
- Proper proxy headers for Elastic Beanstalk

## Apple App Site Association

The configuration properly serves the Apple App Site Association file at `/.well-known/apple-app-site-association` for iOS app integration.
