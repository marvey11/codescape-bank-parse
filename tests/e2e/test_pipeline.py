import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from codescape.parse import parse_document
from codescape.parse.models import (
    BankIdentifier,
    DocumentCategory,
    StatementFrequency,
)


def create_mock_pdf_bytes(text_content: str) -> bytes:
    """Helper to construct an in-memory PDF with readable text streams via ReportLab."""
    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)

    text_object = pdf_canvas.beginText(50, 750)
    text_object.setFont("Helvetica", 10)

    for line in text_content.splitlines():
        text_object.textLine(line)

    pdf_canvas.drawText(text_object)
    pdf_canvas.showPage()
    pdf_canvas.save()

    return buffer.getvalue()


class TestParseDocumentIntegration:
    """End-to-end integration tests for parse_document using pypdf."""

    def test_parse_document_scalable_quarterly_pdf(self) -> None:
        raw_text = (
            "Scalable Capital Bank GmbH • Seitzstraße 8e, 80538 Munich\n"
            "Periodic balance statementPeriod 01.04.2026 - 30.06.2026\n"
            "Clearing account DE76120700700758453158 (DEUTDEFFXXX)\n"
            "Date 02.07.2026"
        )
        pdf_bytes = create_mock_pdf_bytes(raw_text)

        # Act: Pass raw PDF bytes directly into the pipeline
        metadata = parse_document(pdf_bytes)

        # Assert: Verify pypdf extraction + classifier pipeline works end-to-end
        assert metadata is not None
        assert metadata.bank == BankIdentifier.SCALABLE
        assert metadata.category == DocumentCategory.ACCOUNT_STATEMENT
        assert metadata.frequency == StatementFrequency.QUARTERLY
        assert metadata.statement_period_year == 2026
        assert metadata.statement_period_quarter == 2
        assert metadata.account_iban == "DE76120700700758453158"

    def test_parse_document_unclassified_pdf(self) -> None:
        raw_text = "Random invoice document with no bank signatures."
        pdf_bytes = create_mock_pdf_bytes(raw_text)

        metadata = parse_document(pdf_bytes)

        assert metadata is None
