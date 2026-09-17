import re
from datetime import date
from typing import ClassVar

from codescape.parse.models import BankIdentifier, DocumentCategory, DocumentMetadata

from .base import BaseDocumentClassifier


class ComdirectClassifier(BaseDocumentClassifier):
    """Classifier for comdirect bank documents with intelligent period resolution."""

    schema_version: int = 1

    BANK_SIGNATURES: ClassVar[list[re.Pattern[str]]] = [
        re.compile(r"comdirect\s+bank\s+AG", re.IGNORECASE),
        re.compile(
            r"comdirect\s+[\u2013-]\s+eine\s+Marke\s+der\s+Commerzbank\s+AG",
            re.IGNORECASE,
        ),
        re.compile(r"Kundennummer:\s*\d+", re.IGNORECASE),
        re.compile(r"COBADEHD", re.IGNORECASE),
    ]

    # Matches
    # - "Finanzreport Nr. 7 per 03.08.2026" or
    # - "Finanzreport Nr. 1 per 31.12.2008"
    FINANZREPORT_PATTERN = re.compile(
        r"Finanzreport\s+(?:Nr\.\s*(\d+)\s+)?(?:per|vom)\s+(\d{2})\.(\d{2})\.(\d{4})",
        re.IGNORECASE,
    )

    GIRO_IBAN_PATTERN = re.compile(
        r"Girokonto\s+(DE\d{2}\s*(?:\d{4}\s*){4}\d{2})",
        re.IGNORECASE,
    )
    GENERIC_IBAN_PATTERN = re.compile(
        r"\b(DE\d{2}\s*(?:\d{4}\s*){4}\d{2})\b",
        re.IGNORECASE,
    )

    def can_classify(self, text_content: str) -> bool:
        if not text_content:
            return False
        return any(pattern.search(text_content) for pattern in self.BANK_SIGNATURES)

    def classify(self, text_content: str) -> DocumentMetadata | None:
        if not self.can_classify(text_content):
            return None

        period_month: int | None = None
        period_year: int | None = None
        doc_date: date | None = None

        match = self.FINANZREPORT_PATTERN.search(text_content)
        if match:
            report_num = int(match.group(1)) if match.group(1) else None
            day = int(match.group(2))
            month = int(match.group(3))
            year = int(match.group(4))

            doc_date = date(year, month, day)
            period_month, period_year = self._resolve_statement_period(
                report_num, day, month, year
            )

        iban_match = self.GIRO_IBAN_PATTERN.search(
            text_content
        ) or self.GENERIC_IBAN_PATTERN.search(text_content)
        iban = re.sub(r"\s+", "", iban_match.group(1)) if iban_match else None

        return DocumentMetadata(
            bank=BankIdentifier.COMDIRECT,
            category=DocumentCategory.ACCOUNT_STATEMENT,
            statement_period_year=period_year,
            statement_period_month=period_month,
            document_date=doc_date,
            account_iban=iban,
            schema_version=self.schema_version,
        )

    def _resolve_statement_period(
        self, report_num: int | None, day: int, month: int, year: int
    ) -> tuple[int, int]:
        """
        Resolve reporting period considering report index and early-month cutoff dates.
        """
        # 1. If explicit report number exists (and >= 2009 monthly era)
        if report_num is not None and 1 <= report_num <= 12 and year >= 2009:
            # Report Nr. 12 issued in early January covers December of the previous year
            if report_num == 12 and month == 1:
                return 12, year - 1
            # Otherwise, report_num directly dictates the target month in the issue year
            return report_num, year

        # 2. Fallback (for older documents or missing report numbers):
        # If cutoff day is early in the month (<= 7), report covers the previous month
        if day <= 7:
            if month == 1:
                return 12, year - 1
            return month - 1, year

        return month, year
