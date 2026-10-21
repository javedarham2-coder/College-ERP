# Important Project Decisions

Record decisions that materially change project direction.
Do not use this file as a transcript of ordinary conversations.

## Decision 1 — Integrated Scope
The project contains Admission Management and Student Management.
They will be developed in separate folders and integrated after shared
interfaces and data relationships are agreed.

## Decision 2 — Standalone First
A standalone application is acceptable for the college project.
Development must not depend on access to the existing ERP source code.

## Decision 3 — Provisional Technology Stack
React, TypeScript, Vite, FastAPI, SQLAlchemy, PostgreSQL, and Docker Compose
are the proposed foundation. Verify compatibility and setup before implementation.

## Decision 4 — Existing ERP Integration
The existing Android ERP's source code, backend, and database are unknown.
Do not connect to production systems or create conflicting official student
records without authorization and technical investigation.

## Decision 5 — Documentation Discipline
Maintain prd.md, architecture.md, rules.md, phases.md, design.md, and memory.md.
Create design.md when frontend work starts. Each teammate updates phases.md
after completing a milestone. Update relevant documents when important decisions
or implementations change.

## Decision 6 — Data Safety
Use synthetic development data. Do not commit secrets or real student records.
