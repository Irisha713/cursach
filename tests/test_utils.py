import pytest
from unittest.mock import patch, MagicMock, mock_open
from src.utils import *


@pytest.fixture
def sample_excel_file(tmp_path):
    data = {
        'Дата операции': ['15.03.2024 14:00:00', '05.03.2024 09:00:00', '20.03.2024 21:00:00'],
        'Номер карты': ['1234', '5678', '9012'],
        'Сумма операции с округлением': [1000, 2500, 1500],
        'Кэшбэк': [10, 25, 15],
        'Сумма платежа': [990, 2480, 1490],
        'Категория': ['Еда', 'Путешествия', 'Магазин'],
        'Описание': ['Ресторан', 'Билет', 'Продукты']
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "sample_data.xlsx"
    df.to_excel(file_path, index=False)
    return str(file_path)


def test_hello_returns_string():
    result = hello()
    assert isinstance(result, str)
    assert result in ['Доброй ночи', 'Доброе утро', 'Добрый день', 'Добрый вечер']


@pytest.fixture
def sample_df():
    data = {
        'Дата операции': ['01.01.2023 10:00:00', '15.01.2023 12:00:00'],
        'Номер карты': ['1234', '5678'],
        'Сумма операции с округлением': [100.0, 200.0],
        'Кэшбэк': [10.0, 20.0]
    }
    df = pd.DataFrame(data)
    return df


def test_card_info_valid(sample_excel_file):
    result = card_info(sample_excel_file, '2024.03.31 23:59:59')
    assert isinstance(result, list)
    assert len(result) == 3
    for item in result:
        assert "last_digits" in item
        assert "total_spent" in item
        assert "cashback" in item


def test_card_info_handles_exception():
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = Exception("error")
        result = card_info('fake_path.xlsx', '2023.01.15 23:59:59')
        assert result is None


@pytest.fixture
def sample_df_sorted():
    data = {
        'Дата операции': ['01.01.2023 10:00:00', '05.01.2023 12:00:00', '10.01.2023 15:00:00'],
        'Сумма операции с округлением': [300, 500, 400],
        'Сумма платежа': [30, 50, 40],
        'Категория': ['cat1', 'cat2', 'cat3'],
        'Описание': ['desc1', 'desc2', 'desc3']
    }
    df = pd.DataFrame(data)
    return df


def test_top_five_transactions_handles_exception():
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = Exception("error")
        result = top_five_transactions('fake_path.xlsx', '2023.01.15 23:59:59')
        assert result is None


def test_currency_rates_success():
    sample_json = {
        "conversion_rates": {
            "RUB": 75.25
        }
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_json
    mock_file = mock_open(read_data=json.dumps({"user_currencies": ["USD", "EUR"]}))

    with patch('builtins.open', mock_file), \
         patch('requests.get', return_value=mock_response):
        result = currency_rates()
        assert isinstance(result, list)
        assert len(result) == 2
        for item in result:
            assert 'currency' in item
            assert 'rate' in item
            assert item['rate'] == round(75.25, 2)


def test_currency_rates_failure():
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.json.return_value = {}
    with patch('builtins.open', mock_open(read_data=json.dumps({"user_currencies": ["USD"]}))), \
         patch('requests.get', return_value=mock_response):
        result = currency_rates()
        assert result == []


def test_stock_prices_success():
    sample_json = {
        "Global Quote": {
            "01. symbol": "AAPL",
            "05. price": "150.00"
        }
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_json
    mock_file = mock_open(read_data=json.dumps({"user_stocks": ["AAPL", "GOOG"]}))

    with patch('builtins.open', mock_file), \
         patch('requests.get', return_value=mock_response):
        result = stock_prices()
        assert isinstance(result, list)
        assert all('stock' in item and 'price' in item for item in result)


def test_stock_prices_mismatched_symbol():
    sample_json = {
        "Global Quote": {
            "01. symbol": "MSFT",
            "05. price": "250.00"
        }
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_json
    with patch('builtins.open', mock_open(read_data=json.dumps({"user_stocks": ["AAPL"]}))), \
         patch('requests.get', return_value=mock_response):
        result = stock_prices()
        assert result == []
