# Marketplace API

FastAPI marketplace backend with JWT authentication, products, orders, WebSocket chat and Celery background tasks.

## Stack

- FastAPI
- PostgreSQL
- SQLAlchemy Async
- Alembic
- JWT
- Redis
- Celery
- WebSockets

## Setup

### Clone project

```bash
git clone <repo_url>
cd marketplace-api
````

### Install dependencies

```bash
poetry install
```

### Activate virtualenv

```bash
poetry shell
```

### Create .env

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/marketplace
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

## Run PostgreSQL

Example Docker container:

```bash
docker run -d \
  --name marketplace-postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=marketplace \
  -p 5432:5432 \
  postgres
```

## Run Redis

```bash
docker run -d --name redis -p 6379:6379 redis
```

## Run migrations

```bash
alembic upgrade head
```

## Run backend

```bash
poetry run uvicorn app.main:app --reload
```

## Run Celery worker

```bash
celery -A app.celery.celery_app worker --loglevel=info
```

## Run tests

```bash
pytest
```

## API Docs

```txt
http://localhost:8000/docs
```

## WebSocket Chat

```txt
ws://localhost:8000/chats/{room_id}?token=JWT_TOKEN
```
