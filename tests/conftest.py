from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any

import pytest

from codescape.parse.classifiers.comdirect import ComdirectClassifier

# Point to the fixtures directory relative to this test file
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="class")
def comdirect_environment() -> Generator[
    tuple[ComdirectClassifier, dict[str, str]], Any, None
]:
    # --- SETUP (runs once before any tests in the class) ---
    classifier = ComdirectClassifier()
    temp_cache: dict[str, str] = {}

    # Pass resources to the test class/methods
    yield classifier, temp_cache

    # --- TEARDOWN (runs once after all tests in the class finish) ---
    temp_cache.clear()


@pytest.fixture
def load_comdirect_fixture() -> Callable[[str], str]:
    """Factory fixture to load text from a comdirect fixture file."""

    def _loader(filename: str) -> str:
        file_path = FIXTURES_DIR / "comdirect" / filename
        if not file_path.exists():
            pytest.fail(f"Fixture file not found: {file_path}")
        return file_path.read_text(encoding="utf-8")

    return _loader


@pytest.fixture
def load_ing_fixture() -> Callable[[str], str]:
    """Factory fixture to load text from an ING fixture file."""

    def _loader(filename: str) -> str:
        file_path = FIXTURES_DIR / "ing" / filename
        if not file_path.exists():
            pytest.fail(f"Fixture file not found: {file_path}")
        return file_path.read_text(encoding="utf-8")

    return _loader


@pytest.fixture
def load_scalable_fixture() -> Callable[[str], str]:
    """Factory fixture to load text from a Scalable fixture file."""

    def _loader(filename: str) -> str:
        file_path = FIXTURES_DIR / "scalable" / filename
        if not file_path.exists():
            pytest.fail(f"Fixture file not found: {file_path}")
        return file_path.read_text(encoding="utf-8")

    return _loader
