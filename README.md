# Курсовая работа

## Описание:

Приложение для анализа транзакций, которые находятся в Excel-файле. 
Приложение генерирует JSON-данные для веб-страниц, 
формирует Excel-отчеты,
предоставляет другие сервисы.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/username/project.git
```

2. Установите зависимости:
```
pip install -r requirements.txt
```

3. Создайте базу данных и выполните миграции:
```
python manage.py migrate
```

4. Запустите локальный сервер:
```
python manage.py runserver
```
## Использование:

Примеры использования функций:

```python
from src.views import main_view
from src.services import return_search
from src.reports import day_spending
import pandas as pd

df = pd.read_excel("../data/operations.xlsx")

# Пример использования day_spending
day_spending(df)

# Пример использования main_view
main_view("../data/operations.xlsx", "2019.5.17 0:0:0")

# Пример использования return_search
return_search(df)
```

## Тестирование

```
Name              Stmts   Miss  Cover
-------------------------------------
src\__init__.py       0      0   100%
src\reports.py       52      6    88%
src\services.py      22      3    86%
src\utils.py        103     20    81%
-------------------------------------
TOTAL               177     29    84%
