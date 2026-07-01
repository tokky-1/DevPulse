# DevPulse

DevPulse is a FastAPI-based backend service for tracking and summarizing a developer's GitHub activity. It lets users register, authenticate, sync their public GitHub push events, and view useful activity insights such as total commits, repository count, top languages, and commit streaks.

The project is designed to be simple to run locally or with Docker, and it includes health checks, PostgreSQL persistence, and scheduled activity syncing.

## Why this project exists

Developers often want a lightweight way to monitor their coding activity over time. DevPulse provides a backend API that can:

- collect GitHub activity data from a public GitHub profile
- store that activity in a relational database
- expose summary metrics for dashboards or personal analytics
- support authentication for individual users

## Features

- User registration and login with JWT-based authentication
- Protected endpoints for authenticated users
- GitHub activity sync from public GitHub event history
- Activity persistence with SQLAlchemy and PostgreSQL
- Summary metrics for total commits, repositories, and top language
- Commit streak calculation
- Health and readiness endpoints
- Scheduled background sync jobs using APScheduler
- Database migrations with Alembic

## Tech stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic / Pydantic Settings
- JWT authentication with python-jose
- Alembic for migrations
- Pytest for tests
- Docker Compose for local deployment

## Project structure

- main.py: FastAPI app entry point and scheduler setup
- routes/: API endpoints for auth, GitHub data, and health checks
- services/: business logic for auth and GitHub activity workflows
- repositories/: database access helpers
- models/: SQLAlchemy models for users and GitHub activities
- schemas/: request and response models
- database/: database connection and session management
- test/: API tests
- alembic/: database migration files

## Prerequisites

Before you begin, make sure you have:

- Python 3.12+
- PostgreSQL running locally or access to a database URL
- Docker and Docker Compose (optional, but recommended)

## Environment variables

Create a .env file in the project root with values similar to the following:

```env
DB_URL=postgresql://postgres:postgres@localhost:5432/devpulse
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GITHUB_TOKEN=your-github-token
```

Notes:

- DB_URL should point to your PostgreSQL instance.
- SECRET_KEY should be a strong random value.
- GITHUB_TOKEN is included in settings and can be used for future authenticated GitHub integrations.

## Quick start

### Option 1: Run with Docker Compose

This is the easiest way to start the app and its database.

```bash
docker compose up --build
```

The API will be available at:

- http://localhost:8000
- Health check: http://localhost:8000/health

### Option 2: Run locally with Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

If you are using Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Start the app:

```bash
uvicorn main:app --reload
```

## Database migrations

If you need to initialize or update the database schema:

```bash
alembic upgrade head
```

## API overview

### Authentication

- POST /User/register: create a new user
- POST /User/login: sign in and receive a JWT token
- GET /User/me: get the current authenticated user

### GitHub activity

- POST /Github/request_activity?github_username=your_username: sync GitHub push events for the given username
- GET /Github/summary: get totals and top-language summary
- GET /Github/streak: get the current commit streak

### Health

- GET /health: basic liveness check
- GET /health/ready: readiness check against the database

## Example usage

Register a user:

```bash
curl -X POST "http://localhost:8000/User/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"dev@example.com","username":"devuser","github_username":"octocat","password":"strongpassword"}'
```

Login:

```bash
curl -X POST "http://localhost:8000/User/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=devuser&password=strongpassword"
```

Sync GitHub activity:

```bash
curl -X POST "http://localhost:8000/Github/request_activity?github_username=octocat" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Testing

Run the test suite with:

```bash
pytest
```

## Notes

- The app includes a background scheduler that syncs activity every 6 hours.
- The current GitHub sync flow pulls public event data and stores relevant push events.
- The service is intentionally lightweight and can be extended with analytics, dashboards, or richer GitHub integration later.
