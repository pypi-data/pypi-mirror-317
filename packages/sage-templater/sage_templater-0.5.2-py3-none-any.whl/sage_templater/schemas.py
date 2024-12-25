from decimal import Decimal
from typing import Annotated, AnyStr, Optional

from pydantic import BaseModel, BeforeValidator


def validate_decimal(value: AnyStr):
    """Validate the tax value."""
    if isinstance(value, tuple):
        value = value[0]
    if value is None or value == "" or value == "None":
        return Decimal("0.0")
    return Decimal(value)


Tax = Annotated[Decimal, BeforeValidator(validate_decimal)]
Amount = Annotated[Decimal, BeforeValidator(validate_decimal)]
Total = Annotated[Decimal, BeforeValidator(validate_decimal)]


class PetitCashRecordSchema(BaseModel):
    """Small box record schema."""

    code: Optional[str] = None
    national_id: Optional[str] = None
    verification_digit: Optional[str] = None
    name: str
    invoice: Optional[str] = None
    date: str
    amount: Amount
    tax: Tax
    total: Total
    description: str
    source_file: Optional[str] = None
    source_sheet: Optional[str] = None


class PetitCashSageRecordSchema(BaseModel):
    """Small box record schema for Sage import"""
    date: str
    reference: str
    description: str
    amount: Decimal
    account: str
    distribution_number: int


# Fecha
# No. Ck.
# A nombre de:
# RUC
# DV
# Monto
# ITBMS
# Total
# Concepto
# Proyecto

class CheckRecordSchema(BaseModel):
    """Check record schema."""

    date: Optional[str] = None
    check_number: str
    name: str
    national_id: Optional[str] = None
    verification_digit: Optional[str] = None
    amount: Decimal
    tax: Tax
    total: Decimal
    description: str
    project: Optional[str] = None
