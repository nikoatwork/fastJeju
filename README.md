# FastJeju

A FastAPI project with Pydantic and Pandas integration.

## What this repo contains

- Python environment setup with virtualenv
- FastAPI with example endpoints
- Pydantic for data validation
- Pandas for data manipulation

## Setup

Create a virtual environment:

```bash
virtualenv venv
```

Activate the environment and install dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Running the application

Start the FastAPI server:

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

API documentation is available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Running tests

```bash
pytest
```

## API Endpoints

- `GET /`: Root endpoint
- `GET /api/items`: Get all items
- `GET /api/items/{item_id}`: Get a specific item
- `POST /api/items`: Create a new item
- `GET /api/pandas/info`: Get information about the pandas DataFrame
