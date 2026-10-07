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
## Running with Docker

You can also run the application inside a Docker container. This method automatically handles all dependencies and environment variables.

### Prerequisites

* Docker Desktop installed and running

### Steps to Run

1. **Build the Docker image**:
   ```bash
   docker build -t quizapp-image .
   ```

2. **Run the container**:
   ```bash
   docker run -d --name quizapp-container -p 80:8000 quizapp-image
   ```
   *Note: This maps port 80 of your local machine to port 8000 inside the container, where Uvicorn is running.*

3. **Access the application**:
   * Main App: [http://localhost](http://localhost)
   * Swagger Documentation: [http://localhost/docs](http://localhost/docs)
   * ReDoc Documentation: [http://localhost/redoc](http://localhost/redoc)

### Managing the Container

* **View logs**:
  ```bash
  docker logs quizapp-container
  ```
* **Stop the container**:
  ```bash
  docker stop quizapp-container
  ```
* **Start the container again**:
  ```bash
  docker start quizapp-container
  ```
* **Remove the container**:
  ```bash
  docker rm -f quizapp-container
  ```


## Testing

Run all tests:

```bash
pytest
```

## Project Structure

```text
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
* **`tests/`**: Contains automated tests powered by `pytest` and `Httpx` to verify the application's correctness.

### Note on `__init__.py` files
Every module folder contains an `__init__.py` file. This explicit initialization guarantees seamless absolute imports across the project (e.g., `from app.core.config import settings`) and ensures that `pytest` discovers modules correctly during test execution.


## Git Workflow

The project uses the following branches:

* `main` — stable production branch
* `develop` — development/integration branch
* `BE-1-init-application` — branch for the initial FastAPI application

Each task should be implemented in a separate task-specific branch and merged into `develop` through a pull request.
