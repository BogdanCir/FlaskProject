# FlaskProject

This is a take-home assignment project built with Flask and React.
A web application that groups anagrams together and stores the results in a database.

## Features

- group words by anagrams
- results are cached in the db
- view all previous anagrams
- search and filter history
- handles uppercase, lowercase, and mixed case input
- only accepts alphabetic characters
- REST API with proper status codes
- unit and integration tests
- github Actions for automated testing and Docker Hub deployment

## Tech Stack

**Backend**: Flask, SQLAlchemy, SQLite  
**Frontend**: React, Vite  
**DevOps**: Docker, Docker Compose, GitHub Actions, Git

### Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/BogdanCir/FlaskProject.git
cd FlaskProject
```

#### 2. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This command will:

- Build the frontend React application image
- Build the backend Flask application image
- Create and start both containers with volume mounts
- Automatically create the SQLite database

- **Frontend**: Open your browser to `http://localhost:3000`
- **Backend**: `http://localhost:5000`
