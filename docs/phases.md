# College ERP --- Master Milestone Map

> **Purpose:** This is the single source of truth for project progress
> and the next action. Update this file whenever a milestone is
> verified, a blocker changes the plan, or an important
> route/architecture decision changes.
>
> **Status meanings:** `COMPLETE` = implemented and verified;
> `IN PROGRESS` = actively being built; `NEXT` = immediate priority;
> `PLANNED` = not started; `BLOCKED` = waiting for a decision or
> dependency. A screen or code file alone does not make a feature
> complete.

## Project Goal

Build one database-backed College ERP application with two independently
developed modules---**Admission Management** (`admission/`) and
**Student Management** (`student/`)---connected through one shared
**FastAPI backend** and **PostgreSQL database**.

**Core workflow:** Applicant submits an application → authorized
admission staff review it → application is approved or rejected → an
approved admission creates exactly one linked student record under the
college-approved registration rules → the student appears in Student
Management.

**Important boundary:** We are building a standalone project unless the
college later provides explicit authorization, source code, API access,
and requirements for integration with its existing ERP.

## Current Project Snapshot

-   **Repository:** `College-ERP`; one GitHub repository and one VS Code
    workspace.
-   **Frontend plan:** React, TypeScript, Vite, Tailwind CSS, React
    Router, Axios.
-   **Backend plan/current foundation:** Python, FastAPI, Pydantic;
    SQLAlchemy 2.x, Alembic, psycopg and pydantic-settings are
    planned/expected but must be checked against the actual requirements
    and files before schema work.
-   **Database:** PostgreSQL 16 in Docker Compose; database
    `college_erp`, user `erp_user`.
-   **Last reported Git state:** `main` synced with `origin/main`,
    working tree clean; HEAD was `25ce785` (`requirement updated`).
    Recheck Git before the next commit.
-   **Current scope:** Backend foundation and health checks only.
    Admission/student models, business APIs, frontend workflows,
    authentication, end-to-end integration and deployment are not
    complete.

## Milestone 1 --- Repository and Project Rules

**Status: COMPLETE**

-   [x] Create/connect the GitHub repository and VS Code workspace.
-   [x] Establish separate `admission/` and `student/` module folders.
-   [x] Establish shared/backend/test/documentation folders.
-   [x] Create the initial product, architecture and coding/team rules
    documents.
-   [x] Agree that backend and database---not frontend mock data---own
    the business workflow.

**Completion evidence:** Repository and initial documentation were
established. Preserve the existing structure unless an inspected need
justifies changing it.

## Milestone 2 --- Local Database Environment

**Status: COMPLETE**

-   [x] Verify Docker and Docker Compose.
-   [x] Run PostgreSQL 16 in Docker.
-   [x] Verify database `college_erp` and database user `erp_user`.
-   [x] Confirm the database container is healthy and a database query
    succeeds.

**Completion evidence:** PostgreSQL and its local development connection
were reported working.

## Milestone 3 --- FastAPI and Database Connectivity Foundation

**Status: COMPLETE**

-   [x] Create the backend virtual environment and install the initial
    dependencies.
-   [x] Implement `backend/app/main.py` and `GET /health`.
-   [x] Confirm interactive API documentation at `/docs`.
-   [x] Add environment-based settings in `backend/app/config.py`.
-   [x] Add SQLAlchemy engine/session setup in
    `backend/app/database.py`.
-   [x] Implement `GET /health/db` and verify a real PostgreSQL
    connection.

**Follow-up check:** Reconcile the actual `backend/requirements.txt`
with the imports and planned stack. Earlier inspection did not show
SQLAlchemy, Alembic, psycopg or pydantic-settings in that file, and no
Alembic configuration was found under `backend/`. Do not assume those
pieces exist until verified.

## Milestone 4 --- Automated Health Tests and Git Verification

**Status: COMPLETE --- recheck before the next change**

-   [x] Test the normal health endpoint.
-   [x] Test the connected database-health path.
-   [x] Test simulated database unavailability.
-   [x] Latest reported result: **3 tests passed**.
-   [x] Test command: `cd backend && python -m pytest -v`.
-   [x] Latest reported Git state showed a clean working tree and `main`
    synced with `origin/main`; test commit `00813b0` was in history.

**Rule:** Run the tests again after changes that affect backend
configuration, database setup or health behavior.

## Milestone 5 --- Confirm Requirements and Design the Database

**Status: NEXT**

**Goal:** Agree on the minimum correct data model before writing
migrations or business APIs.

-   [ ] Recheck `docs/prd.md`, `docs/architecture.md`, `docs/rules.md`,
    current source files, dependencies and Git status.
-   [ ] Reconcile the architecture document's database-health wording
    with the implemented `/health/db` behavior.
-   [ ] Confirm required applicant, admission and student fields with
    the team/college; mark unknown college policies as unresolved rather
    than guessing.
-   [ ] Define admission statuses and valid transitions, including who
    is allowed to approve/reject.
-   [ ] Decide student-number and optional roll-number generation rules
    only after confirming college requirements.
-   [ ] Define relationships and constraints: unique application number;
    unique student number; one student per originating admission;
    optional roll number unique when assigned.
-   [ ] Define the approval/registration transaction and behavior on
    retries, failures and duplicate requests.
-   [ ] Confirm SQLAlchemy/Alembic/driver/settings dependencies and
    configure Alembic.
-   [ ] Create SQLAlchemy models, generate an initial migration, apply
    it to the development database and verify the resulting schema.
-   [ ] Add/update only the relevant documentation in the same
    milestone.

**Exit criteria:** The schema is documented, migration applies
successfully, database tables/constraints are verified, and automated
checks pass.

## Milestone 6 --- Backend API Contracts and Implementation

**Status: PLANNED**

-   [ ] Agree on request/response schemas, status codes, validation
    rules and error format before frontend integration.
-   [ ] Implement admission submission, listing and detail retrieval.
-   [ ] Implement admission review, approval and rejection.
-   [ ] Implement student listing, detail retrieval and permitted
    updates.
-   [ ] Keep validation, authorization, status transitions and student
    creation in the backend.
-   [ ] Make approval/registration transactional and retry-safe so one
    admission cannot create duplicate students.
-   [ ] Add automated API and database tests.

**Candidate routes (proposals only; not implemented until confirmed):**

``` text
POST  /api/v1/admissions
GET   /api/v1/admissions
GET   /api/v1/admissions/{id}
POST  /api/v1/admissions/{id}/approve
POST  /api/v1/admissions/{id}/reject
GET   /api/v1/students
GET   /api/v1/students/{id}
PATCH /api/v1/students/{id}
```

**Exit criteria:** Documented, tested APIs operate against PostgreSQL;
API contracts are ready for both module owners.

## Milestone 7 --- Build Admission and Student Frontends Independently

**Status: PLANNED --- may overlap safely with Milestone 6**

**Admission module (`admission/`):** - \[ \] Application form and
client-side validation. - \[ \] Applicant list and detail view. - \[ \]
Admission review/status interface. - \[ \] Approval/rejection actions
connected to the agreed API.

**Student module (`student/`):** - \[ \] Student directory. - \[ \]
Search/filtering. - \[ \] Student profile/details. - \[ \] Permitted
student updates and status display. - \[ \] Connect to the agreed
student APIs.

-   [ ] Create/update `docs/design.md` when frontend design work begins.
-   [ ] Mock data may be used temporarily, but must be replaced by real
    APIs before the integrated workflow is declared complete.

**Exit criteria:** Each module can be demonstrated independently and its
API usage, limitations and blockers are documented.

## Milestone 8 --- Integrate the Complete Admission-to-Student Workflow

**Status: PLANNED**

-   [ ] Connect both frontends to the shared FastAPI backend.
-   [ ] Verify API contracts, loading states and error handling.
-   [ ] Submit an application and retrieve it through the admission
    module.
-   [ ] Approve/reject it through the authorized workflow.
-   [ ] Verify approval creates exactly one student record according to
    confirmed college rules.
-   [ ] Verify the student record references the originating admission
    and appears in Student Management.
-   [ ] Check CORS, validation, duplicate requests, transaction rollback
    and data consistency.
-   [ ] Update architecture/API documentation if implementation differs
    from the agreed design.

**Exit criteria:** The complete workflow succeeds end to end against the
real development database, not just mock data.

## Milestone 9 --- Security, Reliability and Regression Testing

**Status: PLANNED**

-   [ ] Test valid and invalid submissions, missing fields and invalid
    status transitions.
-   [ ] Test duplicate approval/registration and repeated requests.
-   [ ] Test database failure and transaction rollback.
-   [ ] Implement and test authentication/role-based authorization
    appropriate to the agreed scope before exposing protected actions.
-   [ ] Add database integration and end-to-end tests.
-   [ ] Re-run the full test suite and fix major bugs.
-   [ ] Avoid claiming security or production readiness without
    evidence.

**Exit criteria:** Critical workflow and failure paths are tested; known
limitations and unresolved risks are recorded.

## Milestone 10 --- Setup, Demo and Delivery

**Status: PLANNED**

-   [ ] Prepare synthetic demo data; do not use real student personal
    data without authorization.
-   [ ] Verify environment configuration and keep `.env`, credentials
    and tokens out of Git.
-   [ ] Verify database migrations and application startup from a clean
    setup.
-   [ ] Update `README.md` with prerequisites, setup, run, migration and
    test instructions.
-   [ ] Prepare and rehearse a short demonstration of the end-to-end
    workflow.
-   [ ] Confirm repository status, documentation and final known
    limitations.
-   [ ] Deploy only if time, hosting and security requirements permit.

**Exit criteria:** Another teammate can set up and run the project using
the documented instructions, and the demo shows the real working
workflow.

## Working Rules for Every Milestone

1.  **Read before changing:** Inspect the relevant documentation and
    actual repository files before significant implementation or
    architecture changes.
2.  **Small, ordered steps:** Make one bounded change at a time; explain
    the purpose in beginner-friendly language.
3.  **Verify before marking complete:** Record the test or observable
    evidence. UI existence alone is not proof.
4.  **Update this map:** When a milestone is completed, update its
    status and checklist; record test results, blockers and the
    immediate next action.
5.  **Record route/architecture changes:** If an API route, schema,
    workflow or major decision changes, update this map and the relevant
    `architecture.md`, `prd.md`, `rules.md`, `design.md` or `memory.md`
    in the same task as appropriate.
6.  **Keep documents purposeful:** `phases.md` is only this master
    milestone map. Use `memory.md` for material decisions---not a
    conversation diary.
7.  **Every teammate contributes:** The person completing a milestone
    reports completed work, tests, blockers and next steps so the map
    remains truthful.
8.  **Safe Git workflow:** Check `git status`, review the diff, stage
    specific relevant files, and commit code plus relevant documentation
    together. Never commit `.env`, credentials, tokens or `.venv`.
9.  **No guessed college policy:** Keep uncertain registration
    conditions, required fields, permissions and numbering rules marked
    as unresolved until confirmed.
10. **Re-plan transparently:** If a blocker or new requirement changes
    the sequence, update the map before proceeding and explain why.
