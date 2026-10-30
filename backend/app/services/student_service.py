import secrets

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.admission import Admission
from app.models.student import Student
from app.schemas.student import StudentUpdate


def list_students(
    db: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[Student]:
    statement = (
        select(Student)
        .order_by(Student.id.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def get_student(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def register_student_from_admission(
    db: Session,
    admission_id: int,
    current_year: int,
) -> tuple[Student, bool]:
    """
    Register an approved admission as a student.

    Returns:
        (student, created)
        created is False when the student was already registered.
    """
    try:
        # PostgreSQL locks the admission row so concurrent registration
        # requests for the same admission are serialized.
        admission = db.scalar(
            select(Admission)
            .where(Admission.id == admission_id)
            .with_for_update()
        )

        if admission is None:
            raise HTTPException(
                status_code=404,
                detail="Admission application not found.",
            )

        if admission.status != "approved":
            raise HTTPException(
                status_code=409,
                detail="Only approved admissions can be registered.",
            )

        existing_student = db.scalar(
            select(Student).where(Student.admission_id == admission_id)
        )

        if existing_student is not None:
            db.commit()
            return existing_student, False

        student = Student(
            student_number=f"STU-{secrets.token_hex(8).upper()}",
            admission_id=admission.id,
            full_name=admission.full_name,
            email=admission.email,
            phone_number=admission.phone_number,
            course=admission.course_applied,
            branch=admission.branch_applied,
            current_year=current_year,
            enrollment_number=None,
            roll_number=None,
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        return student, True

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()

        # The unique admission_id constraint is the final protection
        # against duplicate registration.
        existing_student = db.scalar(
            select(Student).where(Student.admission_id == admission_id)
        )

        if existing_student is not None:
            return existing_student, False

        raise

    except Exception:
        db.rollback()
        raise


def update_student(
    db: Session,
    student: Student,
    payload: StudentUpdate,
) -> Student:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)
    except Exception:
        db.rollback()
        raise

    return student