import re
from datetime import date
from typing import ClassVar

from codescape.parse.models import BankIdentifier, DocumentCategory, DocumentMetadata

from .base import BaseDocumentClassifier


class IngClassifier(BaseDocumentClassifier):
    """Classifier for ING bank account statements."""

    schema_version: int = 1

    # German month names map for text-based date parsing
    GERMAN_MONTHS: ClassVar[dict[str, int]] = {
        "januar": 1,
        "februar": 2,
        "märz": 3,
        "maerz": 3,
        "april": 4,
        "mai": 5,
        "juni": 6,
        "juli": 7,
        "august": 8,
        "september": 9,
        "oktober": 10,
        "november": 11,
        "dezember": 12,
    }

    # Bank identification signatures
    BANK_SIGNATURES: ClassVar[list[re.Pattern[str]]] = [
        re.compile(r"ING-DiBa\s+AG", re.IGNORECASE),
        re.compile(r"www\.ing\.de", re.IGNORECASE),
        re.compile(r"BIC:?\s*INGDDEFF", re.IGNORECASE),
    ]

    # Pattern for "Kontoauszug August 2026"
    MONTH_NAME_STATEMENT_PATTERN = re.compile(
        r"Kontoauszug\s+([a-zäöü]+)\s+(\d{4})",
        re.IGNORECASE,
    )

    # Pattern for "Datum 31.08.2026" or "Datum: 31.08.2026"
    DOCUMENT_DATE_PATTERN = re.compile(
        r"Datum\s*:?\s*(\d{2})\.(\d{2})\.(\d{4})",
        re.IGNORECASE,
    )

    # General German IBAN pattern
    IBAN_PATTERN = re.compile(
        r"\b(DE\d{2}\s*(?:\d{4}\s*){4}\d{2})\b",
        re.IGNORECASE,
    )

    def can_classify(self, text_content: str) -> bool:
        """Verify whether the text contains ING bank signatures."""
        if not text_content:
            return False
        return any(pattern.search(text_content) for pattern in self.BANK_SIGNATURES)

    def classify(self, text_content: str) -> DocumentMetadata | None:
        """Extract metadata from raw document text."""
        if not self.can_classify(text_content):
            return None

        period_month: int | None = None
        period_year: int | None = None
        doc_date: date | None = None

        # 1. Match month name pattern: "Kontoauszug August 2026"
        month_match = self.MONTH_NAME_STATEMENT_PATTERN.search(text_content)
        if month_match:
            month_str = month_match.group(1).lower()
            period_month = self.GERMAN_MONTHS.get(month_str)
            period_year = int(month_match.group(2))

        # 2. Extract issue date: "Datum 31.08.2026"
        date_match = self.DOCUMENT_DATE_PATTERN.search(text_content)
        if date_match:
            day = int(date_match.group(1))
            month = int(date_match.group(2))
            year = int(date_match.group(3))
            doc_date = date(year, month, day)

            # Fallback if text-based month matching failed
            if not (period_month and period_year):
                period_month = month
                period_year = year

        # 3. Extract primary IBAN
        iban_match = self.IBAN_PATTERN.search(text_content)
        iban = re.sub(r"\s+", "", iban_match.group(1)) if iban_match else None

        return DocumentMetadata(
            bank=BankIdentifier.ING,
            category=DocumentCategory.ACCOUNT_STATEMENT,
            statement_period_year=period_year,
            statement_period_month=period_month,
            document_date=doc_date,
            account_iban=iban,
            schema_version=self.schema_version,
        )
