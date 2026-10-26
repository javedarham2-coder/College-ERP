# Important Project Decisions

Record decisions that materially affect project direction or future implementation.
Do not use this file as a transcript of ordinary conversations.

## Decision 1 — Integrated Project Scope

The project contains two independently developed modules:

- Admission Management (`admission/`)
- Student Management (`student/`)

Both modules will use a shared FastAPI backend and PostgreSQL database.

## Decision 2 — Standalone Development First

The application will initially be developed as a standalone college project using synthetic data.

Integration with the existing college ERP requires explicit authorization and technical investigation.

## Decision 3 — Technology Stack

The planned stack is:

- Frontend: React, TypeScript, Vite, Tailwind CSS, React Router, Axios.
- Backend: FastAPI, Pydantic, SQLAlchemy 2.x.
- Database: PostgreSQL 16.
- Migrations: Alembic.
- PostgreSQL driver: psycopg.
- Configuration: pydantic-settings.
- Local database environment: Docker Compose.

Verify dependencies and configuration against the actual repository before implementation.

## Decision 4 — Admission Data

The proposed admission model includes:

- Unique application number.
- Applicant name, email, and phone number.
- Course and branch applied for.
- Class 10 and Class 12 obtained marks, maximum marks, and percentages.
- Independent JEE and CUET participation fields.
- Exam marks/score, percentile, and rank where applicable.
- Application status and review information.

Entrance examination results remain optional when the applicant did not appear for the respective examination.

Marks, percentages, percentiles, and ranks must be represented as distinct values.

Final mandatory fields, scoring validation, and support for multiple examination attempts must follow confirmed requirements.

## Decision 5 — Student Data and Official Identifiers

The student model includes an internal student identifier, a unique internal student number, and a link to the originating admission.

The official AKTU enrollment number is a separate field. It may remain empty until AKTU assigns the number.

The application must never fabricate an official AKTU enrollment number or present an internal identifier as an official one.

A college roll number is also a separate identifier and may remain empty until assigned.

## Decision 6 — Admission-to-Student Relationship

Each student record must reference its originating admission.

The database must enforce that one admission can create at most one student record.

Student registration must be transactional and safe against repeated requests so that retries cannot create duplicate student records.

Admission approval and student registration are separate steps. Student creation must follow the applicable enrollment conditions confirmed by the college.

## Decision 7 — Student Contact Information

When a student record is created, the student's name, email, phone number, course, and branch should initially be copied from the admission data.

Authorized staff may update permitted student information later.

## Decision 8 — Academic Year

The current academic year is stored as an integer.

Academic-year updates will be manual in the initial version.

Automatic promotion is outside the initial scope and requires additional academic-year and promotion rules.

## Decision 9 — Database Integrity and Migrations

Use SQLAlchemy for database models and Alembic for schema migrations.

The database should enforce:

- Unique application numbers.
- Unique internal student numbers.
- Unique AKTU enrollment numbers when assigned.
- Unique roll numbers when assigned.
- Valid foreign-key relationships.
- At most one student record per admission.

Database models and migrations must be applied and tested before the schema milestone is marked complete.

## Decision 10 — Documentation Discipline

Maintain the following project documents:

- `prd.md`: product scope and requirements.
- `architecture.md`: architecture, data relationships, and technical design.
- `rules.md`: implementation and collaboration rules.
- `phases.md`: single master milestone map.
- `memory.md`: material project decisions.
- `design.md`: frontend design decisions when frontend work begins.

Update relevant documents when important requirements, schemas, workflows, API contracts, or architectural decisions change.

## Decision 11 — Data Safety

- Use synthetic data during development and demonstrations.
- Never commit `.env`, credentials, tokens, or virtual environments.
- Do not modify production systems without explicit authorization.
- Do not claim that a feature is complete until its behavior has been implemented and verified.

- Admission statuses for the initial schema are submitted, under_review, approved, and rejected.
- reviewed_by is deferred until the user/accounts model is designed.
- The Student model references Admission through a unique foreign key.
- Number-generation formats and college-specific enrollment rules remain unresolved.
Avoid duplicating the full schema or adding a transcript of this conversation.

## Decision 12 — Initial Authentication and Authorization

- Use JWT bearer tokens to authenticate users of the shared FastAPI backend.
- Store user accounts in the database and hash passwords securely; never store plaintext passwords.
- The initial application roles are `admin`, `admission_staff`, and `student`.
- Staff accounts are provisioned through a backend CLI. Public staff registration is not supported.
- Admission submission remains public, while admission listing and detail retrieval require staff authentication.
- Admission approval and rejection require staff authorization and the development review-endpoints flag.
- Student listing requires staff authorization.
- Students may access only their own linked student record and may update only permitted contact fields.
- Student account provisioning is deferred until the account-to-student linking workflow is defined.
- JWT signing secrets and database credentials must remain outside version control.
- Authentication and authorization are not considered complete until the relevant tests and end-to-end workflows are verified.

These are the initial implementation decisions. Any future change to roles, permissions, or account-linking behavior must be reflected in the architecture and relevant tests.
