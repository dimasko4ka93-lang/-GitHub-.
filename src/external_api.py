import xml.etree.ElementTree as ET

import requests


def get_transaction_amount_in_rub(transaction: dict) -> float:
    """
    Принимает транзакцию, возвращает сумму в рублях (float).
    Для USD/EUR обращается к API ЦБ РФ.
    """
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    response.encoding = "windows-1251"

    root = ET.fromstring(response.text)

    for valute in root.findall("Valute"):
        char_code_elem = valute.find("CharCode")
        value_elem = valute.find("Value")
        nominal_elem = valute.find("Nominal")

        # Проверяем, что элементы существуют
        if char_code_elem is None or value_elem is None or nominal_elem is None:
            continue

        # Проверяем, что текст существует
        if (char_code_elem.text is None or value_elem.text is None
                or nominal_elem.text is None):
            continue

        char_code = char_code_elem.text
        if char_code == currency:
            value = float(value_elem.text.replace(",", "."))
            nominal = int(nominal_elem.text)
            rate = value / nominal
            return round(amount * rate, 2)

    print(f"Валюта {currency} не найдена в API ЦБ РФ")
    return 0.0
