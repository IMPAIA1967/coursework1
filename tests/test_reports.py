import pandas as pd
import pytest

from src.reports import save_report, spending_by_category


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "Дата операции": [
                "2024-10-01",
                "2024-10-02",
                "2024-10-03",
                "2024-11-01",
                "2024-11-02",
                "2024-11-03",
                "2024-12-01",
                "2024-12-02",
                "2024-12-03",
            ],
            "Сумма платежа": [-100, -200, -300, -400, -500, -600, -700, -800, -900],
            "Категория": [
                "Супермаркеты",
                "Супермаркеты",
                "Кафе",
                "Супермаркеты",
                "Кафе",
                "Супермаркеты",
                "Кафе",
                "Супермаркеты",
                "Супермаркеты",
            ],
            "Описание": [
                "Магнит",
                "Пятерочка",
                "Кофейня",
                "Перекресток",
                "Шоколадница",
                "Ашан",
                "Кофейня",
                "Metro",
                "FixPrice",
            ],
        }
    )


def test_spending_by_category(sample_df):
    result = spending_by_category(sample_df, "Супермаркеты", "2024-12-01", save_to_file=False)
    assert isinstance(result, list)
    for row in result:
        assert "date" in row and "amount" in row and "description" in row
        assert row["amount"] < 0


def test_save_report_creates_file(tmp_path):
    @save_report(filename=str(tmp_path / "test_report.json"))
    def dummy_report(save_to_file=False):
        _ = save_to_file  # подавляет предупреждение линтера
        return {"example": 1}

    dummy_report(save_to_file=True)
    file_path = tmp_path / "test_report.json"
    assert file_path.exists()

    with open(file_path, encoding="utf-8") as f:
        data = f.read()
        assert '"example": 1' in data
