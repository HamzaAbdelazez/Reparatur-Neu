## Getting Started

### Running with Docker Compose:

```bash
# Build the Docker images defined in the docker-compose.yml without cache
docker-compose build --no-cache

# Start containers in the foreground (attach to logs)
docker-compose up

# After starting, open the API docs at:
# http://0.0.0.0:8000/docs
```