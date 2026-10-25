# Architecture and Technical Decisions

## 1. Architecture Overview

Build one integrated College ERP web application with two independently developed modules:

- Admission Management: `admission/`
- Student Management: `student/`

Both modules will use a shared backend, database, and agreed API contracts.

The backend is responsible for business rules, validation, database integrity, admission decisions, and student registration.

## 2. Technology Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic
- psycopg
- pydantic-settings

### Database and Development Environment

- PostgreSQL 16
- Docker Compose
- Local environment variables stored in `.env`

### Collaboration

- Git
- GitHub
- Visual Studio Code

The deployment provider remains undecided.

**Implementation status:** The FastAPI foundation and database connectivity checks exist. Database models, Alembic migrations, business APIs, and frontend workflows are still pending.

## 3. Repository Structure

The intended repository structure is:

```text
College-ERP/
├── admission/
├── student/
├── shared/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── services/
│   ├── tests/
│   ├── alembic.ini
│   ├── alembic/
│   └── requirements.txt
├── docs/
│   ├── prd.md
│   ├── architecture.md
│   ├── rules.md
│   ├── phases.md
│   ├── memory.md
│   └── design.md
├── docker-compose.yml
└── README.md
```

This is the intended structure, not a claim that every listed directory or file already exists. Add directories as implementation requires.

## 4. Database Environment

PostgreSQL runs locally through Docker Compose.

Current development configuration:

- Database: `college_erp`
- Database user: `erp_user`
- Password: supplied through the local `.env` file.
- Persistent storage: Docker named volume.
- Database port: bound to localhost for local development.

Secrets must not be committed to GitHub.

The development database must use synthetic data and must not be treated as the college's production database.

## 5. Proposed Database Design

The initial relational model contains two core tables:

- `admissions`
- `students`

Authentication, user accounts, audit history, and document storage may require additional tables when their implementation scope is finalized.

### 5.1 Admissions Table

Proposed fields:

| Field | Purpose |
|---|---|
| `id` | Internal primary key |
| `application_number` | Unique application reference |
| `full_name` | Applicant's name |
| `email` | Applicant's email |
| `phone_number` | Applicant's phone number |
| `course_applied` | Course applied for |
| `branch_applied` | Branch applied for |
| `class_10_obtained_marks` | Marks obtained in Class 10 |
| `class_10_maximum_marks` | Maximum possible Class 10 marks |
| `class_10_percentage` | Class 10 percentage |
| `class_12_obtained_marks` | Marks obtained in Class 12 |
| `class_12_maximum_marks` | Maximum possible Class 12 marks |
| `class_12_percentage` | Class 12 percentage |
| `jee_applied` | Whether the applicant appeared for JEE |
| `jee_marks` | JEE score, when applicable |
| `jee_percentile` | JEE percentile, when applicable |
| `jee_rank` | JEE rank, when applicable |
| `cuet_applied` | Whether the applicant appeared for CUET |
| `cuet_marks` | CUET score, when applicable |
| `cuet_percentile` | CUET percentile, when applicable |
| `cuet_rank` | CUET rank, when applicable |
| `status` | Current application status |
| `review_remarks` | Admission review remarks |
| `reviewed_by` | Reviewer reference, pending user model |
| `reviewed_at` | Review timestamp |
| `created_at` | Creation timestamp |
| `updated_at` | Last-update timestamp |

The final SQL types, precision, nullability, and validation rules must be established when the models are implemented.

Marks, percentages, percentiles, and ranks are different values and must not be treated as interchangeable.

JEE and CUET results are optional when the applicant did not appear for the respective examination. Examination-specific rules and support for multiple attempts require confirmation before finalizing the schema.

### 5.2 Students Table

Proposed fields:

| Field | Purpose |
|---|---|
| `id` | Internal primary key |
| `student_number` | Unique internal student number |
| `enrollment_number` | Official AKTU enrollment number; nullable until assigned |
| `admission_id` | Foreign key to the originating admission |
| `full_name` | Student's name |
| `email` | Student's email |
| `phone_number` | Student's phone number |
| `course` | Registered course |
| `branch` | Registered branch |
| `current_year` | Current academic year, stored as an integer |
| `roll_number` | College roll number, nullable until assigned |
| `created_at` | Creation timestamp |
| `updated_at` | Last-update timestamp |

The internal student ID, internal student number, AKTU enrollment number, and college roll number represent different identifiers.

The application must never fabricate an official AKTU enrollment number.

### 5.3 Relationships and Constraints

The following rules must be enforced by the database wherever applicable:

1. `admissions.application_number` must be unique.
2. `students.student_number` must be unique.
3. `students.enrollment_number` must be unique when present.
4. `students.admission_id` must reference an existing admission.
5. `students.admission_id` must be unique, allowing at most one student record per admission.
6. `students.roll_number` must be unique when present.
7. Student records must not be created from nonexistent admissions.
8. Numeric marks must be validated against the applicable maximum marks.
9. Optional examination results must be represented consistently.
10. Current academic year must be a valid value for the student's programme.

PostgreSQL permits multiple `NULL` values in an ordinary unique constraint. This supports students whose AKTU enrollment number or roll number has not yet been assigned.

## 6. Admission-to-Student Registration Workflow

The intended data flow is:

```text
Applicant
   |
   v
Admission API
   |
   v
Admissions table
   |
   v
Authorized admission review
   |
   +----> Rejected
   |
   v
Approved, with applicable enrollment conditions satisfied
   |
   v
Transactional student registration
   |
   v
Students table
   |
   v
Student Management API
```

Approval and student registration are related but distinct operations.

The backend must follow the confirmed enrollment rules before creating a student record.

### Transaction and Duplicate Prevention

Student registration must:

- Use a database transaction.
- Enforce the unique admission relationship at the database level.
- Handle repeated requests safely.
- Avoid creating a second student record if the original registration already succeeded.
- Roll back incomplete database changes if registration fails.
- Return a clear result when a repeated request encounters an already-registered admission.

The precise API response behavior will be finalized in the backend API contract milestone.

## 7. Student Information Initialization

When student registration is permitted:

1. Copy the student's name, email, phone number, course, and branch from the approved admission data.
2. Create the internal student identifier according to the implemented internal numbering design.
3. Leave the AKTU enrollment number empty until the official number is assigned.
4. Leave the roll number empty until it is assigned, if applicable.
5. Initialize the academic year according to the confirmed admission process.
6. Allow authorized updates to permitted student fields.

The system must not silently invent official college numbering rules.

## 8. Academic Year Management

Store `current_year` as an integer rather than display text.

The initial application will support manual academic-year updates by authorized staff.

Automatic promotion, promotion eligibility, academic sessions, and programme-specific year rules are outside the initial implementation scope.

The applicable academic-year values must be validated against the student's programme.

## 9. Backend Foundation and Health Checks

The current backend foundation includes:

- `GET /health`: checks that the API is responding.
- `GET /health/db`: attempts a database connection and reports database availability.

The database health endpoint exists in `backend/app/main.py`. Its successful path executes a database query through `check_database_connection()`.

The health endpoint must be tested after changes to database configuration or dependencies.

## 10. Dependencies and Database Migrations

The backend dependencies must be explicitly declared in `backend/requirements.txt`.

Required libraries include:

- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic
- psycopg
- pydantic-settings
- Uvicorn
- pytest for the test environment

Verify the actual environment and compatible versions before updating the dependency file. Do not blindly replace the existing dependency list without checking how it is used.

Alembic will manage database schema migrations.

The initial migration must create the approved tables, relationships, and constraints. It must be applied to the development database and verified before the schema milestone is marked complete.

## 11. Security and Data Safety

- Use synthetic data during development and demonstrations.
- Keep credentials and tokens out of Git.
- Validate input on the backend.
- Protect admission decisions and student updates with appropriate authorization before exposing those operations.
- Restrict access to applicant and student information according to the finalized permission model.
- Do not connect to or modify the college's production systems without explicit authorization.
- Do not treat an unimplemented authorization rule as enforced security.

## 12. Existing College ERP

The existing Android ERP's source code, backend, database, and API capabilities have not been established.

The project will proceed as a standalone application using synthetic data.

Any future integration requires college authorization, technical investigation, and an agreed integration plan.

## 13. Documentation and Implementation Discipline

- `prd.md` defines product scope and requirements.
- `architecture.md` records system design and technical decisions.
- `rules.md` defines implementation and collaboration rules.
- `phases.md` is the single master milestone map.
- `memory.md` records only material project decisions.
- `design.md` is created or updated when frontend design work begins.

In the admission schema section, ensure it reflects these decisions:
- reviewed_by is deferred until a user/accounts model is designed.
- Admission statuses are submitted, under_review, approved, and rejected.
- Marks, percentages, and percentiles use numeric database types.
- Admission and student timestamps use timezone-aware date/time fields.
- The admission status and numeric range constraints are implemented in the SQLAlchemy model.
In the student schema section, add or confirm:
- students.admission_id is a required foreign key to admissions.id.
- students.admission_id is unique, so one admission can be linked to at most one student.
- student_number is required and unique.
- enrollment_number and roll_number are nullable and unique when provided.
- Automatic number generation and college-specific enrollment rules remain unresolved.
Keep any existing notes about unconfirmed college requirements.

Update relevant documentation when a material requirement, schema, workflow, API contract, or architectural decision changes.

Do not mark a feature complete until it has been implemented and verified.

## Backend API Implementation Status

The FastAPI application currently registers the following endpoints.

### Admission Management

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/admissions` | Submit an admission application |
| GET | `/api/v1/admissions` | List applications with pagination and optional status filtering |
| GET | `/api/v1/admissions/{admission_id}` | Retrieve application details |
| POST | `/api/v1/admissions/{admission_id}/approve` | Approve an application |
| POST | `/api/v1/admissions/{admission_id}/reject` | Reject an application |

Admission review endpoints are controlled by the `ENABLE_DEV_REVIEW_ENDPOINTS` configuration setting. They are intended for development and must not be treated as production-secure review workflows.

### Student Management

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/students` | List student records |
| GET | `/api/v1/students/{student_id}` | Retrieve student details |
| PATCH | `/api/v1/students/{student_id}` | Update permitted student fields |

### Health Checks

- `GET /health` checks application availability.
- `GET /health/db` checks database connectivity.

### Verification Status

The current automated test suite contains 25 passing tests using a temporary SQLite database. These tests cover admission submission and review, Student API operations, validation, health checks, and database model constraints.

PostgreSQL integration verification, authentication and authorization, and transaction-safe student registration remain outstanding. Automatic student registration following admission approval must not be assumed until the required business rules are confirmed and implemented.

### PostgreSQL Integration Tests

PostgreSQL integration tests are maintained separately from the SQLite-based unit and API tests.

Run them explicitly from the `backend/` directory:

```bash
COLLEGE_ERP_RUN_PG_TESTS=1 python -m pytest -v tests/test_postgres_integration.py

## Authentication and Authorization

### 1. Authentication Approach

The project will use JWT-based authentication for students and college
staff.

The authentication system will be implemented in the shared FastAPI
backend and will use PostgreSQL to persist user accounts.

Planned authentication components:

- User accounts with unique login identities.
- Secure password hashing; passwords must never be stored in plaintext.
- A login endpoint that verifies credentials.
- JWT access tokens issued after successful authentication.
- Backend authentication dependencies for protected API endpoints.
- Configurable token expiry and secure signing-key management.

JWT authentication is a planned architectural decision. It must not be
considered implemented until the relevant code and tests are complete.

### 2. Target Users

The authentication system must support:

- Students.
- Admission staff.
- Student-record staff.
- Other authorized college staff.
- Administrators, subject to confirmed requirements.

The exact staff roles, permissions, account-creation process, and
account-management rules require further definition.

These categories describe intended users and do not establish a
finalized college permission policy.

### 3. Authorization and Data Protection

Authentication verifies the user's identity. Authorization determines
which actions and records that user may access.

The backend must enforce authorization independently of frontend
visibility.

Planned access boundaries:

- Students may access their own permitted student information and
  services.
- Admission staff may access admission operations permitted by their
  assigned permissions.
- Student-record staff may access and update records permitted by
  their assigned permissions.
- Other staff may access only their authorized features.
- Administrative operations must be restricted to authorized accounts.

Users must not gain access to another student's private records merely
because they are authenticated.

Exact permissions must be confirmed before they are implemented.

### 4. Existing API Protection

The existing admission and student APIs must be reviewed and protected
according to the confirmed access policy.

Protection must cover, where applicable:

- Admission listing and individual admission retrieval.
- Student listing and individual student retrieval.
- Student record updates.
- Admission approval and rejection.

Public admission submission may remain available without an existing
account if that matches the approved admission workflow. Public
submission must not grant access to private admission or student data.

The development-only admission review flag is not a replacement for
authentication or authorization.

### 5. User Accounts and Data Relationships

The authentication design must establish how user accounts relate to
student records.

A student account must be linked to the correct student record so the
backend can enforce record ownership.

Staff accounts must support authorization based on the permissions
approved for the project.

The final account-to-student relationship, staff role model, and
account provisioning process must be agreed before database migrations
are created.

Do not invent official college account rules or create real college
accounts without authorization.

### 6. Security Requirements

- Store password hashes, never plaintext passwords.
- Keep JWT signing secrets outside version control.
- Reject missing, invalid, and expired tokens.
- Validate permissions on protected backend operations.
- Prevent students from accessing other students' private information.
- Avoid exposing credentials, tokens, or sensitive student information
  in logs and error responses.
- Use synthetic data during development.
- Do not connect to or modify production systems without explicit
  authorization.

### 7. Authentication Testing

Tests must verify:

- Successful login with valid credentials.
- Rejection of invalid credentials.
- Rejection of missing, malformed, invalid, and expired tokens.
- Access to protected endpoints with valid authentication.
- Denial of operations without the required permissions.
- Student record ownership restrictions.
- Appropriate protection of admission review operations.

Authentication and authorization must not be described as complete
until implementation and relevant tests have been verified.