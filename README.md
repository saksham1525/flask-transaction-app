## Flask Transaction API

A simple Flask REST API demonstrating **CRUD operations**, Request Validation with **Marshmallow**, **SQLAlchemy ORM**, **Database Persistence** using **SQLite**, **JWT Authentication**, HTML template rendring with **Bootstrap**, and **Docker containerization**.

### Build & Run
```bash

# Build image (first time only)
docker build -t flask-app .

# Run container
docker run -p 5000:5000 flask-app
```

### Authentication

```bash
# Get JWT token
curl -X POST -H "Content-Type: application/json" \
-d '{"username": "admin", "password": "password123"}' \
http://localhost:5000/login
```

### API Endpoints

```bash
# Get all transactions: JSON
curl http://localhost:5000/transactions

# Add transaction - Requires JWT token
curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN_HERE" \
-d '{"description": "book", "amount": -300}' \
http://localhost:5000/transactions

# View all transactions: Bootstrap UI
http://localhost:5000/view

# Home
curl http://localhost:5000/
```

### Useful Commands

```bash
# Stop container
docker stop flask-app

# Start container
docker start flask-app

#Database is stored inside container. To persist data across container removals
docker run -p 5000:5000 -v $(pwd)/instance:/app/instance flask-app

#To run without Docker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Tech Stack
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Marshmallow** - Data validation
- **SQLite** - Lightweight database
- **PyJWT** - JWT token authentication
- **Bootstrap 5** - UI styling
- **Docker** - Containerization
