import re
import requests
import unittest
# Проверка и поиск синтаксически корректных почтовых индексов



#российские индексы: 6 цифр, начало не с 0
POSTAL_REGEX = r'\b[1-9]\d{5}\b'


def find_postal_codes(text: str):
    """
Функция ищет все почтовые индексы в переданном тексте.
:return: список найденных индексов
"""
    return re.findall(POSTAL_REGEX, text)


def check_postal_code(code: str) -> bool:
    """
Проверяет, является ли строка корректным почтовым индексом.
    """
    return bool(re.fullmatch(POSTAL_REGEX, code))


def find_postal_codes_from_url(url: str):
    """
    Загружает веб-страницу и ищет индексы в её тексте.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return find_postal_codes(response.text)
    except Exception as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return []


def find_postal_codes_in_file(file_path: str):
    """
    Считывает содержимое файла и ищет индексы.
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            text = file.read()
        return find_postal_codes(text)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


# ----------------------------------------------
# Unit-тесты
# ----------------------------------------------

class TestPostalCodeFunctions(unittest.TestCase):

    def test_valid_codes(self):
        self.assertTrue(check_postal_code("123456"))
        self.assertTrue(check_postal_code("654321"))

    def test_invalid_codes(self):
        self.assertFalse(check_postal_code("012345"))
        self.assertFalse(check_postal_code("12345"))
        self.assertFalse(check_postal_code("12a456"))

    def test_find_postal_codes(self):
        text = "Мой индекс 123456, а у друга 654321."
        result = find_postal_codes(text)
        self.assertEqual(result, ["123456", "654321"])


# ----------------------------------------------
# Пользовательский ввод (для ручного тестирования)
# ----------------------------------------------
if __name__ == "__main__":
    print("=== Проверка почтовых индексов ===")
    print("Выберите режим работы:")
    print("1 — Проверить отдельный индекс")
    print("2 — Найти индексы в тексте")
    print("3 — Найти индексы на веб-странице")
    print("4 — Найти индексы в файле")

    choice = input("Введите номер режима: ")

    if choice == "1":
        code = input("Введите индекс: ")
        if check_postal_code(code):
            print("✅ Индекс корректный.")
        else:
            print("❌ Индекс некорректный.")

    elif choice == "2":
        text = input("Введите текст: ")
        print("Найденные индексы:", find_postal_codes(text))

    elif choice == "3":
        url = input("Введите URL страницы: ")
        print("Найденные индексы:", find_postal_codes_from_url(url))

    elif choice == "4":
        path = input("Введите путь к файлу: ")
        print("Найденные индексы:", find_postal_codes_in_file(path))

    else:
        print("Неизвестная команда.")
