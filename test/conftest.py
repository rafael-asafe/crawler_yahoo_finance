import pytest
from const_fixtures import INVALID_PRICE_HTML, MISSING_COLUMNS_HTML, VALID_TABLE_HTML

from data_handler.file_handler import FileHandler
from factories import EquityFactory


@pytest.fixture
def make_equity():
    return EquityFactory.build


@pytest.fixture
def valid_table_html():
    return VALID_TABLE_HTML


@pytest.fixture
def invalid_price_html():
    return INVALID_PRICE_HTML


@pytest.fixture
def missing_columns_html():
    return MISSING_COLUMNS_HTML


@pytest.fixture
def equity(make_equity):
    return make_equity()


@pytest.fixture
def equities(make_equity):
    return [make_equity(), make_equity()]


@pytest.fixture
def handler(tmp_path) -> FileHandler:
    h = object.__new__(FileHandler.__wrapped__)
    h.base_path = str(tmp_path)
    h.csv_name = "equities.csv"
    return h
