# College ERP — Development and AI Collaboration Rules

> **Purpose:** This document defines how every team member and their AI coding assistant must collaborate on the College ERP project.
>
> **Applies to:** All team members, ChatGPT conversations, coding assistants, implementation tasks, code reviews, testing, documentation, and Git operations.
>
> **Primary principle:** Work as a reliable technical teammate. Understand the existing project, preserve verified progress, communicate clearly, and deliver working, tested functionality without unnecessary complexity.

---

# 1. Project Overview

The College ERP project contains two independently developed modules:

- `admission/` — Admission Management.
- `student/` — Student Management.

Both modules will integrate through one shared FastAPI backend and PostgreSQL database.

The intended workflow is:

1. An applicant submits an admission application.
2. Authorized admission staff review the application.
3. The application is approved or rejected.
4. Applicable enrollment conditions are satisfied.
5. The backend creates at most one linked student record.
6. The student appears in Student Management.

The project will initially operate as a standalone application using synthetic development data.

Integration with the college's existing ERP requires appropriate authorization, technical investigation, and an agreed integration plan.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend | Python, FastAPI, Pydantic |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL 16 |
| Migrations | Alembic |
| Testing | pytest |
| Local database environment | Docker Compose |
| Version control | Git and GitHub |

Follow the current repository and architecture documentation if implementation details evolve.

Do not independently change the agreed architecture without explaining the reason and documenting the decision.

---

# 2. How ChatGPT Must Communicate

Every AI assistant working on this project must follow these communication rules.

## 2.1 Be a Teammate

- Communicate naturally, respectfully, and directly.
- Use simple English and explain technical concepts in understandable language.
- Use Hinglish when requested or when it helps a team member understand a concept.
- Be friendly without becoming unnecessarily formal.
- Use headings, bullet points, tables, and code blocks when they improve readability.
- Explain technical terminology when it is unfamiliar or important to the decision.
- Help team members understand why an implementation works, not merely copy code.

## 2.2 Balance Detail With Clarity

- Keep routine answers concise and easy to scan.
- Provide sufficient detail for complex implementation, debugging, architecture, and testing tasks.
- Avoid long paragraphs when a short list communicates the same information.
- Do not repeat the same explanation unnecessarily.
- Do not suggest unrelated improvements that distract from the immediate task.
- Do not overwhelm beginners with several alternative architectures when one suitable approach is already agreed.

Concise does not mean incomplete. Important implementation details, risks, test instructions, and documentation requirements must not be omitted.

## 2.3 Be Honest and Challenge Assumptions

The AI assistant must act as an intellectual collaborator, not merely agree with every suggestion.

- Challenge assumptions when evidence indicates they may be incorrect.
- Explain technical risks and relevant trade-offs.
- Distinguish facts from assumptions and recommendations.
- Identify missing information that materially affects correctness.
- Admit uncertainty rather than inventing an answer.
- Never claim to have inspected files, run commands, tested code, or modified a repository unless that actually happened.
- Correct mistakes directly when they are discovered.

The objective is a reliable project, not simply a quick or agreeable response.

---

# 3. How ChatGPT Must Guide Development

## 3.1 Maintain a Continuous Workflow

Development guidance must be organized into logical phases.

The assistant must not interrupt the workflow after every trivial action. It should continue through clearly understood actions and pause when actual user input is required.

Follow these principles:

1. Identify the current goal and relevant milestone.
2. Check the relevant documentation and repository state.
3. Determine which actions can safely be performed or explained without additional input.
4. Group related instructions into manageable phases.
5. Continue through independent actions when the next action is clear.
6. Pause when a command result, user decision, permission, or other missing information is necessary for correctness.
7. After receiving the requested output, analyze it and continue from the actual result.

### When to Pause

Pause when:

- A terminal output is needed to determine the next action.
- A test or migration fails and the cause must be investigated.
- A requirement or architecture decision is ambiguous.
- An operation could cause data loss or affect an external system.
- Explicit authorization is required.
- The next action depends materially on the user's response.

### When Not to Pause

Do not unnecessarily pause:

- After every minor explanation.
- After every obvious, low-risk action.
- To request confirmation for an already agreed task.
- When several related instructions can be provided together.
- To ask the user to repeat information already available in the conversation or project documentation.

**Important:** A continuous workflow does not mean dumping an entire project implementation into one response. Keep the work manageable while avoiding needless conversational interruptions.

## 3.2 Give Actionable Instructions

When providing implementation guidance:

- Specify the exact file path.
- Explain the purpose of the change.
- Provide complete replacement contents when replacing a file.
- Provide precise edits when only a small section needs changing.
- Provide commands appropriate to the user's current working directory.
- Identify assumptions and prerequisites.
- Explain how to verify the result.
- State what output or information is needed next, when applicable.

Do not give ambiguous instructions such as "configure the backend" without identifying what must actually change.

## 3.3 Troubleshoot Before Moving Forward

When an error occurs:

1. Read the actual error output.
2. Identify the likely cause.
3. Inspect the relevant configuration or source code.
4. Recommend the smallest appropriate correction.
5. Verify the correction with a suitable command or test.
6. Continue the planned workflow after the issue is resolved.

Do not repeatedly suggest unrelated fixes or replace working code without understanding the failure.

---

# 4. Read Before Changing

Before any significant implementation, architecture, configuration, or database change:

1. Read the relevant Markdown documentation.
2. Inspect the existing source code.
3. Check the current project structure.
4. Check Git status when repository changes may already exist.
5. Identify existing behavior and dependencies.
6. Determine whether the proposed change conflicts with an agreed decision.
7. Make the smallest appropriate change.

Do not assume that a file, feature, dependency, API, or configuration is missing merely because it has not been mentioned in the latest conversation.

Do not overwrite existing implementation blindly.

Preserve verified progress unless a specific problem justifies changing it.

---

# 5. Implementation Standards

## 5.1 Code Quality

- Follow the existing project's conventions.
- Use clear, descriptive names.
- Keep functions and modules focused on their responsibilities.
- Avoid unnecessary abstraction and premature optimization.
- Avoid duplicating business logic across the two modules.
- Keep shared contracts consistent.
- Validate inputs at the backend boundary.
- Handle expected errors explicitly.
- Use appropriate type hints and data schemas.
- Keep configuration separate from application logic.
- Avoid introducing dependencies without a clear need.
- Do not refactor unrelated code during a focused task.

Prefer the smallest maintainable implementation that satisfies the agreed requirements.

## 5.2 Preserve Existing Behavior

Before changing existing code, understand its current behavior.

When making a change:

- Preserve unrelated working functionality.
- Identify affected callers, tests, and modules.
- Update dependent code where necessary.
- Test important existing behavior after the change.
- Explain any intentional behavior change.

Do not rewrite entire files when a precise change is sufficient, unless the user explicitly requests a complete replacement or the file genuinely requires restructuring.

## 5.3 Separate Planned, Implemented, and Verified Work

Always distinguish between:

- **Planned:** A proposed design or task that has not been implemented.
- **Implemented:** Code or configuration has been written.
- **Tested:** Relevant tests have been executed and their results inspected.
- **Verified:** The required behavior has been confirmed using appropriate evidence.
- **Deployed:** The intended version has actually been deployed and checked.

These terms are not interchangeable.

A UI existing does not prove that its backend works. A migration file existing does not prove that it applies successfully. A successful unit test does not prove that the entire application workflow works.

---

# 6. Architecture and Module Independence

## 6.1 Admission and Student Modules

Keep Admission Management and Student Management independently developed in their respective folders.

They will share:

- The FastAPI backend.
- The PostgreSQL database.
- Agreed data relationships.
- Approved API contracts.
- Shared types or utilities where appropriate.

Do not merge the two modules into one unstructured folder merely for convenience.

## 6.2 Backend Owns Business Rules

The backend and database must enforce critical business rules.

Examples include:

- Admission-status validation.
- Authorization for admission decisions.
- Validation of marks and other numeric values.
- Uniqueness of identifiers.
- Student-to-admission relationships.
- Prevention of duplicate student registration.
- Transactional student creation.
- Validation of permitted student updates.

Frontend validation improves usability but does not replace backend validation.

## 6.3 Avoid Inventing College Policies

Do not assume or fabricate:

- Mandatory admission documents.
- Eligibility or merit criteria.
- Official admission approval rules.
- Official enrollment-number formats.
- College roll-number formats.
- User roles or permissions.
- Final enrollment conditions.
- Academic promotion rules.
- Data retention policies.

Ask for confirmation when an unresolved requirement materially affects implementation.

When a safe technical default is appropriate, identify it as a provisional implementation decision rather than an established college policy.

---

# 7. Database and Migration Rules

## 7.1 Database Integrity

The database must enforce the agreed integrity rules.

Current project requirements include:

- Unique application numbers.
- Unique internal student numbers.
- Unique official enrollment numbers when assigned.
- Unique roll numbers when assigned.
- A valid admission reference for every student.
- At most one student record linked to a given admission.
- Appropriate numeric validation constraints.
- Transaction-safe student registration.

Use database constraints in addition to application-level validation where appropriate.

## 7.2 Alembic Migrations

When changing the schema:

1. Read the current models and migration configuration.
2. Understand the existing migration history.
3. Make the intended model change.
4. Generate or write the appropriate migration.
5. Review the migration before applying it.
6. Apply it to the intended development database.
7. Verify the resulting schema.
8. Run relevant tests.
9. Update the affected documentation.
10. Review the Git diff before committing.

Never assume that model changes automatically update an existing database.

Do not casually edit or delete an already-applied migration. If migration history needs correction, investigate the current database and migration state first.

Do not use destructive database operations merely to make a migration pass.

## 7.3 Data Safety

- Use synthetic data during development and demonstrations.
- Never commit real student records or sensitive applicant information.
- Never commit `.env`, passwords, tokens, API keys, or other secrets.
- Do not expose database credentials in terminal screenshots, logs, or responses.
- Do not modify production systems without explicit authorization.
- Do not drop tables or reset databases without understanding the impact and obtaining necessary approval.

---

# 8. Testing and Verification

Testing must match the type and risk of the change.

## 8.1 Backend Testing

When relevant, test:

- Normal successful behavior.
- Invalid inputs.
- Missing required fields.
- Numeric boundaries.
- Database constraints.
- Expected error responses.
- Database unavailability.
- Transaction rollback.
- Duplicate requests.
- Authorization and permission boundaries.

Use the existing testing framework and conventions unless there is a justified reason to change them.

## 8.2 Database Testing

For schema changes, verify:

- Migration status.
- Table creation.
- Column types and nullability.
- Primary and foreign keys.
- Unique constraints.
- Check constraints.
- Expected deletion behavior.
- Relevant model metadata tests.

Do not claim the schema is verified merely because the migration command returned success.

## 8.3 Frontend Testing

For frontend changes, verify the relevant behavior, including:

- Form validation.
- Loading and empty states.
- Error handling.
- API integration.
- Search and filtering where applicable.
- Correct display of returned data.
- Appropriate handling of failed requests.

A successful frontend build alone does not prove that the user workflow works.

## 8.4 Report Actual Results

When reporting tests:

- State the command that was run when useful.
- Report the actual pass/fail result.
- Mention failures and relevant warnings.
- Distinguish tests that were run from tests that remain outstanding.
- Never invent test results.

If the environment prevents testing, state the limitation clearly.

---

# 9. Required Documentation Discipline

Maintain these Markdown files:

| File | Responsibility |
|---|---|
| `docs/prd.md` | Product scope, target users, functional requirements, and exclusions |
| `docs/architecture.md` | Architecture, data flow, relationships, technology, and interfaces |
| `docs/rules.md` | Development standards, AI collaboration rules, security, and team workflow |
| `docs/phases.md` | Master milestone plan and chronological progress log |
| `docs/memory.md` | Material project decisions and changes in direction |
| `docs/design.md` | Frontend design decisions when frontend work begins |
| `README.md` | Prerequisites, installation, configuration, execution, migrations, and testing |

## 9.1 Update Documentation With Implementation

When an implementation or material decision changes:

1. Identify the documents affected.
2. Update those documents in the same task.
3. Ensure the documentation matches the actual implementation.
4. Include documentation in the eventual commit.

Do not mechanically rewrite every document after every change.

Update only the documents whose purpose is affected.

When guiding a development milestone, provide complete file contents or precise edits for the relevant documentation, as appropriate.

## 9.2 `phases.md` Uses an Append-Only Progress Log

Routine progress updates must be added to the end of `docs/phases.md`.

Do not repeatedly rewrite the whole file to record ordinary progress.

Each new progress entry should include:

- Date.
- Milestone.
- Current status.
- Completed work.
- Verification evidence and test results.
- Documentation or Git changes.
- Blockers and unresolved decisions.
- Next action.

Preserve earlier entries as historical records.

The permanent milestone plan should only be changed when the plan itself changes or a correction is necessary.

A progress entry does not automatically make a milestone complete.

## 9.3 `memory.md` Records Decisions

Record material project decisions, such as:

- A confirmed architecture change.
- An agreed database relationship.
- A change in implementation strategy.
- A confirmed business rule.
- A significant technical limitation.

Do not turn `memory.md` into a transcript of every conversation, command, or routine update.

## 9.4 Keep Documentation Truthful

Never document an unverified feature as complete.

If a feature is implemented but not tested, say so.

If a decision is provisional, label it provisional.

If an integration remains untested, state that limitation explicitly.

---

# 10. Git and GitHub Workflow

## 10.1 Review Before Committing

Before committing changes:

1. Check the current branch.
2. Review `git status`.
3. Review the diffs of modified files.
4. Inspect new files that do not appear in ordinary diffs.
5. Run relevant tests.
6. Check documentation accuracy.
7. Confirm that secrets and unintended files are excluded.
8. Stage only the intended changes.
9. Review the staged diff.
10. Commit related implementation, tests, configuration, and documentation together.
11. Verify the commit and working-tree status.
12. Push when the intended changes are ready.

Do not blindly stage everything with `git add .` without reviewing the repository state.

Never commit:

- `.env` files.
- Credentials or tokens.
- Virtual environments.
- Unrelated generated files.
- Sensitive real student or applicant data.

## 10.2 Commit Messages

Use clear commit messages that describe the work.

Examples:

```text
feat: add admission and student database models
test: add database model constraint tests
docs: update milestone progress and architecture
fix: validate admission examination scores
```

Use the prefix that best matches the actual changes.

## 10.3 Git Claims Must Be Accurate

Never claim a change has been committed or pushed without evidence.

If a command fails, diagnose the failure before claiming success.

Do not overwrite teammates' work or discard uncommitted changes without understanding their purpose and obtaining appropriate permission.

---

# 11. Team Collaboration

## 11.1 Independent Ownership

Team members may develop their assigned modules independently, but must follow the agreed architecture and shared interfaces.

Before integrating modules:

- Agree on request and response contracts.
- Agree on shared data relationships.
- Identify ownership of shared files.
- Coordinate changes that affect multiple modules.
- Test the integrated behavior.

Do not independently change shared contracts without informing the affected teammates.

## 11.2 Milestone Reporting

Each teammate must update `docs/phases.md` after completing a meaningful milestone.

The entry should state:

- What was completed.
- What was tested.
- Test evidence.
- What remains incomplete.
- Any blockers.
- The next action.

A teammate must not mark a milestone complete merely because their assigned code has been written.

## 11.3 Communicating Blockers

When blocked:

1. State the problem.
2. Explain its impact.
3. Identify the missing information or dependency.
4. Suggest a reasonable next action.
5. Record the blocker in the progress log when it materially affects the project.

Do not silently invent requirements to avoid reporting a blocker.

---

# 12. Security, Privacy, and Authorization

- Use synthetic development data.
- Keep secrets outside version control.
- Validate data on the backend.
- Implement appropriate authorization before exposing protected operations.
- Restrict access to applicant and student information.
- Do not claim that authentication or authorization exists until implemented and tested.
- Do not connect to or modify the college's production ERP without explicit authorization.
- Do not include sensitive information in documentation or logs.
- Review security implications before introducing new external integrations.

Authentication and role-based permissions must be implemented according to confirmed requirements, not assumptions.

---

# 13. AI Assistant Workflow for Every Development Task

Every ChatGPT assistant working on this project should follow this sequence.

## Phase A — Understand

1. Identify the requested outcome.
2. Determine the relevant module and milestone.
3. Read the relevant project documentation.
4. Inspect the existing implementation and repository state.
5. Identify constraints, dependencies, and unresolved requirements.

## Phase B — Plan

1. Define the immediate goal.
2. Choose the smallest appropriate implementation.
3. Identify affected files and modules.
4. Identify relevant tests.
5. Determine which documentation needs updating.
6. Explain significant design choices and trade-offs.

## Phase C — Implement

1. Make focused changes.
2. Preserve unrelated working code.
3. Follow existing conventions.
4. Handle errors and validation appropriately.
5. Avoid unrelated refactoring.
6. Explain unfamiliar or important code where useful.

## Phase D — Verify

1. Run relevant tests or provide exact commands for the user to run.
2. Inspect actual results.
3. Fix failures before proceeding.
4. Verify database or API behavior when relevant.
5. Identify any untested behavior honestly.

## Phase E — Document

1. Update affected Markdown files.
2. Add a progress entry to the end of `docs/phases.md` when appropriate.
3. Record material decisions in `docs/memory.md`.
4. Ensure documentation matches the implementation.

## Phase F — Review and Deliver

1. Review Git status and diffs.
2. Confirm secrets are excluded.
3. Stage only intended files.
4. Commit related code and documentation together.
5. Verify the commit.
6. Report completed work, evidence, limitations, and the next action.

**Important:** These phases define the workflow, not a requirement to send a separate message for every phase. Combine actions into logical groups when safe, and pause when user input or actual output is necessary.

---

# 14. Definition of Done

A task is complete only when its applicable acceptance criteria are satisfied.

Depending on the task, completion may require:

- Correct implementation.
- Relevant tests passing.
- Verified database or API behavior.
- Appropriate error handling.
- Updated documentation.
- Reviewed Git changes.
- A successful commit, when committing is part of the task.

A milestone is complete only when its documented exit criteria are satisfied.

Do not confuse writing code with completing a feature.

Do not confuse completing one module with completing the integrated workflow.

Do not confuse a successful local test with a verified deployment.

---

# 15. Final Working Principles

Every team member and AI assistant must follow these principles:

1. **Understand before changing.**
2. **Preserve verified progress.**
3. **Prefer the smallest correct solution.**
4. **Communicate clearly and naturally.**
5. **Guide work continuously without unnecessary interruptions.**
6. **Pause when real input or evidence is required.**
7. **Test behavior instead of assuming success.**
8. **Update affected documentation alongside implementation.**
9. **Append routine progress entries rather than rewriting history.**
10. **Never invent college policies or official identifiers.**
11. **Protect credentials and sensitive data.**
12. **Review Git changes before committing.**
13. **Be honest about failures, uncertainty, and limitations.**
14. **Help teammates understand the implementation.**
15. **Prioritize a reliable, working, integrated College ERP over unnecessary complexity.**

The shared goal is to deliver a maintainable, database-backed College ERP in which Admission Management and Student Management work independently and integrate correctly through tested APIs and agreed data relationships.
