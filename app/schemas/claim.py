
from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ClaimCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    claim_reference: str = Field(
        min_length=3,
        max_length=40,
        pattern=r"^[A-Za-z0-9_-]+$",
    )
    patient_reference: str = Field(
        min_length=3,
        max_length=40,
        pattern=r"^[A-Za-z0-9_-]+$",
    )
    service_date: date
    service_category: Literal[
        "consultation",
        "diagnostic",
        "emergency",
        "inpatient",
        "outpatient",
    ]
    claim_amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    diagnosis_code: str = Field(
        min_length=2,
        max_length=20,
    )


class ClaimResponse(ClaimCreate):
    id: int
    status: Literal["submitted"] = "submitted"
