from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Date,
    Integer,
    Numeric,
    String,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Claim(Base):
    __tablename__ = "claims"

    __table_args__ = (
        CheckConstraint("claim_amount > 0", name="ck_claim_amount_positive"),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    claim_reference: Mapped[str] = mapped_column(
        String(40), unique=True, nullable=False, index=True
    )
    patient_reference: Mapped[str] = mapped_column(
        String(40), nullable=False, index=True
    )
    service_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )
    service_category: Mapped[str] = mapped_column(
        String(20), nullable=False
    )
    claim_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    diagnosis_code: Mapped[str] = mapped_column(
        String(20), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="submitted"
    )