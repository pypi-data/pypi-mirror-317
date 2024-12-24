import unittest  # стандартный модуль Python для тестирования.
from my_library.module2 import count_words, reverse_string


class TestModule2(unittest.TestCase): # Этот класс наследует unittest.TestCase, что делает его тестовым набором
    def test_count_words(self): # Проверяет корректность работы функции count_words(), которая, предположительно, считает количество слов в строке
        self.assertEqual(count_words("Hello World"), 2) # 2 слова - возвращает значение 2
        self.assertEqual(count_words("Python is awesome"), 3) # 3 слова = 3
        self.assertEqual(count_words(""), 0) # Пустое сообщение = 0
        self.assertEqual(count_words("singleWord"), 1) # 1 слово = 1

    def test_reverse_string(self): # Проверяет функцию reverse_string(), которая должна возвращать строку, записанную в обратном порядке.
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string("Python"), "nohtyP")
        self.assertEqual(reverse_string(""), "")
        self.assertEqual(reverse_string("12345"), "54321")


if __name__ == "__main__": # Запускает тесты, если файл запускается напрямую (например, через команду python test_module2.py).
    unittest.main() # unittest.main() находит все методы, начинающиеся с test_, и запускает их.
