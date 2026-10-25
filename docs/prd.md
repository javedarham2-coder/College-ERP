# Product Requirements Document (PRD)

## 1. Project Overview

Build an integrated College ERP web application containing two independently developed modules:

- Admission Management
- Student Management

Both modules will use a shared FastAPI backend and PostgreSQL database.

The application must be functional, database-backed, testable, and suitable for a college project demonstration.

## 2. Target Users

- **Applicant:** Submits an admission application, provides academic and entrance examination details, and tracks application status.
- **Admission Officer:** Reviews applications, examines submitted information, and records admission decisions.
- **Student:** Views their authorized student profile and academic information.
- **Administrator:** Manages authorized users and system configuration, subject to the authentication and permissions implementation.

## 3. Admission Management

### 3.1 Applicant and Application Information

The admission application should support the following fields:

- Application ID: internal database identifier.
- Application number: unique application reference.
- Full name.
- Email address.
- Phone number.
- Course applied for.
- Branch applied for.
- Class 10 obtained marks.
- Class 10 maximum marks.
- Class 10 percentage.
- Class 12 obtained marks.
- Class 12 maximum marks.
- Class 12 percentage.
- JEE participation status.
- JEE marks or score, where applicable.
- JEE percentile, where applicable.
- JEE rank, where applicable.
- CUET participation status.
- CUET marks or score, where applicable.
- CUET percentile, where applicable.
- CUET rank, where applicable.
- Application status.
- Review remarks.
- Reviewer information, once the user and authorization model is implemented.
- Creation and last-update timestamps.

The final mandatory fields and validation requirements must be confirmed against the college's admission requirements before production use.

### 3.2 Academic Marks and Entrance Examination Results

- Class 10 and Class 12 records should capture obtained marks, maximum marks, and percentage.
- Marks must be non-negative and must not exceed maximum marks.
- Percentages must be within the valid range of 0–100.
- The system should validate that obtained marks and maximum marks are valid before calculating or accepting a percentage.
- JEE and CUET participation must be recorded independently.
- Applicants may have appeared for either examination, both examinations, or neither, according to the applicable admission rules.
- Exam results must remain optional when the applicant did not appear for that examination.
- Marks, percentile, and rank must be stored as separate values because they represent different measurements.
- Exam-specific validation must respect the examination's scoring format and year.
- Support for multiple examination attempts must be confirmed before implementation.

### 3.3 Application Workflow

The intended workflow is:

1. Applicant submits an application.
2. The application is stored in PostgreSQL.
3. Authorized admission staff review the application and its academic information.
4. Staff record the decision and any applicable remarks.
5. The application is approved or rejected according to the permitted status transitions.
6. A student record is created only when the applicable enrollment conditions are satisfied.

The initial proposed statuses are:

- `submitted`
- `under_review`
- `approved`
- `rejected`

Valid status transitions and the exact approval permissions must be enforced by the backend. These proposed statuses must be reviewed before API implementation.

## 4. Student Management

### 4.1 Student Information

The student record should support:

- Internal student database ID.
- Internal student number, unique within the application.
- Official AKTU enrollment number, nullable until assigned.
- Reference to the originating admission application.
- Full name.
- Email address.
- Phone number.
- Registered course.
- Registered branch.
- Current academic year.
- College roll number, if assigned.
- Creation and last-update timestamps.

### 4.2 Student Registration Rules

- A student record must be linked to its originating admission application.
- One admission application may create at most one student record.
- The internal student ID and internal student number must not be confused with the official AKTU enrollment number.
- AKTU assigns the official enrollment number. The application must not invent or present a generated internal identifier as an official AKTU number.
- The enrollment number may remain empty until it is assigned.
- Enrollment numbers must be unique when present.
- Roll numbers must be unique when present.
- Applicant email and phone number should initially be copied into the student record during registration.
- Authorized staff may update student contact information later.
- The current academic year will be updated manually in the initial version.
- Student creation must be transaction-safe and resistant to duplicate requests.

### 4.3 Academic Year

Store the current academic year as an integer:

- `1`: First year
- `2`: Second year
- `3`: Third year
- `4`: Fourth year

The frontend may display these as "1st Year", "2nd Year", "3rd Year", and "4th Year".

The applicable programme duration must determine which years are valid for a particular student.

Automatic year promotion is outside the initial implementation scope.

## 5. Integrated Admission-to-Student Workflow

The expected workflow is:

Applicant submits application  
→ Admission staff review the application  
→ Application is approved or rejected  
→ Applicable enrollment conditions are satisfied  
→ Backend creates exactly one linked student record  
→ Student Management displays the registered student  
→ Authorized staff update the AKTU enrollment number when assigned.

Admission approval and official enrollment are separate concepts. The precise conditions for creating a student record must follow confirmed college rules.

## 6. Initial Project Scope

Prioritize:

- Admission application data.
- Academic marks and entrance examination information.
- Admission review and status management.
- Student registration and profiles.
- Database persistence and integrity constraints.
- Admission-to-student integration.
- Backend validation.
- Automated testing.
- Appropriate authentication and role-based authorization before protected workflows are exposed.

Fee collection, examination management, attendance management, and other groups' modules are outside the current scope.

## 7. Technical and Operational Constraints

- One GitHub repository and one VS Code workspace.
- Separate `admission/` and `student/` module folders.
- Shared FastAPI backend and PostgreSQL database.
- SQLAlchemy for database models and Alembic for migrations.
- PostgreSQL 16 for local development.
- Docker Compose for the local database environment.
- Synthetic data for development and demonstrations.
- No production ERP integration without explicit authorization and technical investigation.

## 8. Requirements Requiring College Confirmation

The following must not be assumed:

- Mandatory admission fields and documents.
- Eligibility and merit rules.
- Accepted Class 10 and Class 12 marks formats.
- Accepted JEE/CUET score formats and applicable validation rules.
- Whether multiple entrance examination attempts must be supported.
- Final enrollment and student-registration conditions.
- Official AKTU enrollment-number assignment process.
- College roll-number format and assignment process.
- Course and branch naming conventions.
- User roles, permissions, and authentication requirements.
- Data retention and deployment requirements.

## 9. Definition of Done

A feature is complete only when:

- Its behavior is implemented.
- Relevant validations and database constraints are present.
- Appropriate automated tests pass.
- Documentation reflects the actual implementation.
- Important limitations and unresolved requirements are recorded.

A visible UI or a proposed schema alone does not qualify as a completed feature.
