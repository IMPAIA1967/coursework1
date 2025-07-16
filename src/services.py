import logging
import re


# Функция "Простой поиск"
def simple_search(transactions: list[dict], search_string: str) -> list[dict]:
    """ Выполняет поиск строк в категориях и описаниях транзакций, игнорируя регистр символов.
     Возвращает список транзакций, соответствующих указанному шаблону. """

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Фильтрация транзакций по регулярному выражению
    result = [
        transaction
        for transaction in transactions
        if isinstance(transaction.get("Описание", ""), str)
        and pattern.search(transaction.get("Описание", ""))
        or isinstance(transaction.get("Категория", ""), str)
        and pattern.search(transaction.get("Категория", ""))
    ]
    logging.info(f"Возвращаем список транзакций, в категории или описании которых есть -  {search_string}")
    return result
