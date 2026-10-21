
# Architecture and Technical Decisions

## 1. Architecture

Build one integrated web application with two independently developed modules:

- Admission Management
- Student Management

Both modules will be integrated after their shared interfaces and data relationships are agreed.

The application will use a shared backend, database, authentication foundation, and approved API contracts where appropriate.

## 2. Technology Stack

Frontend:
- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios

Backend:
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

Database:
- PostgreSQL 16 for standalone development.

Local database environment:
- Docker Compose.

Collaboration:
- Git
- GitHub
- Visual Studio Code

The deployment provider remains undecided.

## 3. Repository Structure

- admission/: Admission module.
- student/: Student Management module.
- shared/: Shared types, contracts, and reusable code.
- backend/app/: Backend application and business logic.
- backend/tests/: Backend tests.
- docs/: Project documentation.
- docker-compose.yml: Local database service configuration.
- README.md: Installation and execution instructions.

The internal frontend and backend organization will be finalized before feature development.

## 4. Database Development Environment

PostgreSQL runs locally through Docker Compose.

Configuration:
- Database: college_erp
- Database user: erp_user
- Database password: supplied through a local .env file.
- Persistent storage: Docker named volume.
- Port binding: localhost only.

Secrets must not be committed to GitHub.

The development database uses synthetic data and is not the college's production database.

## 5. Intended Data Flow

Applicant
-> Admission API
-> Admission application stored in database
-> Authorized document review and admission decision
-> Student creation transaction
-> Student Management API
-> Official student record within our application

The backend enforces authorization, validation, and business rules.

## 6. Integration Rules

- Agree on API contracts and data relationships before integration.
- Create student records only after approved enrollment conditions are met.
- Link every student record to its originating admission application.
- Enforce uniqueness and use database transactions where appropriate.
- Prevent duplicate student creation.
- Do not connect to production systems without authorization.

## 7. Existing College ERP

The existing Android APK is available, but its original source code,
backend, database, and API capabilities have not been established.

Standalone development will proceed using synthetic data.

Any future integration requires college authorization and technical investigation.

## 8. Mobile and Deployment

The application should support responsive desktop and mobile browsers.

PWA support may be considered later.

The deployment provider and production database architecture remain undecided.
