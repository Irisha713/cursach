import datetime
import pandas as pd
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('C:/Users/Admin/PycharmProjects/cursach/logs/views.log')
logger.addHandler(file_handler)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)

func_df = pd.read_excel("../cursach/data/operations.xlsx").fillna("-")


def file_decorator(filename="../cursach/data/report.json"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                logger.info(f"Функция начала выполнение")
                result = func(*args, **kwargs)

                if result is not None:
                    if isinstance(result, pd.DataFrame):
                        with open(filename, 'w', encoding='utf-8') as file:
                            json.dump(result.to_dict(orient="records"), file, ensure_ascii=False, indent=4)
                        logger.info(f"Результат функции записан в файл {filename}")
                    else:
                        logger.warning("Результат функции не является DataFrame и не может быть записан в файл.")
                else:
                    logger.warning("Результат функции пустой (None).")

                return result
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                return None
        return wrapper
    return decorator


@file_decorator(filename="../data/report.json")
def day_spending(df, user_date=None):
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца от переданной даты"""
    try:
        if user_date:
            date = datetime.datetime.strptime(user_date, "%d.%m.%Y %H:%M:%S")
        else:
            date = datetime.datetime.now()

        df_date = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        months = date.month
        if months < 3:
            years = date.year
            start_date = date.replace(year=years - 1, month=months + 10, day=1, hour=0, minute=0, second=0,
                                      microsecond=0)
        else:
            start_date = date.replace(month=months - 2, day=1, hour=0, minute=0, second=0, microsecond=0)

        filtered_df = df[(df_date >= start_date) & (df_date <= date)].copy()
        filtered_df.loc[:, 'День недели'] = df_date.apply(lambda x: x.weekday())  # Вычисление дня недели

        result = filtered_df.groupby('День недели')['Сумма операции'].mean().reset_index()
        result.columns = ['День недели', 'Итоговые траты']
        result = result.sort_values(by='День недели').reset_index(drop=True)

        logger.info("Затраты возвращены")
        return result
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return None
