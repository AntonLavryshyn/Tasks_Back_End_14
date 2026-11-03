# FastAPI Project

## Requirements

* Python 3.11+
* pip

## Installation

Clone the repository and navigate to the project directory:

```bash
cd QuizApp
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.sample` and configure the required environment variables.

## Running the application

Start the development server:

```bash
python -m uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## Running with Docker Compose

The local development environment is fully containerized using Docker Compose. This method automatically deploys the FastAPI application, PostgreSQL database, and Redis for caching, while also automatically tracking changes in your code.

### Prerequisites

* Docker Desktop installed and running

### Steps to Run

Instead of manually building individual images, use Docker Compose to spin up the entire infrastructure simultaneously:

1. **Start in Development Mode with Auto-Reload (Compose Watch)**:
   ```bash
   docker compose up --watch
   ```
   *This command activates two change-tracking mechanisms:*
   * **Hot Code Reloading**: Any changes made inside the `./app` folder instantly appear inside the container due to volume mounting (`volumes`). The Uvicorn server automatically restarts within milliseconds.
   * **Auto-rebuild**: If you modify or add a new library to the `requirements.txt` file, Docker Compose will automatically trigger a new image build and update the corresponding container.

2. **Standard Run (Background Mode)**:
   ```bash
   docker compose up -d
   ```

3. **Stop All Services**:
   ```bash
   docker compose down
   ```

### Accessing the Application

Once the containers are started, the services are available on your host machine at the following addresses:
* Main App: [http://localhost:8000](http://localhost:8000)
* Swagger Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc Documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔗 Database & Cache Connections Management

Since all components of the system run within an isolated Docker network (`quiz_network`), managing connections has a specific approach:

1. **Network Hosts Instead of `localhost`**:
   Inside Docker containers, the `localhost` address refers to the container itself. To communicate between services, **Docker Compose service names** are used as domain hostnames.
   * To connect to PostgreSQL, the host **`postgres_db`** is used instead of `localhost`.
   * To connect to Redis, the host **`redis_cache`** is used instead of `localhost`.

2. **Configuration via Environment Variables**:
   All database connection variables are centrally managed in the `docker-compose.yml` file under the `environment` section of the `web_app` service:
   * **DATABASE_URL**: `postgresql+asyncpg://my_user:my_password@postgres_db:5432/my_database`
   * **REDIS_URL**: `redis://redis_cache:6379/0`

3. **Startup Ordering (`depends_on`)**:
   The FastAPI service is configured to automatically wait for the PostgreSQL database to be fully ready. Thanks to the built-in `healthcheck` tool (the `pg_isready` utility), the application will not start until the DBMS begins accepting connections, which completely prevents `ConnectionRefusedError` issues during startup.

### Managing the Containers

* **View logs of a specific service**:
  ```bash
  docker compose logs web_app
  ```
* **View real-time logs for all services**:
  ```bash
  docker compose logs -f
  ```
* **Check container statuses**:
  ```bash
  docker compose ps
  ```

---

## 🔄 Database Migrations (Alembic)

Database schema migrations are fully integrated into the Docker infrastructure via an isolated `alembic` utility service. All commands are executed within the containerized backend environment to preserve dependency consistency.

### Connecting via pgAdmin (Host Port Configuration)
If you have a local installation of PostgreSQL on your host Windows machine running on the standard port `5432`, Docker Compose is configured to route the container's internal PostgreSQL database to port **`5433`** on your host to avoid binding conflicts.

To inspect the database inside pgAdmin, register a new server with the following credentials:
* **Host**: `localhost`
* **Port**: `5433`
* **Maintenance database**: `my_database`
* **Username**: `my_user`
* **Password**: `my_password`

### Alembic Workflow Commands

> **Note**: Do not type `alembic` twice in your commands. The service container automatically routes CLI inputs straight to the Alembic engine.

* **Generate a new automatic migration script**:
  Run this command whenever you introduce or update SQLAlchemy/SQLModel ORM models inside `app/db/models`:
  ```bash
  docker compose run --rm alembic revision --autogenerate -m "describe_your_changes"
  ```
  *The resulting script is written seamlessly to your host machine's `./migrations/versions` directory via bind mounts.*

* **Apply all pending migrations to the database**:
  ```bash
  docker compose run --rm alembic upgrade head
  ```

* **Rollback the last applied migration step**:
  ```bash
  docker compose run --rm alembic downgrade -1
  ```

* **View migration historical timeline**:
  ```bash
  docker compose run --rm alembic history
  ```

* **View current revision state of the live database**:
  ```bash
  docker compose run --rm alembic current
  ```

---

## Testing

Run all tests:

```bash
pytest
```

---

## Project Structure

The project follows a modular and scalable architecture for modern FastAPI applications:

```text
QuizApp/
├── app/                  # Main application package
│   ├── core/             # Global configurations, security, and constants
│   ├── db/               # Database connection, session management, and ORM models
│   ├── routes/           # API endpoints (controllers) split by domains
│   ├── schemas/          # Pydantic models for data validation and serialization
│   ├── services/         # Core business logic and database interactions
│   ├── utils/            # Helper functions and reusable utilities
│   ├── __init__.py       # Initializes 'app' as a Python package
│   └── main.py           # Application entry point (FastAPI app initialization)
├── migrations/           # Database migration environment (Alembic)
│   ├── versions/         # Executable migration scripts
│   └── env.py            # Alembic runtime configuration script
├── tests/                # Test suite
│   ├── __init__.py       # Initializes 'tests' as a Python package
│   └── test_main.py      # Integration and unit tests for endpoints
├── .env                  # Local environment variables (ignored by git)
├── .env.sample           # Sample environment variables template
├── .gitignore            # Specifies intentionally untracked files to ignore
├── README.md             # Project documentation
└── requirements.txt      # Project dependencies
```

### Directory Overview

* **`app/core/`**: Contains global configuration files (e.g., loading `.env` variables via Pydantic), security settings, JWT authentication helpers, and project-wide constants.
* **`app/db/`**: Handles database infrastructure. Includes database engine initialization, session management setup (e.g., SQLAlchemy `get_db` dependency), and SQLAlchemy/SQLModel database models.
* **`app/routes/`**: Contains API routers (endpoints). This is where you define your HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) and map them to specific paths.
* **`app/schemas/`**: Stores Pydantic models used for Request and Response data validation. They ensure data type safety entering and leaving the API.
* **`app/services/`**: Houses the actual business logic. Routes should handle requests/responses and delegate all heavy lifting, calculations, and complex DB queries to services.
* **`app/utils/`**: Reusable independent helper scripts (e.g., date formatters, custom loggers, email senders).
* **`migrations/`**: Managed by Alembic. Contains auto-generated migration timeline scripts tracking relational database state changes.
* **`tests/`**: Contains automated tests powered by `pytest` and `Httpx` to verify the application's correctness.

### Note on `__init__.py` files
Every module folder contains an `__init__.py` file. This explicit initialization guarantees seamless absolute imports across the project (e.g., `from app.core.config import settings`) and ensures that `pytest` discovers modules correctly during test execution.

---

## Git Workflow

The project uses the following branches:

* `main` — stable production branch
* `develop` — development/integration branch
