# Kanban Board API

A production-ready FastAPI backend for a Kanban board application with JWT authentication and PostgreSQL database.

## Features

- ✅ **User Authentication** - JWT-based authentication with secure password hashing
- ✅ **Kanban Board Management** - Full CRUD operations for boards, lists, and cards
- ✅ **3-Level Hierarchy** - Board → List → Card structure with cascade deletes
- ✅ **PostgreSQL Database** - Reliable data persistence with SQLAlchemy ORM
- ✅ **Database Migrations** - Alembic for version-controlled schema changes
- ✅ **Comprehensive Tests** - Full test coverage with pytest
- ✅ **API Documentation** - Auto-generated Swagger UI and ReDoc
- ✅ **Authorization** - Users can only access their own boards and resources
- ✅ **Position Management** - Drag-and-drop support with position tracking
- ✅ **Card Features** - Assignments, due dates, priorities, and descriptions

## Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **JWT** - Secure token-based authentication
- **Pytest** - Testing framework

## Project Structure

```
/root/project/
├── app/
│   ├── api/
│   │   ├── deps.py                  # Dependency injection
│   │   └── v1/
│   │       ├── endpoints/           # API endpoints
│   │       │   ├── auth.py          # Authentication
│   │       │   ├── users.py         # User management
│   │       │   ├── boards.py        # Board CRUD
│   │       │   ├── lists.py         # List CRUD
│   │       │   └── cards.py         # Card CRUD
│   │       └── router.py            # Main router
│   ├── core/
│   │   ├── config.py                # Settings
│   │   ├── database.py              # Database setup
│   │   └── security.py              # JWT & password hashing
│   ├── crud/                        # Database operations
│   ├── models/                      # SQLAlchemy models
│   ├── schemas/                     # Pydantic schemas
│   ├── main.py                      # Application entry point
│   └── initial_data.py              # Create first superuser
├── alembic/                         # Database migrations
├── tests/                           # Test suite
├── .env                             # Environment variables
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Database Schema

### User
- `id` (UUID, primary key)
- `email` (unique, indexed)
- `username` (unique, indexed)
- `hashed_password`
- `full_name`
- `is_active`, `is_superuser`
- `created_at`, `updated_at`

### Board
- `id` (UUID, primary key)
- `title`, `description`
- `owner_id` (FK to User)
- `created_at`, `updated_at`

### List
- `id` (UUID, primary key)
- `title`, `position`
- `board_id` (FK to Board)
- `created_at`, `updated_at`

### Card
- `id` (UUID, primary key)
- `title`, `description`, `position`
- `list_id` (FK to List)
- `assigned_to_id` (FK to User, nullable)
- `due_date`, `priority`
- `created_at`, `updated_at`

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip and virtualenv

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE kanban_db;
CREATE USER kanban_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE kanban_db TO kanban_user;
\q
```

### 5. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env`:
```bash
DATABASE_URL="postgresql://kanban_user:your_password@localhost:5432/kanban_db"
SECRET_KEY="your-secret-key-here"  # Generate with: openssl rand -hex 32
```

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Create Initial Superuser (Optional)

```bash
python -m app.initial_data
```

### 8. Start the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info

### Users

- `PUT /api/v1/users/me` - Update current user profile
- `PATCH /api/v1/users/me/password` - Change password

### Boards

- `GET /api/v1/boards/` - List user's boards
- `POST /api/v1/boards/` - Create board
- `GET /api/v1/boards/{board_id}` - Get board with lists and cards
- `PUT /api/v1/boards/{board_id}` - Update board
- `DELETE /api/v1/boards/{board_id}` - Delete board

### Lists

- `POST /api/v1/boards/{board_id}/lists/` - Create list
- `GET /api/v1/lists/{list_id}` - Get list
- `PUT /api/v1/lists/{list_id}` - Update list
- `DELETE /api/v1/lists/{list_id}` - Delete list
- `PATCH /api/v1/lists/{list_id}/reorder` - Reorder list

### Cards

- `POST /api/v1/lists/{list_id}/cards/` - Create card
- `GET /api/v1/cards/{card_id}` - Get card
- `PUT /api/v1/cards/{card_id}` - Update card
- `DELETE /api/v1/cards/{card_id}` - Delete card
- `PATCH /api/v1/cards/{card_id}/move` - Move card to different list
- `PATCH /api/v1/cards/{card_id}/reorder` - Reorder card

## Usage Examples

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create a Board

```bash
curl -X POST http://localhost:8000/api/v1/boards/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Project",
    "description": "Project management board"
  }'
```

### 4. Create a List

```bash
curl -X POST http://localhost:8000/api/v1/boards/<board_id>/lists/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "To Do",
    "position": 0
  }'
```

### 5. Create a Card

```bash
curl -X POST http://localhost:8000/api/v1/lists/<list_id>/cards/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement feature X",
    "description": "Add new feature to the application",
    "position": 0,
    "priority": "high"
  }'
```

### 6. Get Board with All Data

```bash
curl -X GET http://localhost:8000/api/v1/boards/<board_id> \
  -H "Authorization: Bearer <access_token>"
```

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_auth.py -v
pytest tests/test_boards.py -v
pytest tests/test_lists.py -v
pytest tests/test_cards.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=app --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Database Migrations

### Create a New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1  # Rollback one migration
alembic downgrade base  # Rollback all migrations
```

### View Migration History

```bash
alembic history
alembic current
```

## Development

### Run in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables

- `DEBUG=True` - Enable debug mode (creates tables automatically on startup)
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Secret key for JWT token generation
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)
- `CORS_ORIGINS` - Comma-separated list of allowed origins

## Production Deployment

### Disable Debug Mode

Set `DEBUG=False` in `.env` to disable automatic table creation.

### Use Gunicorn

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t kanban-api .
docker run -p 8000:8000 --env-file .env kanban-api
```

## Security Features

- ✅ **Password Hashing** - Bcrypt for secure password storage
- ✅ **JWT Tokens** - Stateless authentication
- ✅ **UUID Primary Keys** - Prevents enumeration attacks
- ✅ **Authorization Checks** - Users can only access their own resources
- ✅ **CORS Configuration** - Configurable allowed origins
- ✅ **Input Validation** - Pydantic schemas validate all inputs
- ✅ **SQL Injection Prevention** - SQLAlchemy ORM protects against SQL injection

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues, questions, or contributions, please open an issue on GitHub.
