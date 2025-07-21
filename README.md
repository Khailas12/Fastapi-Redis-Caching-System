# FastAPI Redis Caching System

This project demonstrates how to integrate **Redis** with **FastAPI** to build a scalable and efficient caching system. It includes examples of caching user and item data, as well as clearing cache entries.


## Table of Contents
- [FastAPI Redis Caching System](#fastapi-redis-caching-system)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Start the Application](#2-start-the-application)
    - [3. Verify the Setup](#3-verify-the-setup)
    - [Connection to `docker-compose.yml`](#connection-to-docker-composeyml)
      - [FastAPI Health Check](#fastapi-health-check)
      - [Redis Health Check](#redis-health-check)
    - [Summary](#summary)
  - [How It Works](#how-it-works)
    - [1. Caching with Redis](#1-caching-with-redis)
      - [Example: Caching User Data](#example-caching-user-data)
      - [Example: Caching Item Data](#example-caching-item-data)
    - [2. Clearing Cache](#2-clearing-cache)
      - [Example: Clearing User Cache](#example-clearing-user-cache)
      - [Example: Clearing Item Cache](#example-clearing-item-cache)
    - [3. Redis Configuration](#3-redis-configuration)
  - [API Endpoints](#api-endpoints)
    - [Redis V1 (Basic CRUD Operations)](#redis-v1-basic-crud-operations)
    - [Redis V2 (User Data Caching)](#redis-v2-user-data-caching)
  - [Project Structure](#project-structure)
  - [Code Examples](#code-examples)
    - [Caching User Data](#caching-user-data)
    - [Clearing User Cache](#clearing-user-cache)
  - [Contributing](#contributing)
  - [License](#license)
    - [Key Sections:](#key-sections)

## Features
- **FastAPI**: A modern, high-performance web framework for building APIs with Python.
- **Redis**: An in-memory data structure store used as a caching layer.
- **Caching**: Built-in caching decorator to cache API responses.
- **Docker**: Containerized setup for easy deployment and development.
- **GET & DELETE Operations**: Examples of caching and clearing cache for user and item data.

## Prerequisites
- Docker and Docker Compose installed on your machine.
- Basic knowledge of FastAPI and Redis.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Khailas12/Fastapi-Redis-Caching-System.git
cd Fastapi-Redis-Caching-System
```

### 2. Start the Application
Run the following command to start the FastAPI application and Redis using Docker Compose:
```bash
docker-compose up --build
```

This will:
- Build the Docker image for the FastAPI application.
- Start the Redis container.
- Start the FastAPI application on `http://localhost:8000`.

### 3. Verify the Setup
Once the containers are running, you can check the health of the application by visiting:
```
http://localhost:8000/health
```

You should see the response:
```json
{"status": "healthy"}
```

This section tells you that after running `docker-compose up --build`, you can verify that the FastAPI application is running correctly by visiting the `/health` endpoint. If the application is healthy, it will return a JSON response with `{"status": "healthy"}`.

### Connection to `docker-compose.yml`

The `docker-compose.yml` file includes health checks for both the FastAPI application (`web` service) and the Redis service. These health checks ensure that the services are running and responsive.

#### FastAPI Health Check
```15:19:docker-compose.yml
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
```

- **`test`**: This command uses `curl` to call the `/health` endpoint of the FastAPI application. If the endpoint returns a non-2xx status code, the command will fail (`exit 1`), indicating that the service is unhealthy.
- **`interval`**: The health check runs every 30 seconds.
- **`timeout`**: The command must complete within 10 seconds.
- **`retries`**: If the health check fails, it will retry up to 3 times before marking the service as unhealthy.

#### Redis Health Check
```25:29:docker-compose.yml
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
```

- **`test`**: This command uses `redis-cli ping` to check if the Redis server is responsive. If Redis is running, it will respond with `PONG`.
- **`interval`**: The health check runs every 30 seconds.
- **`timeout`**: The command must complete within 10 seconds.
- **`retries`**: If the health check fails, it will retry up to 3 times before marking the service as unhealthy.

### Summary

- The `/health` endpoint in the FastAPI application is used to verify that the service is running correctly.
- The `docker-compose.yml` file includes health checks for both the FastAPI application and Redis to ensure they are operational.
- The `README.md` file guides users on how to manually verify the health of the application by visiting the `/health` endpoint.

These health checks are crucial for maintaining the reliability of your application, especially in a containerized environment where services need to be monitored for uptime and responsiveness.

## How It Works

### 1. Caching with Redis
The project uses Redis to cache API responses. The `cache_response` decorator is used to cache the results of specific endpoints.

#### Example: Caching User Data
- **Endpoint**: `GET /redis-v2/users/{user_id}`
- **Cache Key**: `users:user:{user_id}`
- **TTL**: 120 seconds

When you call this endpoint, the response is cached in Redis. Subsequent calls within the TTL will return the cached data.

#### Example: Caching Item Data
- **Endpoint**: `GET /redis-v1/items/{item_id}`
- **Cache Key**: `item_{item_id}`
- **TTL**: 3600 seconds

### 2. Clearing Cache
You can clear the cache for a specific user or item using the delete endpoints.

#### Example: Clearing User Cache
- **Endpoint**: `DELETE /redis-v2/users/{user_id}`
- **Cache Key**: `users:user:{user_id}`

#### Example: Clearing Item Cache
- **Endpoint**: `DELETE /redis-v1/delete/{item_id}`
- **Cache Key**: `item_{item_id}`

### 3. Redis Configuration
The Redis connection pool is configured in `app/config/redis.py`. This ensures that the Redis client is reused across the application, improving performance.

## API Endpoints

### Redis V1 (Basic CRUD Operations)
- **GET /redis-v1/items/{item_id}**: Retrieve item data (cached).
- **DELETE /redis-v1/delete/{item_id}**: Clear item cache.

### Redis V2 (User Data Caching)
- **GET /redis-v2/users/{user_id}**: Retrieve user data (cached).
- **DELETE /redis-v2/users/{user_id}**: Clear user cache.

## Project Structure
```
Fastapi-Redis-Caching-System/
  - app/
    - main.py
    - services/
      - redis_basic/
        - v1/
          - router.py
          - service.py
          - schemas.py
        - v2/
          - router.py
          - cache_response.py
    - config/
      - redis.py
  - docker-compose.yml
  - Dockerfile
  - requirements.txt
```

## Code Examples

### Caching User Data
```python
@router.get("/users/{user_id}")
@cache_response(ttl=120, namespace="users")
async def get_user_details(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Clearing User Cache
```python
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    cache_key = f"users:user:{user_id}"
    await redis_client.delete(cache_key)
    return {"message": "User cache removed successfully"}
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
### Key Sections:
1. **Features**: Highlights the main features of the project.
2. **Installation**: Step-by-step instructions to set up the project.
3. **How It Works**: Explains the caching mechanism and how to use the API.
4. **API Endpoints**: Lists the available endpoints and their functionality.
5. **Project Structure**: Provides an overview of the project’s directory structure.
6. **Code Examples**: Includes snippets of key functionality.
7. **Contributing**: Encourages contributions from the community.
8. **License**: Specifies the license for the project.

This `README.md` is designed to be clear and comprehensive, making it easy for developers to understand and use your project. Let me know if you’d like to add or modify anything! 😊


