from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


AdmissionStatus = Literal[
    "submitted",
    "under_review",
    "approved",
    "rejected",
]


class AdmissionCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    phone_number: str = Field(min_length=7, max_length=20)

    course_applied: str = Field(min_length=1, max_length=100)
    branch_applied: str = Field(min_length=1, max_length=100)

    class_10_obtained_marks: Decimal | None = Field(default=None, ge=0)
    class_10_maximum_marks: Decimal | None = Field(default=None, gt=0)
    class_10_percentage: Decimal | None = Field(default=None, ge=0, le=100)

    class_12_obtained_marks: Decimal | None = Field(default=None, ge=0)
    class_12_maximum_marks: Decimal | None = Field(default=None, gt=0)
    class_12_percentage: Decimal | None = Field(default=None, ge=0, le=100)

    jee_applied: bool = False
    jee_marks: Decimal | None = Field(default=None, ge=0)
    jee_percentile: Decimal | None = Field(default=None, ge=0, le=100)
    jee_rank: int | None = Field(default=None, gt=0)

    cuet_applied: bool = False
    cuet_marks: Decimal | None = Field(default=None, ge=0)
    cuet_percentile: Decimal | None = Field(default=None, ge=0, le=100)
    cuet_rank: int | None = Field(default=None, gt=0)


class AdmissionReview(BaseModel):
    remarks: str | None = Field(default=None, max_length=2000)


class AdmissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_number: str
    full_name: str
    email: str
    phone_number: str
    course_applied: str
    branch_applied: str

    class_10_obtained_marks: Decimal | None
    class_10_maximum_marks: Decimal | None
    class_10_percentage: Decimal | None

    class_12_obtained_marks: Decimal | None
    class_12_maximum_marks: Decimal | None
    class_12_percentage: Decimal | None

    jee_applied: bool
    jee_marks: Decimal | None
    jee_percentile: Decimal | None
    jee_rank: int | None

    cuet_applied: bool
    cuet_marks: Decimal | None
    cuet_percentile: Decimal | None
    cuet_rank: int | None

    status: AdmissionStatus
    review_remarks: str | None
    reviewed_at: datetime | None
    created_at: datetime
    updated_at: datetime