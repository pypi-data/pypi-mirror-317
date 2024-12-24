import unittest # стандартный модуль Python для тестирования.
from my_library.module1 import add, subtract

class TestModule1(unittest.TestCase): # Класс, наследующий unittest.TestCase, чтобы стать тестовым набором
    def test_add(self): # проверяет, что результат совпадает с ожидаемым.
        self.assertEqual(add(2, 3), 5) # 2 + 3 = 5
        self.assertEqual(add(-1, 1), 0) # -1 + 1 = 0

    def test_subtract(self): # Проверяет корректность функции вычитания
        self.assertEqual(subtract(5, 3), 2) # 5 - 3 = 2
        self.assertEqual(subtract(0, 1), -1) # 0 - 1 = -1

if __name__ == "__main__":
    unittest.main() #Этот блок позволяет запускать тесты из командной строки
