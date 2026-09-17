from collections.abc import Callable

from codescape.parse.classifiers import IngClassifier
from codescape.parse.models import BankIdentifier, DocumentCategory


def test_ing_statement_classification(
    load_ing_fixture: Callable[[str], str],
) -> None:
    text = load_ing_fixture("kontoauszug_2026_08.txt")
    classifier = IngClassifier()

    metadata = classifier.classify(text)

    assert metadata is not None
    assert metadata.bank == BankIdentifier.ING
    assert metadata.category == DocumentCategory.ACCOUNT_STATEMENT
    assert metadata.statement_period_year == 2026
    assert metadata.statement_period_month == 8
    assert metadata.account_iban == "DE52500105171234567895"
