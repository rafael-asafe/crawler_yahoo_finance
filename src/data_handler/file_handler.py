import csv
import time
from datetime import date
from functools import cache
from pathlib import Path

from data_handler.models import EquitiesSchema
from utils.logger import logger
from utils.settings import settings


@cache
class FileHandler:
    """Handles writing equity data to timestamped CSV files."""

    def __init__(self):
        self.base_path = settings.DATA_PATH
        self.csv_name = settings.CSV_NAME

    def _build_folder_path(self) -> Path:
        """Creates and returns the dated output folder (YYYY/MM/DD)."""
        folder = Path(self.base_path, date.today().strftime("%Y/%m/%d"))
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def _build_file_path(self) -> Path:
        """Returns the full file path with millisecond timestamp suffix."""
        ms = int(time.time() * 1000)
        name = self.csv_name
        return self._build_folder_path() / f"{name}_{ms}.csv"

    def save_csv(self, data: list[EquitiesSchema]) -> None:
        """Writes equity data to a CSV file and logs the output path."""
        path = self._build_file_path()
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["symbol", "name", "price"])
            writer.writeheader()
            writer.writerows([item.model_dump() for item in data])
        logger.info("Saved %s records to %s", len(data), path)


file_handler = FileHandler()