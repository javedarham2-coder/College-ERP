# Architecture and Technical Decisions

## 1. Architecture
Build one integrated web application with Admission and Student modules
developed in separate folders and integrated after their interfaces are agreed.

The modules will share a backend, database, authentication foundation,
and approved contracts where appropriate.

## 2. Provisional Technology Stack
- Frontend: React, TypeScript, Vite, Tailwind CSS.
- Routing and HTTP: React Router and Axios.
- Backend: Python, FastAPI, Pydantic, SQLAlchemy.
- Database: PostgreSQL for standalone development.
- Database migrations: Alembic.
- Local database environment: Docker Compose.
- Collaboration: Git and GitHub.

These choices are provisional until the foundation is verified.

## 3. Initial Repository Structure
- admission/: Admission module.
- student/: Student Management module.
- shared/: Shared types, contracts, and reusable code where appropriate.
- backend/app/: Shared backend foundation and application logic.
- backend/tests/: Backend tests.
- docs/: Project documentation.
- README.md: Setup and execution instructions.

The internal frontend and backend organization of each module will be
finalized before feature development. Avoid unnecessary duplication.

## 4. Intended Data Flow
Applicant -> Admission API -> Database
Admission review -> Authorized approval
Approval transaction -> Student record creation
Student Management -> Student API -> Database

The backend is responsible for authorization, validation, and enforcing
business rules. Frontend checks alone are not security controls.

## 5. Integration Rules
- Agree on API contracts and data relationships before module integration.
- Create student records only when approved enrollment conditions are met.
- Link each student record to its originating admission application.
- Enforce uniqueness and use transactions where appropriate.
- Prevent duplicate student creation.
- Do not connect to production systems without authorization.

## 6. Existing College ERP
The existing Android APK is available, but its original source code,
backend, database, and API capabilities have not been established.
Standalone development will proceed using synthetic data.
Any future integration requires college authorization and technical review.

## 7. Deployment and Mobile
Deployment provider is undecided.
The initial user experience should be responsive in desktop and mobile browsers.
PWA support may be considered later.
