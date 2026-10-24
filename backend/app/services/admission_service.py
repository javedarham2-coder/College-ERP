import secrets
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.admission import Admission
from app.schemas.admission import AdmissionCreate
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.admission import Admission


def generate_application_number() -> str:
    return f"APP-{datetime.now(timezone.utc):%Y%m%d}-{secrets.token_hex(4).upper()}"


def create_admission(db: Session, data: AdmissionCreate) -> Admission:
    admission = Admission(
        **data.model_dump(),
        application_number=generate_application_number(),
        status="submitted",
    )
    db.add(admission)
    db.commit()
    db.refresh(admission)
    return admission


def list_admissions(
    db: Session,
    *,
    offset: int = 0,
    limit: int = 20,
    status: str | None = None,
) -> list[Admission]:
    statement = select(Admission).order_by(Admission.id.desc())

    if status:
        statement = statement.where(Admission.status == status)

    return list(db.scalars(statement.offset(offset).limit(limit)).all())


def get_admission(db: Session, admission_id: int) -> Admission | None:
    return db.get(Admission, admission_id)

def review_admission(
    db: Session,
    admission_id: int,
    decision: str,
    remarks: str | None = None,
) -> Admission:
    admission = db.get(Admission, admission_id)

    if admission is None:
        raise HTTPException(
            status_code=404,
            detail="Admission application not found.",
        )

    if admission.status not in {"submitted", "under_review"}:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot review an application with status '{admission.status}'.",
        )

    if decision not in {"approved", "rejected"}:
        raise HTTPException(
            status_code=422,
            detail="Decision must be approved or rejected.",
        )

    admission.status = decision
    admission.review_remarks = remarks
    admission.reviewed_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(admission)
    except Exception:
        db.rollback()
        raise

    return admission