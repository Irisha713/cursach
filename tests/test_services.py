import pytest
import json
import re

from src.services import return_search


@pytest.mark.parametrize("lst, expected_contains", [
    (
        [
            {"Категория": "Переводы", "Описание": "Перевод от А. Б.", "Сумма": 100},
            {"Категория": "Покупки", "Описание": "Покупка товара", "Сумма": 50}
        ],
        True
    ),
    (
        [
            {"Категория": "Переводы", "Описание": "Перевод В. В.", "Сумма": 200}
        ],
        True
    ),
])


def test_return_search_found(lst, expected_contains):
    result_json = return_search(lst)
    result = json.loads(result_json)
    assert isinstance(result, list)
    if expected_contains:
        assert all(isinstance(item, dict) for item in result)
        assert all(item['Категория'] == 'Переводы' for item in result)
    else:
        assert result == []


def test_return_search_empty():
    result_json = return_search([])
    result = json.loads(result_json)
    assert result == []


def test_return_search_regex():
    lst = [
        {"Категория": "Переводы", "Описание": "Иванов И.В.", "Сумма": 100},
        {"Категория": "Переводы", "Описание": "Петров П.П.", "Сумма": 150},
        {"Категория": "Переводы", "Описание": "Неправильный формат", "Сумма": 200}
    ]
    result_json = return_search(lst)
    result = json.loads(result_json)
    for item in result:
        description = item.get("Описание", "")
        assert re.findall(r'^\w+\s\D\.$', description)
