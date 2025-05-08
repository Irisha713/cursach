import re
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('C:/Users/Admin/PycharmProjects/cursach/logs/services.log')
logger.addHandler(file_handler)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)


def return_search(lst):
    """Выводит переводы физическим лицам"""
    result = []
    try:
        for operation in lst:
            if operation['Категория'] == 'Переводы':
                for value in operation.values():
                    search = re.findall(r'^\w+\s\D\.$', str(value))
                    if search:
                        result.append(operation)
        logger.info("Поиск осуществлён")
        return json.dumps(result)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
