from collections.abc import Callable

from codescape.parse.classifiers import ComdirectClassifier
from codescape.parse.models import BankIdentifier, DocumentCategory


class TestComdirectClassifier:
    def test_comdirect_legacy_2008_classification(
        self,
        load_comdirect_fixture: Callable[[str], str],
    ) -> None:
        comdirect_classifier = ComdirectClassifier()
        text = load_comdirect_fixture("finanzreport_2008_12.txt")

        meta = comdirect_classifier.classify(text)

        assert meta is not None
        assert meta.bank == BankIdentifier.COMDIRECT
        assert meta.category == DocumentCategory.ACCOUNT_STATEMENT
        assert meta.statement_period_year == 2008
        assert meta.statement_period_month == 12

    def test_comdirect_modern_2026_classification(
        self,
        load_comdirect_fixture: Callable[[str], str],
    ) -> None:
        comdirect_classifier = ComdirectClassifier()
        text = load_comdirect_fixture("finanzreport_2026_08.txt")

        meta = comdirect_classifier.classify(text)

        assert meta is not None
        assert meta.bank == BankIdentifier.COMDIRECT
        assert meta.category == DocumentCategory.ACCOUNT_STATEMENT
        assert meta.statement_period_year == 2026
        assert meta.statement_period_month == 7  # Early August issue -> July period
        assert meta.account_iban == "DE97200411441234567800"

    def test_comdirect_date_resolution(self) -> None:
        classifier = ComdirectClassifier()

        # Early August issue -> July report
        meta_aug = classifier.classify(
            "comdirect bank AG Finanzreport Nr. 7 per 03.08.2026"
        )
        assert meta_aug is not None
        assert meta_aug.statement_period_month == 7
        assert meta_aug.statement_period_year == 2026

        # End of December issue -> December report
        meta_dec = classifier.classify(
            "comdirect bank AG Finanzreport Nr. 12 per 31.12.2025"
        )
        assert meta_dec is not None
        assert meta_dec.statement_period_month == 12
        assert meta_dec.statement_period_year == 2025

        # Early January issue -> December report (previous year)
        meta_jan = classifier.classify(
            "comdirect bank AG Finanzreport Nr. 12 per 02.01.2026"
        )
        assert meta_jan is not None
        assert meta_jan.statement_period_month == 12
        assert meta_jan.statement_period_year == 2025
