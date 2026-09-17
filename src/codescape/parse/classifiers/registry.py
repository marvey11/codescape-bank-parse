from codescape.parse.classifiers import BaseDocumentClassifier
from codescape.parse.models import DocumentMetadata


class ClassifierRegistry:
    """Registry to manage and execute document classifiers."""

    def __init__(self) -> None:
        self._classifiers: list[type[BaseDocumentClassifier]] = []

    def register(self, classifier_cls: type[BaseDocumentClassifier]) -> None:
        """Register a new classifier class."""
        if classifier_cls not in self._classifiers:
            self._classifiers.append(classifier_cls)

    def classify(self, text_content: str) -> DocumentMetadata | None:
        """Iterate registered classifiers and return the first matching metadata."""
        for classifier_cls in self._classifiers:
            classifier = classifier_cls()
            if classifier.can_classify(text_content):
                return classifier.classify(text_content)
        return None


# Global registry instance
default_registry = ClassifierRegistry()
