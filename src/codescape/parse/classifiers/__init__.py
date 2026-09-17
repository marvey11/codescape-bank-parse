from .base import BaseDocumentClassifier
from .comdirect import ComdirectClassifier
from .ing import IngClassifier
from .registry import ClassifierRegistry, default_registry
from .scalable import ScalableClassifier

# Register built-in classifiers
default_registry.register(ComdirectClassifier)
default_registry.register(IngClassifier)
default_registry.register(ScalableClassifier)


__all__ = [
    "BaseDocumentClassifier",
    "ClassifierRegistry",
    "ComdirectClassifier",
    "IngClassifier",
    "ScalableClassifier",
    "default_registry",
]
