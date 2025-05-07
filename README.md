# Agri-Buddy Backend Dockerization


This document explains how to run the Agri-Buddy backend using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
  
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup Instructions

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd Agri-Buddy-Backend
   ```

2. **Configure Environment Variables**
   
   Copy the example .env file and edit it with your actual credentials:
   ```
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your:
   - OpenAI API key
   - Disease detection API endpoint

3. **Build and Start the Docker Container**
   ```
   docker-compose up -d
   ```
   
   This will build the Docker image and start the container in detached mode.

4. **Check the Application Logs**
   ```
   docker-compose logs -f
   ```

5. **Access the Application**
   
   The API will be available at: http://localhost:5000

## File Structure

- `Dockerfile`: Contains instructions for building the Docker image
- `docker-compose.yml`: Defines the services, networks, and volumes
- `.env`: Contains environment variables for the application
- `.dockerignore`: Specifies files to exclude from the Docker build

## Important Directories

- `/app/uploads`: Directory for storing uploaded images
- `/app/database`: Directory for storing vector database files

## Stopping the Application

To stop the container:
```
docker-compose down
```

## Rebuilding After Code Changes

If you make changes to the code, rebuild the container:
```
docker-compose up -d --build
```

## Troubleshooting

1. **Container fails to start**
   - Check logs: `docker-compose logs`
   - Verify environment variables in `.env` file
   - Ensure required API endpoints are accessible from within the container

2. **API calls fail**
   - Check if the OpenAI API key is valid
   - Ensure the disease detection API endpoint is accessible

3. **Volume mounting issues**
   - Ensure the `database` and `uploads` directories exist
   - Check permissions on these directories
