import unittest
from ..validators import correct_username


class TestUsername(unittest.TestCase):
    """Тестируем correct_username."""

    def test_ascii(self):  # Это - test case
        # Вызов тестируемой функции
        call = correct_username('qwerty_123@')
        # Ожидаемый результат
        result = False
        # Проверка: идентичен ли результат вызова ожидаемому результату
        self.assertEqual(
            call, result, 'Функция correct_username не с правильными логинами'
        )

    def test_cyrrilyc(self):  # Это - test case
        # Вызов тестируемой функции
        call = correct_username('Вася')
        # Ожидаемый результат
        result = True
        # Проверка: идентичен ли результат вызова ожидаемому результату
        self.assertEqual(
            call, result, 'Функция correct_username не работает с кириллицей'
        )
