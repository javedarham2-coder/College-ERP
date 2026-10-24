from sqlalchemy import select
from sqlalchemy.orm import Session

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