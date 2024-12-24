# Monobank Tool
Бібліотека Monobank Tool - це Pure Python рішення для роботи з усіма частинами Monobank API

## Встановлення
Ви можете встановити бібліотеку за допомогою `pip`:

```bash
pip install monobank-tool
```
## Робота з API
Кожна група ендпоїнтів в Monobank має свій клас для роботи
### Acquiring API
Відповідає за роботу еквайринга: https://api.monobank.ua/docs/acquiring.html
```python
from monobank.api import AcquiringAPI

# Ініціалізуйте API з вашим API-ключем
api_key = "YOUR_MONOBANK_API_KEY"
acquiring_api = AcquiringAPI(api_key=api_key)
```

### Personal API (WiP)
Відповідає за роботу з особистими даними користувача: https://api.monobank.ua/docs/index.html

**УВАГА!** Цей функціонал ще не реалізований

```python
from monobank.api import PersonalAPI

# Ініціалізуйте API з вашим API-ключем
api_key = "YOUR_MONOBANK_API_KEY"
personal_api = PersonalAPI(api_key=api_key)
```

### Corporate API (WiP)
Відповідає за роботу для провайдерів: https://api.monobank.ua/docs/corporate.html

**УВАГА!** Цей функціонал ще не реалізований

```python
from monobank.api import CorporateAPI

# Ініціалізуйте API з вашим API-ключем
api_key = "YOUR_MONOBANK_API_KEY"
corporate_api = CorporateAPI(api_key=api_key)
```


## Приклад роботи
Структура фасадів відповідає шляху до ендпоїнтів Monobank API.  
Тобто якщо вам треба зробити запит на `https://api.monobank.ua/merchant/invoice/create`, ви маєте використати метод `AcquiringAPI.merchant.invoice.create`.

Кожен метод приймає як аргумент `params` та `data` (якщо потрібно).
* `params` - це словник, для передачі параметрів запиту (query params)
* `data` - це словник, для передачі даних запиту (request body)

Наприклад, для роботи з рахунками (invoices) ви можете використовувати наступний код:

```python
from monobank.api import AcquiringAPI

# Ініціалізуйте API з вашим API-ключем
api_key = "YOUR_MONOBANK_API_KEY"
acquiring_api = AcquiringAPI(api_key=api_key)

# Створення нового рахунку
invoice_data = {
    "amount": 50000,
    "ccy": 980,
    "merchantPaymInfo": {
        "destination": "Місячна підписка на сервіс",
        "comment": "Місячна підписка на сервіс",
        "basketOrder": [
            {
                "name": "Місячна підписка",
                "qty": 1,
                "sum": 50000,
                "icon": "string",
                "unit": "шт.",
                "code": "month-subscription"
            }
        ]
    },
    "paymentType": "debit"
}
response = acquiring_api.merchant.invoice.create(data=invoice_data)
print(response)

# Перевірка статусу рахунку
params = {"invoice_id": "12345"}
status = acquiring_api.merchant.invoice.status(params=params)
print(status)

# Інвалідація рахунку
cancel_response = acquiring_api.merchant.invoice.remove(data=params)
print(cancel_response)
```
