# College ERP — Master Milestone Map

> This is the single source of truth for project progress, blockers, and the next action.
>
> **Status meanings**
> - `COMPLETE`: Implemented and verified.
> - `IN PROGRESS`: Work is actively underway.
> - `NEXT`: Immediate priority.
> - `PLANNED`: Not started.
> - `BLOCKED`: Waiting for a decision or dependency.
>
> A visible UI, written plan, or untested code does not qualify as complete.

## Project Goal

Build one database-backed College ERP application with two independently developed modules:

- `admission/` — Admission Management
- `student/` — Student Management

Both modules will use one shared FastAPI backend and PostgreSQL database.

**Core workflow:** Applicant submits an application → authorized admission staff review it → the application is approved or rejected → applicable enrollment conditions are satisfied → the backend creates at most one linked student record → the student appears in Student Management.

The project will remain standalone unless the college provides explicit authorization and the technical information required for integration with its existing ERP.

## Current Project Snapshot

- **Repository:** `College-ERP`
- **Git branch:** `main`
- **Frontend plan:** React, TypeScript, Vite, Tailwind CSS, React Router, Axios.
- **Backend:** FastAPI and Pydantic foundation exists.
- **Database:** PostgreSQL 16 through Docker Compose.
- **ORM:** SQLAlchemy 2.x is used by the existing database connection code.
- **Migrations:** Alembic setup remains pending.
- **Tests:** The last reported backend test run passed all 3 health tests.
- **Current milestone:** Milestone 5 — database schema and migrations.
- **Next action:** Reconcile backend dependencies, finalize the schema implementation details, configure Alembic, and implement the initial migration.

Recheck Git status and test results before committing further changes.

## Agreed Requirements and Design Decisions

### Admission Management

The proposed admission record includes:

- Application number and applicant contact information.
- Course applied for and branch applied for.
- Class 10 obtained marks, maximum marks, and percentage.
- Class 12 obtained marks, maximum marks, and percentage.
- Independent JEE and CUET participation fields.
- Exam marks/score, percentile, and rank where applicable.
- Application status and review information.
- Creation and last-update timestamps.

Exam-specific results remain optional when the applicant did not appear for that examination. Exam scoring formats and multiple-attempt support require validation before implementation.

### Student Management

The proposed student record includes:

- Internal student ID and unique internal student number.
- Official AKTU enrollment number, nullable until assigned.
- Link to the originating admission.
- Full name, email, and phone number.
- Registered course and branch.
- Current academic year.
- Optional college roll number.
- Creation and last-update timestamps.

Student contact details initially copy from admission data. Authorized updates will be supported.

Academic-year updates will be manual in the initial version.

### Integrity Rules

- Application numbers must be unique.
- Internal student numbers must be unique.
- AKTU enrollment numbers must be unique when assigned.
- Roll numbers must be unique when assigned.
- Each student must reference an existing admission.
- One admission can create at most one student record.
- Registration must be transactional and safe against repeated requests.
- Official college identifiers must never be fabricated.

### Requirements Still Requiring Confirmation

Do not invent college policies about:

- Mandatory fields and documents.
- Eligibility and admission rules.
- Entrance examination result formats and multiple attempts.
- Final enrollment conditions.
- Official enrollment-number and roll-number assignment.
- User permissions and authentication.
- Data retention and deployment.

## Milestone 1 — Repository and Project Rules

**Status: COMPLETE**

- [x] Establish the repository and VS Code workspace.
- [x] Establish the independent admission and student module folders.
- [x] Establish backend, test, shared, and documentation areas.
- [x] Create the initial project documentation.
- [x] Agree that the backend and database own the business workflow.

**Evidence:** Initial repository and project documentation exist.

## Milestone 2 — Local Database Environment

**Status: COMPLETE — previously reported**

- [x] Configure Docker and Docker Compose.
- [x] Run PostgreSQL 16.
- [x] Establish the `college_erp` database and `erp_user`.
- [x] Verify database connectivity.

**Evidence:** PostgreSQL and the development database connection were reported working. Recheck if environment changes affect connectivity.

## Milestone 3 — FastAPI and Database Connectivity

**Status: COMPLETE — previously reported**

- [x] Establish the backend virtual environment.
- [x] Implement `GET /health`.
- [x] Configure environment-based settings.
- [x] Create SQLAlchemy engine/session setup.
- [x] Implement `GET /health/db`.

**Follow-up:** Reconcile imports with `backend/requirements.txt`. The previous inspection found SQLAlchemy and `pydantic-settings` imports that were not declared in the requirements file.

## Milestone 4 — Automated Health Tests and Git Verification

**Status: COMPLETE — recheck after relevant changes**

- [x] Test the normal health endpoint.
- [x] Test the connected database-health path.
- [x] Test simulated database unavailability.
- [x] Previously reported result: 3 tests passed.

**Test command:**

```bash
cd backend && python -m pytest -v
```

**Rule:** Rerun the relevant tests after modifying database configuration, dependencies, or health-check behavior.

## Milestone 5 — Requirements and Database Schema

**Status: IN PROGRESS**

### Requirements and Design

- [x] Review the PRD, architecture, current backend files, and milestone map.
- [x] Agree on the proposed admission fields, including course, branch, Class 10/12 marks, and JEE/CUET results.
- [x] Agree on the proposed student fields, including course, branch, year, contact information, and AKTU enrollment number.
- [x] Agree that academic-year updates will initially be manual.
- [x] Agree that official AKTU enrollment numbers must not be fabricated.
- [x] Agree that an admission may create at most one student record.
- [ ] Confirm any remaining college-specific requirements before finalizing implementation details.
- [ ] Finalize field types, nullability, numeric precision, and validation constraints.

### Implementation

- [ ] Reconcile and update backend dependencies.
- [ ] Configure Alembic.
- [ ] Implement SQLAlchemy admission and student models.
- [ ] Create the initial Alembic migration.
- [ ] Apply the migration to the development PostgreSQL database.
- [ ] Verify tables, relationships, and constraints.
- [ ] Add relevant automated database tests.
- [ ] Update the affected documentation with the implemented design and test evidence.
- [ ] Commit code and documentation together after reviewing Git status and the diff.

**Exit criteria:** The migration applies successfully, the resulting database schema is verified, relevant tests pass, and documentation reflects the actual implementation.

## Milestone 6 — Backend API Contracts and Implementation

**Status: PLANNED**

- [ ] Define request and response schemas.
- [ ] Agree on validation, status codes, error responses, and permitted status transitions.
- [ ] Implement admission submission, listing, and detail retrieval.
- [ ] Implement authorized admission review, approval, and rejection.
- [ ] Implement student listing, detail retrieval, and permitted updates.
- [ ] Implement transaction-safe, retry-safe student registration.
- [ ] Add automated API and database tests.
- [ ] Document the finalized API contracts for both module owners.

**Candidate routes — proposals, not yet implemented:**

```text
POST  /api/v1/admissions
GET   /api/v1/admissions
GET   /api/v1/admissions/{id}
POST  /api/v1/admissions/{id}/approve
POST  /api/v1/admissions/{id}/reject
GET   /api/v1/students
GET   /api/v1/students/{id}
PATCH /api/v1/students/{id}
```

Review these routes before treating them as the final API contract.

**Exit criteria:** The documented and tested APIs operate against PostgreSQL and are ready for frontend integration.

## Milestone 7 — Independent Admission and Student Frontends

**Status: PLANNED**

### Admission Module

- [ ] Build the application form and client-side validation.
- [ ] Display admission applications and their details.
- [ ] Display academic marks and entrance examination information.
- [ ] Build the admission review and status interface.
- [ ] Connect approval and rejection actions to the backend.

### Student Module

- [ ] Build the student directory.
- [ ] Add search and filtering.
- [ ] Build student profile and details views.
- [ ] Display course, branch, academic year, and enrollment information.
- [ ] Implement permitted student updates.
- [ ] Connect to the agreed student APIs.

Additional tasks:

- [ ] Create or update `docs/design.md` when frontend design starts.
- [ ] Replace temporary mock data with real API data before declaring the integrated workflow complete.

**Exit criteria:** Each module works independently, uses its agreed contracts, and has documented limitations and blockers.

## Milestone 8 — End-to-End Integration

**Status: PLANNED**

- [ ] Connect both frontends to the shared FastAPI backend.
- [ ] Verify loading states, validation, and error handling.
- [ ] Submit an admission application and retrieve it.
- [ ] Review and approve/reject the application through the authorized workflow.
- [ ] Verify that student creation follows confirmed enrollment conditions.
- [ ] Verify that repeated registration requests do not create duplicate students.
- [ ] Verify that the student references the originating admission.
- [ ] Verify that the student appears in Student Management.
- [ ] Test transaction rollback and relevant database failures.
- [ ] Update architecture and API documentation if implementation differs from the agreed design.

**Exit criteria:** The complete admission-to-student workflow succeeds against the development database using real API calls, not just mock data.

## Milestone 9 — Security, Reliability, and Regression Testing

**Status: PLANNED**

- [ ] Test valid and invalid admission submissions.
- [ ] Test missing fields and invalid marks.
- [ ] Test optional JEE/CUET results and applicable scoring validations.
- [ ] Test invalid admission status transitions.
- [ ] Test repeated approval and registration requests.
- [ ] Test database failure and transaction rollback.
- [ ] Implement and test appropriate authentication and role-based authorization.
- [ ] Verify access controls for admission decisions and student updates.
- [ ] Run the full test suite.
- [ ] Record known limitations and unresolved risks.

**Exit criteria:** Critical workflows and failure paths have been tested, and known limitations are documented.

## Milestone 10 — Setup, Demo, and Delivery

**Status: PLANNED**

- [ ] Prepare synthetic demonstration data.
- [ ] Verify that secrets remain outside Git.
- [ ] Verify clean setup, application startup, and database migrations.
- [ ] Update `README.md` with prerequisites, setup, run, migration, and test instructions.
- [ ] Rehearse a short end-to-end demonstration.
- [ ] Verify Git status, documentation, and known limitations.
- [ ] Deploy only if time, hosting, and security requirements permit.

**Exit criteria:** A teammate can set up and run the project using the documentation, and the demonstration shows the real working workflow.

## Working Rules

1. Read relevant documentation and source files before significant changes.
2. Make small, ordered changes and explain their purpose.
3. Verify behavior before marking work complete.
4. Update this master map after milestone verification or material plan changes.
5. Update the relevant PRD, architecture, rules, design, or memory documentation when necessary.
6. Keep `phases.md` as the single master progress map.
7. Record material decisions in `memory.md`, not ordinary conversation.
8. Review Git status and diffs before committing.
9. Commit relevant code and documentation together.
10. Never commit `.env`, credentials, tokens, or virtual environments.
11. Do not invent college policies or official identifiers.
12. Record completed work, tests, blockers, and next steps honestly.

## Immediate Next Action

Continue Milestone 5 by reconciling backend dependencies, finalizing the schema's implementation details, and setting up Alembic before creating and testing the initial migration.