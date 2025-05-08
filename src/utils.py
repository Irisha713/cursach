import datetime
import pandas as pd
import json
import os
from dotenv import load_dotenv
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('C:/Users/Admin/PycharmProjects/cursach/logs/views.log')
logger.addHandler(file_handler)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)


load_dotenv()

api_key = os.getenv("API_CURRENCY_KEY")
api_stocks_key = os.getenv("API_STOCKS_KEY")


def hello():
    """Вывод приветственного сообщения в зависимости от времени"""
    try:
        hours = int(datetime.datetime.now().hour)
        result = ''
        if hours in range(0, 6):
            result = 'Доброй ночи'
        elif hours in range(6, 12):
            result = 'Доброе утро'
        elif hours in range(12, 17):
            result = 'Добрый день'
        elif hours in range(17, 24):
            result = 'Добрый вечер'
        logger.info("Приветствие передано")
        return result
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def card_info(path, date):
    try:
        """Выводим информацию о сумме операции и кэшбеке с номером карты за определённый период"""
        df = pd.read_excel(path).fillna("-")

        end_date = datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S")
        start_date = end_date.replace(day=1)
        df_date = pd.to_datetime(df['Дата операции'], format="%d.%m.%Y %H:%M:%S")

        filtered_df = df[(df_date >= start_date) & (df_date <= end_date)]
        lst_of_operations = filtered_df.to_dict(orient='records')

        result = []

        for operation in lst_of_operations:
            dictionary = {
                    "last_digits": operation['Номер карты'],
                    "total_spent": operation['Сумма операции с округлением'],
                    "cashback": operation['Кэшбэк']
                }
            result.append(dictionary)
        logger.info("Информация об операции, кэшбеке по номеру карты передана")
        return result
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def top_five_transactions(path, date):
    """Выводим 5 транзакций с наивысшей суммой операции за определённый период"""
    try:
        df = (pd.read_excel(path).fillna("-").sort_values
        (by="Сумма операции с округлением", ascending=False))

        end_date = datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S")
        start_date = end_date.replace(day=1)
        df_date = pd.to_datetime(df['Дата операции'], format="%d.%m.%Y %H:%M:%S")

        filtered_df = df[(df_date >= start_date) & (df_date <= end_date)]
        lst_of_operations = filtered_df.to_dict(orient='records')[:5]

        result = []

        for operation in lst_of_operations:
            dictionary = {
                "date": operation['Дата операции'],
                "amount": operation['Сумма платежа'],
                "category": operation['Категория'],
                "description": operation['Описание']
            }
            result.append(dictionary)
        logger.info("5 транзакций переданы")
        return result
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def currency_rates():
    """Выводим стоимость валюты интересную пользователю"""
    try:
        with open("../user_settings.json", 'r') as file:
            data =  json.load(file)
            to_currency = data.get("user_currencies")

        result = []

        for currency in to_currency:
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"

            response = requests.get(url)
            data = response.json()

            response_code = response.status_code
            if response_code == 200:
                exchange_rate = round(data["conversion_rates"].get("RUB"), 2)
                dictionary = {
                    "currency": currency,
                    "rate": exchange_rate
                }
                result.append(dictionary)

        logger.info("Информация передана")
        return result
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def stock_prices():
    """Выводим стоимость акций исходя интересных пользователю"""
    try:
        with open("../user_settings.json", 'r') as file:
            data = json.load(file)
            stocks = data.get("user_stocks")

        result = []

        for stock in stocks:
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_stocks_key}'
            response = requests.get(url)
            data = response.json()

            response_code = response.status_code
            if response_code == 200:
                if data.get("Global Quote").get("01. symbol") == stock:
                    dictionary = {
                        "stock": stock,
                        "price": data.get("Global Quote").get("05. price")
                    }
                    result.append(dictionary)

        logger.info("Стоимость акций передана")
        return result
    except Exception as e:
        logger.error(f"Ошибка: {e}")
