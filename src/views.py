from src.utils import hello, card_info, top_five_transactions, currency_rates, stock_prices
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("C:/Users/Admin/PycharmProjects/cursach/logs/views.log")
logger.addHandler(file_handler)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)


def main_view(path, date):
    """Функции для вкладки 'Главная'"""
    try:
        output = {
            "hello": hello(),
            "card_info": card_info(path, date),
            "top_five_transactions": top_five_transactions(path, date),
            "currency_rates": currency_rates(),
            "stock_prices": stock_prices(),
        }
        logger.info("Данные отправлены")
        return json.dumps(output, ensure_ascii=False)
    except Exception as error:
        logger.error(f"Ошибка: {error}")
