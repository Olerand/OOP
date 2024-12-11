import unittest
from password_utils import PasswordUtils

class TestPasswordUtils(unittest.TestCase):

    def test_generate_password_invalid_length(self):
        # Тестируем, что ошибка возникает, если длина пароля меньше 4
        with self.assertRaises(ValueError):
            PasswordUtils.generate_password(3, True, True, True, "keyword")

    def test_generate_password_invalid_custom_keywords(self):
        # Тестируем, что ошибка возникает, если не выбраны никакие параметры
        with self.assertRaises(ValueError):
            PasswordUtils.generate_password(8, False, False, False, "")

    def test_generate_password_no_uppercase(self):
        # Тестируем, что пароль без заглавных букв
        password = PasswordUtils.generate_password(8, False, True, True, "keyword")
        self.assertFalse(any(c.isupper() for c in password), "Пароль должен содержать только строчные буквы")
    
    def test_generate_password_with_numbers(self):
        # Тестируем, что пароль содержит цифры
        password = PasswordUtils.generate_password(8, True, True, True, "keyword")
        self.assertTrue(any(c.isdigit() for c in password), "Пароль должен содержать цифры")
    
    def test_calculate_crack_time(self):
        # Тестируем расчет времени взлома для пароля
        password = "A1b2C3d4"
        time = PasswordUtils.calculate_crack_time(password, True, True, True)
        self.assertIsInstance(time, str, "Время взлома должно быть строкой")
    
    def test_save_password_to_file(self):
        # Тестируем сохранение пароля в файл
        password = "A1b2C3d4"
        custom_keywords = "keyword"
        try:
            PasswordUtils.save_password_to_file(password, custom_keywords)
            # Проверяем, что файл существует и содержит данные
            with open("generated_passwords.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                self.assertGreater(len(lines), 0, "Файл не должен быть пустым")
        except Exception as e:
            self.fail(f"Ошибка при сохранении пароля в файл: {e}")
    
    def test_generate_password_no_special_chars(self):
        # Тестируем отсутствие специальных символов
        password = PasswordUtils.generate_password(8, True, True, False, "keyword")
        self.assertNotIn("!", password, "Пароль не должен содержать специальные символы")
        self.assertNotIn("@", password, "Пароль не должен содержать специальные символы")

if __name__ == '__main__':
    unittest.main()
