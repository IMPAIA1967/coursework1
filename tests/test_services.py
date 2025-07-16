import pytest

from src.services import simple_search

sample_data = [
    {"Дата операции": "2021-12-10", "Сумма операции": -1000.0, "Категория": "Супермаркеты", "Описание": "Пятёрочка"},
    {
        "Дата операции": "2021-12-11",
        "Сумма операция": -200.0,
        "Категория": "Связь",
        "Описание": "МТС Mobile +7 981 333-44-55",
    },
    {"Дата операция": "2021-12-15", "Сумма операция": -500.0, "Категория": "Переводы", "Описание": "Иван С."},
    {
        "Дата операция": "2021-12-20",
        "Сумма операция": 3000.0,
        "Категория": "Пополнения",
        "Описание": "Пополнение через банкомат",
    },
]


def test_simple_search_found_category():
    result = simple_search(sample_data, "СВ")
    assert result == [sample_data[1]]


def test_simple_search_not_found_descr():
    result = simple_search(sample_data, "Пупупу")
    assert result == []
