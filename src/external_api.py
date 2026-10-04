import xml.etree.ElementTree as ET

import requests


def get_transaction_amount_in_rub(transaction: dict) -> float:
    """
    Принимает транзакцию, возвращает сумму в рублях (float).
    Для USD/EUR обращается к API ЦБ РФ.
    """
    # 1. Получаем сумму и валюту
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    # 2. Если RUB — возвращаем сразу
    if currency == "RUB":
        return amount

    # 3. Запрос к API ЦБ РФ (XML, без ключа)
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    response.encoding = "windows-1251"

    # 4. Парсим XML
    root = ET.fromstring(response.text)

    # 5. Ищем курс нужной валюты
    for valute in root.findall("Valute"):
        char_code = valute.find("CharCode").text
        if char_code == currency:
            value = float(valute.find("Value").text.replace(",", "."))
            nominal = int(valute.find("Nominal").text)
            rate = value / nominal
            return round(amount * rate, 2)

    # 6. Если валюта не найдена — ошибка
    print(f"Валюта {currency} не найдена в API ЦБ РФ")
