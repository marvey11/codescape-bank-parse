from abc import ABC, abstractmethod

from codescape.parse.models import DocumentMetadata


class BaseDocumentClassifier(ABC):
    """Interface for document type and metadata detection."""

    schema_version: int = 1

    @abstractmethod
    def can_classify(self, text_content: str) -> bool:
        """Quick check (regex/signature) to verify if this parser handles the layout."""
        ...

    @abstractmethod
    def classify(self, text_content: str) -> DocumentMetadata | None:
        """Extract classification metadata from raw document text."""
        ...
