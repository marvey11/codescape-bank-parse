"""codescape-bank-parse public API."""

from codescape.parse.classifiers import (
    BaseDocumentClassifier,
    ClassifierRegistry,
    default_registry,
)
from codescape.parse.models import (
    BankIdentifier,
    DocumentCategory,
    DocumentMetadata,
    StatementFrequency,
)
from codescape.parse.parse_document import extract_text_from_pdf, parse_document

__all__ = [
    "BankIdentifier",
    "BaseDocumentClassifier",
    "ClassifierRegistry",
    "DocumentCategory",
    "DocumentMetadata",
    "StatementFrequency",
    "default_registry",
    "extract_text_from_pdf",
    "parse_document",
]
