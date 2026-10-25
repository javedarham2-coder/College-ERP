from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth import CurrentUser, StudentStaff
from app.database import get_db
from app.schemas.student import StudentRead, StudentUpdate
from app.services.student_service import (
    get_student,
    list_students,
    update_student,
)

router = APIRouter(prefix="/api/v1/students", tags=["Students"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[StudentRead])
def get_students(
    db: DbSession,
    _user: StudentStaff,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    try:
        return list_students(db, offset=offset, limit=limit)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve students.",
        ) from exc


@router.get("/{student_id}", response_model=StudentRead)
def get_student_details(student_id: int, db: DbSession, user: CurrentUser):
    try:
        student = get_student(db, student_id)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve the student.",
        ) from exc

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found.",
        )
    if user.role == "student" and user.student_id != student.id:
        raise HTTPException(status_code=403, detail="You may only access your own student record.")

    return student


@router.patch("/{student_id}", response_model=StudentRead)
def patch_student(
    student_id: int,
    payload: StudentUpdate,
    db: DbSession,
    user: CurrentUser,
):
    student = get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found.",
        )

    if user.role == "student" and user.student_id != student.id:
        raise HTTPException(status_code=403, detail="You may only update your own student record.")

    changes = payload.model_dump(exclude_unset=True)
    if user.role == "student" and set(changes) - {"email", "phone_number"}:
        raise HTTPException(status_code=403, detail="Students may only update their contact details.")

    if not changes:
        raise HTTPException(
            status_code=422,
            detail="Provide at least one field to update.",
        )

    try:
        return update_student(db, student, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="The update conflicts with an existing student record.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Unable to update the student.",
        ) from exc
        