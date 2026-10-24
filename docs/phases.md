# College ERP — Master Milestone Map

> **Purpose:** This file defines the project plan and maintains a chronological record of development progress.
>
> **Progress update rule:** For routine progress updates, add a new dated entry under `## Progress Log` at the end of this file. Do not rewrite earlier log entries or repeatedly edit the project plan.
>
> **Source of truth:** The most recent progress-log entry determines the latest reported status, blockers, and next action. Verify the actual code, tests, database, and Git state before reporting anything as complete.

---

## 1. Project Goal

Build one database-backed College ERP application with two independently developed modules:

- `admission/` — Admission Management
- `student/` — Student Management

Both modules will use one shared FastAPI backend and PostgreSQL database.

### Core Workflow

Applicant submits an application → authorized admission staff review it → application is approved or rejected → applicable enrollment conditions are satisfied → backend creates at most one linked student record → student appears in Student Management.

The project will remain standalone unless the college provides explicit authorization and the technical information required for integration with its existing ERP.

---

## 2. Project Structure and Technology

### Planned Technology Stack

| Component | Technology |
|---|---|
| Admission frontend | React, TypeScript, Vite, Tailwind CSS |
| Student frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend | FastAPI, Python, Pydantic |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL 16 |
| Database migrations | Alembic |
| Backend testing | pytest |
| Local database environment | Docker Compose |

### Main Project Areas

- `admission/` — Admission Management frontend and module-specific code.
- `student/` — Student Management frontend and module-specific code.
- `backend/` — Shared API, configuration, database connection, models, migrations, and tests.
- `docs/` — Requirements, architecture, coding rules, design, milestone tracking, and material project decisions.

Actual folder contents must be verified before assuming every planned component exists.

---

## 3. Development Rules

1. Read the relevant documentation and existing code before significant changes.
2. Work in small, ordered steps and verify each step before moving forward.
3. Keep Admission Management and Student Management independently developed.
4. Use agreed interfaces when integrating the two modules.
5. The backend and database own business rules and data integrity.
6. Do not invent college-specific requirements, policies, permissions, or official identifiers.
7. Never fabricate official enrollment numbers or roll numbers.
8. Test actual behavior before marking a feature complete.
9. Update the relevant documentation when an implementation or important decision changes.
10. Append routine progress updates to the end of this file.
11. Each teammate must record their completed milestones, blockers, and next steps.
12. Review Git status and diffs before committing.
13. Commit related code, tests, configuration, and documentation together.
14. Never commit `.env`, credentials, tokens, virtual environments, or other secrets.
15. Keep `docs/memory.md` focused on material decisions, not ordinary conversation.
16. Do not mark an entire milestone complete if its exit criteria have not been satisfied.

---

## 4. Status Definitions

- **COMPLETE:** All milestone exit criteria have been satisfied and verified.
- **IN PROGRESS:** Work has started but exit criteria remain.
- **NEXT:** The immediate priority.
- **PLANNED:** Work has not started.
- **BLOCKED:** Progress depends on an unresolved decision, permission, or dependency.

A UI, written plan, generated migration, or untested implementation alone is not evidence that a feature is complete.

---

## 5. Product Requirements and Design Decisions

### 5.1 Admission Management

The proposed admission record includes:

- Application number.
- Applicant's full name and contact information.
- Course applied for and branch applied for.
- Class 10 obtained marks, maximum marks, and percentage.
- Class 12 obtained marks, maximum marks, and percentage.
- Independent JEE and CUET participation fields.
- Examination marks or scores, percentile, and rank where applicable.
- Application status and review information.
- Creation and last-update timestamps.

Exam-specific results remain optional when the applicant did not appear for that examination.

Exam scoring formats, multiple-attempt support, mandatory fields, and eligibility criteria require confirmation before their business rules are implemented.

### 5.2 Student Management

The proposed student record includes:

- Internal student ID.
- Unique internal student number.
- Official AKTU enrollment number, nullable until assigned.
- Link to the originating admission.
- Full name and contact information.
- Registered course and branch.
- Current academic year.
- Optional college roll number.
- Creation and last-update timestamps.

Student contact details initially copy from admission data. Authorized updates will be supported.

Academic-year updates will be manual in the initial version.

### 5.3 Data Integrity Rules

- Application numbers must be unique.
- Internal student numbers must be unique.
- AKTU enrollment numbers must be unique when assigned.
- Roll numbers must be unique when assigned.
- Each student must reference an existing admission.
- One admission can create at most one student record.
- Student registration must be transactional and safe against repeated requests.
- Official college identifiers must never be fabricated.

### 5.4 Requirements Requiring Confirmation

Do not invent college policies about:

- Mandatory fields and documents.
- Eligibility and admission rules.
- Entrance examination scoring and multiple attempts.
- Final enrollment conditions.
- Official enrollment-number and roll-number assignment.
- User permissions and authentication.
- Data retention and deployment.
- Any additional rules that depend on the college's actual processes.

Record important confirmed decisions in `docs/memory.md` and update the relevant requirements or architecture document when necessary.

---

## 6. Milestone Plan

Milestone statuses below represent the baseline plan. For the latest reported progress, consult the final entry in the Progress Log.

### Milestone 1 — Repository and Project Rules

**Baseline status: COMPLETE**

- [x] Establish the repository and VS Code workspace.
- [x] Establish independent Admission and Student module areas.
- [x] Establish backend, test, shared, and documentation areas.
- [x] Create initial project documentation.
- [x] Agree that the backend and database own the business workflow.

**Exit criteria:** Repository structure and foundational project documentation exist.

### Milestone 2 — Local Database Environment

**Baseline status: COMPLETE — previously verified**

- [x] Configure Docker and Docker Compose.
- [x] Run PostgreSQL 16.
- [x] Establish the `college_erp` database and `erp_user`.
- [x] Verify database connectivity.

**Exit criteria:** The local PostgreSQL development environment is operational.

**Note:** Recheck connectivity if database configuration or the development environment changes.

### Milestone 3 — FastAPI and Database Connectivity

**Baseline status: COMPLETE — previously verified**

- [x] Establish the backend virtual environment.
- [x] Implement `GET /health`.
- [x] Configure environment-based settings.
- [x] Establish SQLAlchemy engine and session setup.
- [x] Implement `GET /health/db`.

**Exit criteria:** The backend starts and its health-check endpoints behave as expected.

**Note:** Rerun relevant tests after changes to configuration, dependencies, or database connectivity.

### Milestone 4 — Automated Health Tests and Git Verification

**Baseline status: COMPLETE — previously verified**

- [x] Test the normal health endpoint.
- [x] Test the connected database-health path.
- [x] Test simulated database unavailability.

**Previously reported evidence:** Three health tests passed.

**Exit criteria:** Health-check behavior is covered by automated tests, and relevant changes are reviewed before committing.

### Milestone 5 — Database Schema and Migrations

**Baseline status: IN PROGRESS**

#### Requirements and Design

- [x] Review the PRD, architecture, existing backend files, and milestone map.
- [x] Establish the proposed admission fields.
- [x] Establish the proposed student fields.
- [x] Agree that academic-year updates will initially be manual.
- [x] Agree that official enrollment numbers must not be fabricated.
- [x] Agree that an admission may create at most one student record.

#### Implementation

- [x] Implement SQLAlchemy admission and student models.
- [x] Configure Alembic.
- [x] Create the initial Alembic migration.
- [x] Apply the initial migration to the development PostgreSQL database.
- [x] Verify the created tables and relevant relationships and constraints.
- [x] Add model metadata tests.

**Previously reported evidence:**

- Initial migration: `342bf7c85b9f`
- Migration status: `342bf7c85b9f (head)`
- Tables verified: `admissions`, `students`, and `alembic_version`
- Student-to-admission foreign key verified.
- Unique student-to-admission relationship verified.
- Relevant uniqueness and numeric validation constraints inspected.
- Latest reported test result: **9 tests passed**.

These results must be rechecked if the relevant implementation changes.

#### Remaining Work

- [ ] Review backend dependency changes.
- [ ] Review `docs/architecture.md` and `docs/memory.md` against the actual implementation.
- [ ] Confirm any remaining college-specific requirements without inventing policies.
- [ ] Review the complete Git diff and verify that no secrets or unintended files are included.
- [ ] Rerun relevant tests and confirm their results.
- [ ] Commit the verified code and documentation together.

**Exit criteria:** The migration applies successfully, the resulting schema is verified, relevant tests pass, and the documentation accurately reflects the implementation.

### Milestone 6 — Backend API Contracts and Implementation

**Baseline status: PLANNED**

- [ ] Define request and response schemas.
- [ ] Define validation rules, status codes, and error responses.
- [ ] Define permitted admission-status transitions.
- [ ] Implement admission submission.
- [ ] Implement admission listing and detail retrieval.
- [ ] Implement authorized admission review, approval, and rejection.
- [ ] Implement student listing and detail retrieval.
- [ ] Implement permitted student updates.
- [ ] Implement transaction-safe, retry-safe student registration.
- [ ] Add automated API and database tests.
- [ ] Document finalized API contracts for both module owners.

**Candidate routes — proposals, not finalized:**

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

These routes must be reviewed before being treated as the final API contract.

**Exit criteria:** The documented and tested APIs operate against PostgreSQL and are ready for frontend integration.

### Milestone 7 — Independent Admission and Student Frontends

**Baseline status: PLANNED**

#### Admission Module

- [ ] Build the application form and client-side validation.
- [ ] Display admission applications and their details.
- [ ] Display academic marks and entrance examination information.
- [ ] Build the admission review and status interface.
- [ ] Connect approval and rejection actions to the backend.

#### Student Module

- [ ] Build the student directory.
- [ ] Add search and filtering.
- [ ] Build student profile and details views.
- [ ] Display course, branch, academic year, and enrollment information.
- [ ] Implement permitted student updates.
- [ ] Connect to the agreed student APIs.

#### Shared Frontend Work

- [ ] Create or update `docs/design.md` when frontend design starts.
- [ ] Replace temporary mock data with real API data.
- [ ] Implement loading, validation, empty, and error states.

**Exit criteria:** Both modules work independently, use their agreed contracts, and document their limitations and blockers.

### Milestone 8 — End-to-End Integration

**Baseline status: PLANNED**

- [ ] Connect both frontends to the shared FastAPI backend.
- [ ] Verify loading states, validation, and error handling.
- [ ] Submit an admission application and retrieve it.
- [ ] Review and approve or reject the application through the authorized workflow.
- [ ] Verify that student creation follows confirmed enrollment conditions.
- [ ] Verify that repeated registration requests do not create duplicate students.
- [ ] Verify that each student references the originating admission.
- [ ] Verify that the student appears in Student Management.
- [ ] Test transaction rollback and relevant database failures.
- [ ] Update architecture and API documentation if implementation differs from the agreed design.

**Exit criteria:** The complete admission-to-student workflow succeeds against the development database through real API calls, not just mock data.

### Milestone 9 — Security, Reliability, and Regression Testing

**Baseline status: PLANNED**

- [ ] Test valid and invalid admission submissions.
- [ ] Test missing fields and invalid marks.
- [ ] Test optional JEE/CUET results and applicable scoring validations.
- [ ] Test invalid admission-status transitions.
- [ ] Test repeated approval and registration requests.
- [ ] Test database failure and transaction rollback.
- [ ] Implement and test appropriate authentication and role-based authorization.
- [ ] Verify access controls for admission decisions and student updates.
- [ ] Run the full test suite.
- [ ] Record known limitations and unresolved risks.

**Exit criteria:** Critical workflows and failure paths have been tested, and known limitations are documented.

### Milestone 10 — Setup, Demo, and Delivery

**Baseline status: PLANNED**

- [ ] Prepare synthetic demonstration data.
- [ ] Verify that secrets remain outside Git.
- [ ] Verify clean setup, application startup, database migrations, and tests.
- [ ] Update `README.md` with prerequisites, setup, run, migration, and test instructions.
- [ ] Rehearse a short end-to-end demonstration.
- [ ] Verify Git status, documentation, and known limitations.
- [ ] Deploy only if time, hosting, and security requirements permit.

**Exit criteria:** A teammate can set up and run the project using the documentation, and the demonstration shows the real working workflow.

---

## 7. Documentation Responsibilities

Update only the documents affected by a change.

| Document | Responsibility |
|---|---|
| `docs/prd.md` | Product scope, users, requirements, and features |
| `docs/architecture.md` | System structure, technology, database design, and module integration |
| `docs/rules.md` | Team coding rules and implementation practices |
| `docs/phases.md` | Milestone plan and append-only progress history |
| `docs/memory.md` | Material project decisions and confirmed constraints |
| `docs/design.md` | Frontend design decisions, when frontend work begins |
| `README.md` | Prerequisites, setup, execution, migration, testing, and delivery instructions |

Do not change a document simply to record ordinary conversation. Record decisions that materially affect the project.

---

## 8. Git and Verification Rules

Before committing:

1. Check the current branch and Git status.
2. Review the diffs of all modified and newly created files.
3. Confirm that relevant tests pass.
4. Confirm that documentation reflects the actual implementation.
5. Confirm that `.env`, credentials, tokens, virtual environments, and other secrets are excluded.
6. Stage only the intended files.
7. Commit related implementation, tests, and documentation together.
8. Verify the resulting commit and working-tree status.
9. Push only after confirming the intended commit.

Do not claim a commit or push succeeded until the command output confirms it.

---

# Progress Log

> **Append-only section:** Add every new progress entry below the previous entry. Never delete or rewrite historical entries during routine updates.
>
> Each entry should record the date, milestone, status, completed work, verification evidence, blockers, and next action. Use `Not checked` or `None reported` where appropriate rather than guessing.

## Entry 001 — 2026-10-24

**Milestone:** Milestone 5 — Database Schema and Migrations

**Status:** IN PROGRESS

### Completed and Reported

- SQLAlchemy admission and student models implemented.
- Alembic configured.
- Initial migration `342bf7c85b9f` generated and applied.
- Database tables and relevant constraints inspected.
- Model metadata tests added.

### Verification Evidence

- `alembic current` reported `342bf7c85b9f (head)`.
- Tables `admissions`, `students`, and `alembic_version` were verified.
- Student-to-admission foreign key and uniqueness constraints were inspected.
- Latest reported test result: **9 passed**.

### Documentation and Git State

- `backend/requirements.txt` has reported changes.
- `backend/alembic.ini` and the `backend/alembic/` migration files have reported changes.
- `backend/app/models/` has reported new files.
- `docs/architecture.md` and `docs/memory.md` have reported changes.
- Final diffs, staging state, and secret exclusion still require verification.
- `docs/phases.md` is being updated to use this append-only progress format.

### Blockers and Unresolved Items

- Any remaining college-specific requirements must be confirmed rather than assumed.
- Final dependency, documentation, test, and Git review is pending.

### Next Action

Review the updated documentation and Git changes, rerun relevant tests, and commit the verified Milestone 5 implementation and documentation together.

---

## Template for Future Progress Entries

Copy this template and append it after the latest entry whenever work progresses.

```markdown
## Entry XXX — YYYY-MM-DD

**Milestone:** Milestone number and name

**Status:** IN PROGRESS / COMPLETE / BLOCKED

### Completed Work
- Describe the work actually completed.

### Verification Evidence
- Tests run and their results.
- Database, API, or UI behavior verified.
- Commit ID, if committed.

### Documentation and Git State
- Documents updated.
- Relevant files changed.
- Commit/push status, if applicable.

### Blockers and Unresolved Items
- Confirmed blockers, unresolved decisions, or `None reported`.

### Next Action
- State exactly the next action.
```

**Important:** A new entry records progress; it does not automatically make a milestone complete. Verify the milestone's exit criteria before reporting completion.

### Milestone 6 Progress Update — 24 October 2026

**Completed and tested**
- Registered Admission and Student routers in the FastAPI application.
- Implemented admission submission, listing, and detail retrieval.
- Implemented development-gated admission approval and rejection.
- Implemented student listing, detail retrieval, and permitted updates.
- Added API tests covering admission review and Student API behavior.
- Verified that all 25 automated tests pass using a temporary SQLite database.
- Verified that the expected API routes are registered.

**Outstanding**
- Verify the implementation against PostgreSQL.
- Finalize and document API request/response contracts and error behavior.
- Implement and test authentication and role-based authorization before treating protected workflows as production-ready.
- Confirm official student-number and academic-year rules.
- Implement and test transaction-safe, retry-safe student registration.
- Complete end-to-end integration testing.

**Current status:** Milestone 6 is in progress. Passing SQLite tests and registering routes do not satisfy all milestone exit criteria.
