from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Admission(Base):
    __tablename__ = "admissions"

    __table_args__ = (
        CheckConstraint(
            "status IN ('submitted', 'under_review', 'approved', 'rejected')",
            name="ck_admissions_status",
        ),
        CheckConstraint(
            "class_10_obtained_marks IS NULL "
            "OR class_10_obtained_marks >= 0",
            name="ck_admissions_class_10_obtained_nonnegative",
        ),
        CheckConstraint(
            "class_10_maximum_marks IS NULL "
            "OR class_10_maximum_marks > 0",
            name="ck_admissions_class_10_maximum_positive",
        ),
        CheckConstraint(
            "class_12_obtained_marks IS NULL "
            "OR class_12_obtained_marks >= 0",
            name="ck_admissions_class_12_obtained_nonnegative",
        ),
        CheckConstraint(
            "class_12_maximum_marks IS NULL "
            "OR class_12_maximum_marks > 0",
            name="ck_admissions_class_12_maximum_positive",
        ),
        CheckConstraint(
            "class_10_percentage IS NULL "
            "OR class_10_percentage BETWEEN 0 AND 100",
            name="ck_admissions_class_10_percentage_range",
        ),
        CheckConstraint(
            "class_12_percentage IS NULL "
            "OR class_12_percentage BETWEEN 0 AND 100",
            name="ck_admissions_class_12_percentage_range",
        ),
        CheckConstraint(
            "jee_percentile IS NULL OR jee_percentile BETWEEN 0 AND 100",
            name="ck_admissions_jee_percentile_range",
        ),
        CheckConstraint(
            "cuet_percentile IS NULL OR cuet_percentile BETWEEN 0 AND 100",
            name="ck_admissions_cuet_percentile_range",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    application_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)

    course_applied: Mapped[str] = mapped_column(String(100), nullable=False)
    branch_applied: Mapped[str] = mapped_column(String(100), nullable=False)

    class_10_obtained_marks: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 2), nullable=True
    )
    class_10_maximum_marks: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 2), nullable=True
    )
    class_10_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )

    class_12_obtained_marks: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 2), nullable=True
    )
    class_12_maximum_marks: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 2), nullable=True
    )
    class_12_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )

    jee_applied: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    jee_marks: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    jee_percentile: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    jee_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)

    cuet_applied: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    cuet_marks: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    cuet_percentile: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    cuet_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="submitted", server_default="submitted"
    )
    review_remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
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