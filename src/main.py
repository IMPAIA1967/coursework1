import json
import os

from dotenv import load_dotenv

from reports import spending_by_category
from services import simple_search
from utils import reading_xlsx
from views import main_view

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, "data", "operations.xlsx")


if __name__ == "__main__":

    input_date = "2021-12-31 16:00:00"
    result = main_view(input_date)
    # print(json.dumps(result, ensure_ascii=False, indent=2))

    df = reading_xlsx(FILE_PATH)
    transactions = df.to_dict(orient="records")

    # Простой поиск
    print("\n=== Простой поиск ===")
    use_search = input("Хотите выполнить простой поиск? (да/нет): ").strip().lower()
    if use_search in ("да", "д", "yes", "y"):
        query = input("Введите слово для поиска в описании или категории: ").strip().lower()
        search_results = simple_search(transactions, query)
        if search_results:
            print(json.dumps(search_results[:3], ensure_ascii=False, indent=2))
        else:
            print("Ничего не найдено по вашему запросу.")
    else:
        print("Простой поиск пропущен.")

    # Получение даты от пользователя
    date_input = input("Введите дату (в формате YYYY-MM-DD) или нажмите Enter для текущей даты: ")
    date = date_input if date_input else None

    # Отчет по категории
    category = input("Сформировать отчет по категории? (введите категорию или оставьте пустым): ").strip().lower()
    if category.lower() not in ["нет", "no"]:
        """Формируем отчёт по конкретной категории расходов,
         предоставляя пользователю удобный интерфейс ввода нужной категории.
        """
        print(f"\n=== Отчет: Траты по категории '{category}' ===")
        report = spending_by_category(df, category, date, save_to_file=False)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("\n=== Отчет о тратах по категории не требуется ===")
