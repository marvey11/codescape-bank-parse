from collections.abc import Callable

from codescape.parse.classifiers import (
    BaseDocumentClassifier,
    ClassifierRegistry,
    ComdirectClassifier,
)
from codescape.parse.models import BankIdentifier, DocumentCategory, DocumentMetadata


class MockMatchingClassifier(BaseDocumentClassifier):
    def can_classify(self, text_content: str) -> bool:
        return True

    def classify(self, text_content: str) -> DocumentMetadata | None:
        return DocumentMetadata(
            bank=BankIdentifier.COMDIRECT,
            category=DocumentCategory.ACCOUNT_STATEMENT,
        )


class MockUnusedClassifier(BaseDocumentClassifier):
    def can_classify(self, text_content: str) -> bool:
        raise AssertionError("Should not be called")

    def classify(self, text_content: str) -> DocumentMetadata | None:
        return None


class TestClassifierRegistry:
    """Unit tests for ClassifierRegistry dispatching logic."""

    def test_classify_text_returns_first_matching_classifier(
        self,
        load_comdirect_fixture: Callable[[str], str],
    ) -> None:
        registry = ClassifierRegistry()
        registry.register(ComdirectClassifier)
        text = load_comdirect_fixture("finanzreport_2026_08.txt")

        metadata = registry.classify(text)

        assert metadata is not None
        assert metadata.bank == BankIdentifier.COMDIRECT
        assert metadata.category == DocumentCategory.ACCOUNT_STATEMENT

    def test_classify_stops_at_first_match(self) -> None:
        """Verify registry evaluation order stops immediately on first match."""

        registry = ClassifierRegistry()
        registry.register(MockMatchingClassifier)
        registry.register(MockUnusedClassifier)

        metadata = registry.classify("some document text")

        assert metadata is not None
        assert metadata.bank == BankIdentifier.COMDIRECT

    def test_classify_returns_none_when_no_classifier_matches(self) -> None:
        """Verify registry retu rns None when no registered classifier matches."""

        registry = ClassifierRegistry()

        metadata = registry.classify("unrecognized document content")

        assert metadata is None
