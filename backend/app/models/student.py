from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    student_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    enrollment_number: Mapped[str | None] = mapped_column(
        String(100), unique=True, nullable=True
    )

    admission_id: Mapped[int] = mapped_column(
        ForeignKey("admissions.id", ondelete="RESTRICT"),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)

    course: Mapped[str] = mapped_column(String(100), nullable=False)
    branch: Mapped[str] = mapped_column(String(100), nullable=False)

    current_year: Mapped[int] = mapped_column(Integer, nullable=False)

    roll_number: Mapped[str | None] = mapped_column(
        String(100), unique=True, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )