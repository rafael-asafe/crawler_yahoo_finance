from bs4 import BeautifulSoup

from data_handler.models import EquitiesSchema
from utils.logger import logger


class Parser:
    """Parses HTML pages from the Yahoo Finance screener into EquitiesSchema objects."""

    @staticmethod
    def _get_headers(table_soup) -> tuple[int, int, int]:
        """Returns column indices for symbol, name and price from table headers."""
        col_map = {
            th.get_text(strip=True): i
            for i, th in enumerate(table_soup.thead.find_all("th"))
            if th.get_text(strip=True)
        }
        sym_idx = next((i for h, i in col_map.items() if h.lower() == "symbol"), None)
        name_idx = next((i for h, i in col_map.items() if h.lower() == "name"), None)
        price_idx = next(
            (i for h, i in col_map.items() if "price (intraday)" in h.lower()), None
        )

        if None in [sym_idx, name_idx, price_idx]:
            logger.error("Required columns not found during parsing")
            raise ValueError

        logger.debug("Column indices — symbol: %s, name: %s, price: %s", sym_idx, name_idx, price_idx)
        return sym_idx, name_idx, price_idx

    @staticmethod
    def get_equities_data(pages_source: list[str]) -> list[EquitiesSchema]:
        """Parses all HTML pages and returns a list of EquitiesSchema."""
        if not pages_source:
            raise ValueError("pages_source is empty")

        rows = []
        table_soup = None

        for i, page in enumerate(pages_source):
            soup = BeautifulSoup(page, "html.parser")
            table_soup = soup.find("table")

            page_rows = [
                [td.get_text(strip=True) for td in tr.find_all("td")]
                for tr in table_soup.tbody.find_all("tr")
                if tr.find_all("td")
            ]
            logger.debug("Page %s: %s rows extracted", i + 1, len(page_rows))
            rows.extend(page_rows)

        sym_idx, name_idx, price_idx = Parser._get_headers(table_soup)
        equities = [
            EquitiesSchema(
                symbol=row[sym_idx],
                name=row[name_idx],
                price=float(row[price_idx].replace(",", "")),
            )
            for row in rows
        ]

        logger.info("Parsed %s equities across %s pages", len(equities), len(pages_source))
        return equities