from unittest.mock import MagicMock, patch

from src.file_readers import read_csv, read_xlsx


@patch("src.file_readers.pd.read_csv")
def test_read_csv_valid_file(mock_read_csv):
    """Читает CSV с помощью mock."""
    # Настраиваем mock
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    mock_read_csv.return_value = mock_df

    result = read_csv("fake.csv")

    assert len(result) == 2
    assert result[0]["state"] == "EXECUTED"
    mock_read_csv.assert_called_once_with("fake.csv", sep=";")


@patch("src.file_readers.pd.read_csv")
def test_read_csv_not_found(mock_read_csv):
    """Несуществующий файл → []."""
    mock_read_csv.side_effect = OSError("File not found")

    result = read_csv("nonexistent.csv")
    assert result == []


@patch("src.file_readers.pd.read_excel")
def test_read_xlsx_valid_file(mock_read_excel):
    """Читает XLSX с помощью mock."""
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    mock_read_excel.return_value = mock_df

    result = read_xlsx("fake.xlsx")

    assert len(result) == 2
    assert result[0]["state"] == "EXECUTED"
    mock_read_excel.assert_called_once_with("fake.xlsx")


@patch("src.file_readers.pd.read_excel")
def test_read_xlsx_not_found(mock_read_excel):
    """Несуществующий файл → []."""
    mock_read_excel.side_effect = OSError("File not found")

    result = read_xlsx("nonexistent.xlsx")
    assert result == []
