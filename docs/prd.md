# Product Requirements Document (PRD)

## 1. Project Overview
Build an integrated College ERP with two independently developed modules:
Admission Management and Student Management.

The application must be functional, database-backed, testable, and suitable
for a college project demonstration.

## 2. Target Users
- Applicant: registers, submits an application, uploads documents, and tracks status.
- Admission Officer: reviews applications, verifies documents, and records decisions.
- Student: views their authorized student profile and academic information.
- Administrator: manages authorized users and system configuration.

## 3. Core Features

### Admission Management
- Applicant registration and authentication.
- Multi-step admission application.
- Server-side validation and duplicate-submission prevention.
- Secure document upload and verification.
- Application status tracking.
- Admission review, remarks, and authorized decisions.
- Audit history for important decisions.

### Student Management
- Student record creation after the approved enrollment conditions are satisfied.
- Unique student identifier and configurable roll-number assignment.
- Student profiles and searchable records.
- Authorized profile updates.
- Basic academic history and permitted reports.
- Prevention of duplicate student records.

## 4. Integrated Workflow
Applicant submits application
-> Admission staff review documents
-> Admission is approved under college rules
-> Backend creates one official student record
-> Student record becomes available in Student Management.

## 5. Initial Scope
Prioritize the complete admission-to-student workflow, authentication,
database persistence, validation, and testing.

Fee collection, examination management, attendance management, and other
groups' modules are outside our current scope.

## 6. Constraints
- Four-member student team.
- Target timeline: 2–4 weeks.
- Mostly beginner-level developers.
- Standalone development is acceptable.
- Existing ERP integration is not yet confirmed.
- Use synthetic data during development.

## 7. Requirements Requiring College Confirmation
- Required admission fields and documents.
- Eligibility and merit rules.
- Final enrollment/approval conditions.
- Student ID and roll-number formats.
- User roles and permissions.
- Data retention and deployment requirements.

## 8. Definition of Done
A feature is complete only when its behavior is implemented, tested,
and documented as appropriate. A visible UI alone does not qualify.
