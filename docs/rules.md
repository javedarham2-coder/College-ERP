# Project Rules and Development Workflow

## 1. General Rules
- Read relevant documentation before significant changes.
- Explain the objective and affected files before implementation.
- Work in small, understandable steps.
- Prefer the smallest reliable fix over unrelated refactoring.
- Do not introduce dependencies without a clear reason.
- Never claim functionality works without testing it.
- Ask when college-specific requirements are unknown.

## 2. Coding Rules
- Keep module responsibilities clear.
- Validate inputs on the backend.
- Keep secrets in environment variables, never in committed source files.
- Use database migrations for schema changes.
- Use meaningful names and commit messages.
- Avoid unnecessary duplication and overengineering.

## 3. Security and Data
- Use synthetic data during development.
- Never access production data without authorization.
- Never store plaintext passwords.
- Enforce authorization on the backend.
- Restrict access to uploaded documents.
- Do not commit credentials, tokens, or private student data.
- Log important admission decisions and sensitive record changes.

## 4. Integration Rules
- Agree on API contracts and database relationships before integration.
- Do not independently change shared contracts without team coordination.
- Prevent duplicate student records.
- Test failure cases and unauthorized requests.
- Do not integrate with the existing ERP without permission.

## 5. Git and Team Collaboration
- Keep one shared GitHub repository.
- Use feature branches for assigned work.
- Make small, meaningful commits.
- Review and test changes before merging into the main branch.
- Every teammate updates docs/phases.md when completing a milestone.
- Coordinate changes to shared backend code, database models, and contracts.

## 6. Error-Handling Workflow
1. Read the complete error message.
2. Identify the affected file, command, or request.
3. Find the most likely root cause.
4. Apply the smallest practical fix.
5. Rerun the failing command or test.
6. Record important findings when they affect future work.

## 7. ChatGPT Working Rules
- Give beginner-friendly explanations and exact commands.
- Explain important code and where it belongs.
- Do not generate the entire application at once.
- Do not invent college policies or integration capabilities.
- Distinguish planned, implemented, tested, and deployed features.
- Update relevant documentation when important decisions or implementations change.
