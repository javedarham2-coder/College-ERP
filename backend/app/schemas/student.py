from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_number: str
    enrollment_number: str | None
    admission_id: int
    full_name: str
    email: str
    phone_number: str
    course: str
    branch: str
    current_year: int
    roll_number: str | None
    created_at: datetime
    updated_at: datetime


class StudentUpdate(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, min_length=7, max_length=20)
    current_year: int | None = Field(default=None, ge=1)
    enrollment_number: str | None = Field(default=None, max_length=100)
    roll_number: str | None = Field(default=None, max_length=100)