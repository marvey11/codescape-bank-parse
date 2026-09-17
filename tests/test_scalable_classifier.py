from collections.abc import Callable

from codescape.parse.classifiers.scalable import ScalableClassifier
from codescape.parse.models import BankIdentifier, DocumentCategory
from codescape.parse.models.base import StatementFrequency


class TestScalableClassifier:
    """Unit tests for Scalable Capital document classification."""

    def test_can_classify_scalable_signatures(self) -> None:
        classifier = ScalableClassifier()
        text = "Scalable Capital Bank GmbH • Seitzstraße 8e, 80538 Munich"
        assert classifier.can_classify(text) is True

    def test_classify_monthly_cash_account_statement(self) -> None:
        classifier = ScalableClassifier()
        text = (
            "Scalable Capital Bank GmbH • Seitzstraße 8e, 80538 Munich\n"
            "Cash Account Statement Period 01.08.2026 - 31.08.2026\n"
            "Document no. 7210353898\n"
            "Clearing account DE04120700701234567813 (DEUTDEFFXXX)\n"
            "Date 02.09.2026"
        )

        metadata = classifier.classify(text)

        assert metadata is not None
        assert metadata.bank == BankIdentifier.SCALABLE
        assert metadata.category == DocumentCategory.ACCOUNT_STATEMENT
        assert metadata.frequency == StatementFrequency.MONTHLY
        assert metadata.statement_period_year == 2026
        assert metadata.statement_period_month == 8
        assert metadata.account_iban == "DE04120700701234567813"

    def test_classify_quarterly_periodic_statement_with_spacing_artifact(self) -> None:
        classifier = ScalableClassifier()
        text = (
            "Scalable Capital Bank GmbH • Seitzstraße 8e, 80538 Munich\n"
            "Periodic balance statementPeriod 01.04.2026 - 30.06.2026\n"
            "Clearing account DE76120700701234567858 (DEUTDEFFXXX)\n"
            "Date 02.07.2026"
        )

        metadata = classifier.classify(text)

        assert metadata is not None
        assert metadata.bank == BankIdentifier.SCALABLE
        assert metadata.category == DocumentCategory.ACCOUNT_STATEMENT
        assert metadata.frequency == StatementFrequency.QUARTERLY
        assert metadata.statement_period_year == 2026
        assert metadata.statement_period_quarter == 2
        assert metadata.account_iban == "DE76120700701234567858"

    def test_classify_monthly_broker_statement_from_fixture(
        self,
        load_scalable_fixture: Callable[[str], str],
    ) -> None:
        classifier = ScalableClassifier()
        text = load_scalable_fixture("monthly_broker_statement_2026_08.txt")

        metadata = classifier.classify(text)

        assert metadata is not None
        assert metadata.bank == BankIdentifier.SCALABLE
        assert metadata.category == DocumentCategory.ACCOUNT_STATEMENT
        assert metadata.frequency == StatementFrequency.MONTHLY
        assert metadata.statement_period_year == 2026
        assert metadata.statement_period_month == 8
        assert metadata.account_iban == "DE04120700701234567813"

    def test_classify_monthly_overnight_statement_from_fixture(
        self,
        load_scalable_fixture: Callable[[str], str],
    ) -> None:
        classifier = ScalableClassifier()
        text = load_scalable_fixture("monthly_overnight_statement_2026_08.txt")

        metadata = classifier.classify(text)

        assert metadata is not None
        assert metadata.bank == BankIdentifier.SCALABLE
        assert metadata.category == DocumentCategory.ACCOUNT_STATEMENT
        assert metadata.frequency == StatementFrequency.MONTHLY
        assert metadata.statement_period_year == 2026
        assert metadata.statement_period_month == 8
        assert metadata.account_iban == "DE76120700701234567858"

    def test_classify_quarterly_broker_statement_from_fixture(
        self,
        load_scalable_fixture: Callable[[str], str],
    ) -> None:
        classifier = ScalableClassifier()
        text = load_scalable_fixture("quarterly_broker_statement_2026_Q2.txt")

        metadata = classifier.classify(text)

        assert metadata is not None
        assert metadata.bank == BankIdentifier.SCALABLE
        assert metadata.category == DocumentCategory.ACCOUNT_STATEMENT
        assert metadata.frequency == StatementFrequency.QUARTERLY
        assert metadata.statement_period_year == 2026
        assert metadata.statement_period_quarter == 2
        assert metadata.account_iban == "DE04120700701234567813"

    def test_classify_quarterly_overnight_statement_from_fixture(
        self,
        load_scalable_fixture: Callable[[str], str],
    ) -> None:
        classifier = ScalableClassifier()
        text = load_scalable_fixture("quarterly_overnight_statement_2026_Q2.txt")

        metadata = classifier.classify(text)

        assert metadata is not None
        assert metadata.bank == BankIdentifier.SCALABLE
        assert metadata.category == DocumentCategory.ACCOUNT_STATEMENT
        assert metadata.frequency == StatementFrequency.QUARTERLY
        assert metadata.statement_period_year == 2026
        assert metadata.statement_period_quarter == 2
        assert metadata.account_iban == "DE76120700701234567858"
