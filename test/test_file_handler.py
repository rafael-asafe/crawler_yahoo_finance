import csv
from datetime import date
from pathlib import Path


def get_csv_file(tmp_path) -> Path:
    folder = tmp_path / date.today().strftime("%Y/%m/%d")
    files = list(folder.glob("*.csv"))
    assert len(files) == 1, f"Expected 1 CSV, found {len(files)}"
    return files[0]


def test_save_csv_creates_file(tmp_path, handler, equity):
    handler.save_csv([equity])

    assert get_csv_file(tmp_path).exists()


def test_save_csv_filename_has_ms_timestamp(tmp_path, handler, equity):
    handler.save_csv([equity])

    name = get_csv_file(tmp_path).name
    assert name.startswith("equities.csv_")
    assert name.endswith(".csv")
    ms_part = name.removeprefix("equities.csv_").removesuffix(".csv")
    assert ms_part.isdigit()


def test_save_csv_header(tmp_path, handler, equity):
    handler.save_csv([equity])

    with open(get_csv_file(tmp_path), encoding="utf-8") as f:
        header = next(csv.reader(f))

    assert header == ["symbol", "name", "price"]


def test_save_csv_content(tmp_path, handler, equities):
    handler.save_csv(equities)

    with open(get_csv_file(tmp_path), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert rows[0]["symbol"] == equities[0].symbol
    assert rows[1]["symbol"] == equities[1].symbol
    assert float(rows[1]["price"]) == equities[1].price


def test_save_csv_creates_nested_dirs(tmp_path, handler, equity):
    handler.save_csv([equity])

    assert (tmp_path / date.today().strftime("%Y/%m/%d")).is_dir()