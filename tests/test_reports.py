import pytest
from unittest.mock import patch
import pandas as pd
import datetime

from src.reports import day_spending


@pytest.fixture
def sample_df():
    data = {
        "Дата операции": [
            "01.01.2023 12:00:00",
            "15.02.2023 15:30:00",
            "28.02.2023 09:45:00",
            "10.03.2023 20:00:00",
            "05.03.2023 10:10:10"
        ],
        "Сумма операции": [100, 200, 150, 300, 250]
    }
    df = pd.DataFrame(data)
    return df


def test_day_spending_exception(sample_df):
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime.datetime(2023, 3, 15)
        mock_datetime.strptime.side_effect = ValueError("Некорректный формат даты")
        with patch('logging.Logger.error') as mock_error:
            result = day_spending(sample_df, user_date="неправильная дата")
            assert result is None
            mock_error.assert_called()


def test_file_write_called(sample_df, caplog):
    with patch('builtins.open', create=True) as mock_open, \
         patch('json.dump') as mock_dump, \
         patch('logging.Logger.info') as mock_info:
        result = day_spending(sample_df)
        mock_open.assert_called_with("../data/report.json", 'w', encoding='utf-8')
        mock_dump.assert_called()
        mock_info.assert_any_call("Затраты возвращены")
        assert isinstance(result, pd.DataFrame)
