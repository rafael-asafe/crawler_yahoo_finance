import pytest
from pydantic import ValidationError

from crawler.parser import Parser


def test_valid_page_returns_equities(valid_table_html):
    result = Parser.get_equities_data([valid_table_html])
    assert len(result) == 2
    assert result[0].symbol == "AAPL"
    assert result[0].name == "Apple Inc."
    assert result[0].price == 150.0


def test_price_with_comma_is_parsed(valid_table_html):
    result = Parser.get_equities_data([valid_table_html])
    assert result[1].price == 1234.56


def test_multiple_pages_aggregates_rows(valid_table_html):
    result = Parser.get_equities_data([valid_table_html, valid_table_html])
    assert len(result) == 4


def test_empty_pages_raises():
    with pytest.raises(ValueError, match="empty"):
        Parser.get_equities_data([])


def test_missing_columns_raises(missing_columns_html):
    with pytest.raises(ValueError):
        Parser.get_equities_data([missing_columns_html])


def test_negative_price_raises(invalid_price_html):
    with pytest.raises(ValidationError):
        Parser.get_equities_data([invalid_price_html])