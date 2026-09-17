import re
from datetime import date
from typing import ClassVar

from codescape.parse.classifiers import BaseDocumentClassifier
from codescape.parse.models import (
    BankIdentifier,
    DocumentCategory,
    DocumentMetadata,
    StatementFrequency,
)


class ScalableClassifier(BaseDocumentClassifier):
    """Classifier for Scalable Capital Bank account and periodic statements."""

    schema_version: int = 1

    # Bank identification signatures
    BANK_SIGNATURES: ClassVar[list[re.Pattern[str]]] = [
        re.compile(r"Scalable\s+Capital\s+Bank\s+GmbH", re.IGNORECASE),
        re.compile(r"HRB\s+217778", re.IGNORECASE),
        re.compile(r"DE300434774", re.IGNORECASE),
    ]

    # Statement type signature
    QUARTERLY_SIGNATURE = re.compile(
        r"Periodic\s+balance\s+statement",
        re.IGNORECASE,
    )

    # Period date range extraction: handles "statementPeriod" spacing artifact
    # Matches: "Period 01.08.2026 - 31.08.2026"
    PERIOD_RANGE_PATTERN = re.compile(
        r"Period\s+\d{2}\.\d{2}\.\d{4}\s*-\s*\d{2}\.(\d{2})\.(\d{4})",
        re.IGNORECASE,
    )

    # Issue date: "Date 02.09.2026"
    DOCUMENT_DATE_PATTERN = re.compile(
        r"Date\s+(\d{2})\.(\d{2})\.(\d{4})",
        re.IGNORECASE,
    )

    # Clearing account IBAN: "Clearing account DE04120700700758294113"
    CLEARING_ACCOUNT_PATTERN = re.compile(
        r"Clearing\s+account\s+(DE\d{20})",
        re.IGNORECASE,
    )

    def can_classify(self, text_content: str) -> bool:
        """Verify whether the text contains Scalable Capital bank signatures."""
        if not text_content:
            return False
        return any(pattern.search(text_content) for pattern in self.BANK_SIGNATURES)

    def classify(self, text_content: str) -> DocumentMetadata | None:
        """
        Extract classification metadata from English Scalable Capital document text.
        """
        if not self.can_classify(text_content):
            return None

        # Determine frequency
        is_quarterly = bool(self.QUARTERLY_SIGNATURE.search(text_content))
        frequency = (
            StatementFrequency.QUARTERLY if is_quarterly else StatementFrequency.MONTHLY
        )

        period_year: int | None = None
        period_month: int | None = None
        period_quarter: int | None = None
        doc_date: date | None = None

        # Extract period timeline
        period_match = self.PERIOD_RANGE_PATTERN.search(text_content)
        if period_match:
            end_month = int(period_match.group(1))
            period_year = int(period_match.group(2))

            if is_quarterly:
                period_quarter = (end_month - 1) // 3 + 1
            else:
                period_month = end_month

        # Extract document issue date
        date_match = self.DOCUMENT_DATE_PATTERN.search(text_content)
        if date_match:
            doc_date = date(
                int(date_match.group(3)),
                int(date_match.group(2)),
                int(date_match.group(1)),
            )

        # Extract Clearing Account IBAN
        iban_match = self.CLEARING_ACCOUNT_PATTERN.search(text_content)
        iban = re.sub(r"\s+", "", iban_match.group(1)) if iban_match else None

        return DocumentMetadata(
            bank=BankIdentifier.SCALABLE,
            category=DocumentCategory.ACCOUNT_STATEMENT,
            frequency=frequency,
            statement_period_year=period_year,
            statement_period_month=period_month,
            statement_period_quarter=period_quarter,
            document_date=doc_date,
            account_iban=iban,
            schema_version=self.schema_version,
        )
