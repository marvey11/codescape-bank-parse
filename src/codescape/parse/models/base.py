from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field


class DocumentCategory(StrEnum):
    ACCOUNT_STATEMENT = "account_statement"
    SECURITY_TRANSACTION = "security_transaction"
    CORPORATE_ACTION = "corporate_action"
    TAX_DOCUMENT = "tax_document"
    UNKNOWN = "unknown"


class BankIdentifier(StrEnum):
    COMDIRECT = "comdirect"
    ING = "ing"
    SCALABLE = "scalable"
    UNKNOWN = "unknown"


class StatementFrequency(StrEnum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    UNKNOWN = "unknown"


class DocumentMetadata(BaseModel):
    """Normalized metadata extracted during document classification."""

    model_config = {"frozen": True}

    bank: BankIdentifier
    category: DocumentCategory
    frequency: StatementFrequency = StatementFrequency.MONTHLY
    statement_period_year: int | None = Field(default=None, ge=1900, le=2100)
    statement_period_month: int | None = Field(default=None, ge=1, le=12)
    statement_period_quarter: int | None = Field(default=None, ge=1, le=4)
    account_iban: str | None = None
    document_date: date | None = None
    schema_version: int = 1
