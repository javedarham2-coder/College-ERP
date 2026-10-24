from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.admission import AdmissionCreate, AdmissionRead
from app.services.admission_service import (
    create_admission,
    get_admission,
    list_admissions,
)
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status as http_status

from app.config import settings
from app.schemas.admission import AdmissionReview
from app.services.admission_service import review_admission



router = APIRouter(prefix="/api/v1/admissions", tags=["Admissions"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=AdmissionRead, status_code=status.HTTP_201_CREATED)
def submit_admission(payload: AdmissionCreate, db: DbSession):
    try:
        return create_admission(db, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The application conflicts with an existing database record.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to save the application right now.",
        ) from exc


@router.get("", response_model=list[AdmissionRead])
def get_admissions(
    db: DbSession,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    admission_status: Literal[
        "submitted", "under_review", "approved", "rejected"
    ] | None = Query(default=None, alias="status"),
):
    try:
        return list_admissions(
            db,
            offset=offset,
            limit=limit,
            status=admission_status,
        )
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to retrieve applications right now.",
        ) from exc


@router.get("/{admission_id}", response_model=AdmissionRead)
def get_admission_details(admission_id: int, db: DbSession):
    try:
        admission = get_admission(db, admission_id)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to retrieve the application right now.",
        ) from exc

    if admission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admission application not found.",
        )

    return admission

@router.post("/{admission_id}/approve", response_model=AdmissionRead)
def approve_admission(
    admission_id: int,
    payload: AdmissionReview,
    db: DbSession,
):
    if not settings.enable_dev_review_endpoints:
        raise HTTPException(
            status_code=404,
            detail="Endpoint not available.",
        )

    return review_admission(
        db,
        admission_id,
        "approved",
        payload.remarks,
    )


@router.post("/{admission_id}/reject", response_model=AdmissionRead)
def reject_admission(
    admission_id: int,
    payload: AdmissionReview,
    db: DbSession,
):
    if not settings.enable_dev_review_endpoints:
        raise HTTPException(
            status_code=404,
            detail="Endpoint not available.",
        )

    return review_admission(
        db,
        admission_id,
        "rejected",
        payload.remarks,
    )