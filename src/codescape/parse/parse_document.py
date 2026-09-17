import io
from pathlib import Path

from pypdf import PdfReader

from codescape.parse.classifiers import ClassifierRegistry, default_registry
from codescape.parse.models import DocumentMetadata


def parse_document(
    pdf_source: str | Path | io.BytesIO | bytes,
    registry: ClassifierRegistry | None = None,
) -> DocumentMetadata | None:
    """Extract text from a PDF source and return matching DocumentMetadata."""
    text_content = extract_text_from_pdf(pdf_source)
    if not text_content.strip():
        return None

    active_registry = registry or default_registry
    return active_registry.classify(text_content)


def extract_text_from_pdf(pdf_source: str | Path | io.BytesIO | bytes) -> str:
    """Extract full raw text content across all pages using pypdf."""
    if isinstance(pdf_source, bytes):
        pdf_source = io.BytesIO(pdf_source)

    reader = PdfReader(pdf_source)
    pages_text: list[str] = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)

    return "\n\n".join(pages_text)
