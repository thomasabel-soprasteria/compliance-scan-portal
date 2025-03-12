
# Compliance Scan Portal - API Backend

A FastAPI backend for scanning and analyzing annual reports for regulatory compliance.

## Features

- Upload and process PDF annual reports
- Extract and analyze content for regulatory compliance
- Store reports and analysis results in PostgreSQL
- RESTful API for managing reports and compliance requirements

## Tech Stack

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Flyway (for database migrations)

## Setup

1. Clone the repository
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
3. Set up the PostgreSQL database
4. Configure environment variables:
   ```
   cp .env.example .env
   ```
5. Run database migrations:
   ```
   flyway migrate
   ```
6. Start the server:
   ```
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with pytest:
```
pytest
```
