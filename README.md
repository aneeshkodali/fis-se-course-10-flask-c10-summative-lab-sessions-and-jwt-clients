# Productivity Tasks API

## Description

Productivity Tasks API is a Flask backend for a task tracking application. It supports session-based authentication, protected user accounts, and full CRUD actions for tasks that belong to individual users.

Users can sign up, log in, stay logged in through a session cookie, and manage only their own tasks. Task index results are paginated so clients can request smaller pages of data.

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-RESTful
- Flask-Bcrypt
- Marshmallow
- SQLite

## Installation

From the project root, install dependencies:

```bash
pipenv install
pipenv shell
```

## Database Setup

Run migrations from the `server` directory:

```bash
cd server
flask db upgrade head
```

To reset the database with starter data:

```bash
python seed.py
```

The seed file creates three users and several tasks.

Demo users:

| Username | Password |
| --- | --- |
| `aneesh` | `password123` |
| `sam` | `password123` |
| `maya` | `password123` |

## Running the API

From the `server` directory:

```bash
python app.py
```

The Flask API runs on:

```text
http://localhost:5555
```

## Optional Frontend

This project includes two provided frontend templates. The backend is built for the session-based client:

```bash
npm install --prefix client-with-sessions
npm start --prefix client-with-sessions
```

The sessions frontend proxies requests to the Flask API on port `5555`.

## Authentication Endpoints

| Method | Endpoint | Auth Required | Description |
| --- | --- | --- | --- |
| `POST` | `/signup` | No | Creates a user, hashes their password, starts a session, and returns the user. |
| `POST` | `/login` | No | Authenticates a user and starts a session. |
| `GET` | `/check_session` | Yes | Returns the current logged-in user if the session is active. |
| `DELETE` | `/logout` | Yes | Clears the current user session. |

### Signup Request

```json
{
  "username": "newuser",
  "password": "password123",
  "password_confirmation": "password123"
}
```

### Login Request

```json
{
  "username": "aneesh",
  "password": "password123"
}
```

## Task Endpoints

All task endpoints require an authenticated session. Users can only access tasks that belong to their own account.

| Method | Endpoint | Auth Required | Description |
| --- | --- | --- | --- |
| `GET` | `/tasks?page=1&per_page=10` | Yes | Returns the logged-in user's tasks with pagination metadata. |
| `POST` | `/tasks` | Yes | Creates a new task for the logged-in user. |
| `PATCH` | `/tasks/<id>` | Yes | Updates one task owned by the logged-in user. |
| `DELETE` | `/tasks/<id>` | Yes | Deletes one task owned by the logged-in user. |

### Task Request Body

```json
{
  "title": "Draft project README",
  "description": "Document setup, seed instructions, and endpoints.",
  "priority": "medium",
  "status": "not started",
  "due_date": "2026-05-26"
}

### Paginated Tasks Response

```json
{
  "page": 1,
  "per_page": 2,
  "total": 3,
  "total_pages": 2,
  "items": [
    {
      "id": 1,
      "title": "Plan weekly study schedule",
      "description": "Block time for Flask review, project work, and interview practice.",
      "priority": "high",
      "status": "in progress",
      "due_date": "2026-05-22",
      "user_id": 1
    }
  ]
}
```