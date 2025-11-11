# Flask Transaction API

A simple Flask REST API demonstrating CRUD operations, Request Validation with Marshmallow, SQLAlchemy ORM, Database Persistence using SQLite, HTML template rendring with Bootstrap, and Docker containerization.

### Build & Run
```bash

# Build image (first time only)
docker build -t flask-app .

# Run container
docker run -p 5000:5000 flask-app
```

## API Endpoints

```bash
# Get all transactions: JSON
curl http://localhost:5000/transactions

# Add transaction
curl -X POST -H "Content-Type: application/json" \
-d '{"description": "book", "amount": -300}' \
http://localhost:5000/transactions

# View all transactions: Bootstrap UI
http://localhost:5000/view

# Home
curl http://localhost:5000/
```

## Useful Commands

```bash
# Stop container
docker stop flask-app

# Start container
docker start flask-app

# View logs
docker logs flask-app

# Remove container
docker rm flask-app

# List running containers
docker ps

# Rebuild after changes
docker build -t flask-app . && docker run -p 5000:5000 flask-app
```

## Data Persistence

Database is stored inside container. To persist data across container removals:
```bash
docker run -p 5000:5000 -v $(pwd)/instance:/app/instance flask-app
```

## Without Docker

If you prefer to run without Docker:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Tech Stack
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Marshmallow** - Data validation
- **SQLite** - Lightweight database
- **Bootstrap 5** - UI styling
- **Docker** - Containerization
