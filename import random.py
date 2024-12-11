import random
import string
from datetime import datetime

class PasswordUtils:
    @staticmethod
    def generate_password(length, include_uppercase, include_numbers, include_special, custom_keywords):
        if length < 4:
            raise ValueError("Длина пароля должна быть не менее 4 символов")
        
        # Ограничение на максимальную длину пароля
        if length > 50:
            raise ValueError("Длина пароля не может превышать 50 символов")

        if not (include_uppercase or include_numbers or include_special or custom_keywords):
            raise ValueError("Необходимо выбрать хотя бы одну категорию символов или добавить ключевые слова")

        char_pool = string.ascii_lowercase
        required_chars = []

        if include_uppercase:
            char_pool += string.ascii_uppercase
            required_chars.append(random.choice(string.ascii_uppercase))

        if include_numbers:
            char_pool += string.digits
            required_chars.append(random.choice(string.digits))

        if include_special:
            char_pool += "!@#$%^&*()-_=+"
            required_chars.append(random.choice("!@#$%^&*()-_=+"))

        # Добавляем пользовательские ключевые слова в список
        if custom_keywords:
            custom_keywords_list = custom_keywords.split()
            required_chars += custom_keywords_list
        
        remaining_length = length - len(required_chars)
        password = [random.choice(char_pool) for _ in range(remaining_length)]

        password += required_chars
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def evaluate_password(password):
        length_score = len(password) >= 8
        has_upper = any(char.isupper() for char in password)
        has_number = any(char.isdigit() for char in password)
        has_special = any(char in "!@#$%^&*()-_=+" for char in password)

        score = sum([length_score, has_upper, has_number, has_special])
        
        if score == 4:
            return "Надежный"
        elif score == 3:
            return "Средний"
        else:
            return "Слабый"

    @staticmethod
    def calculate_crack_time(password, include_uppercase, include_numbers, include_special):
        length = len(password)

        # Количество символов в наборе
        char_set = string.ascii_lowercase  # малые буквы

        if include_uppercase:
            char_set += string.ascii_uppercase  # заглавные буквы
        if include_numbers:
            char_set += string.digits  # цифры
        if include_special:
            char_set += "!@#$%^&*()-_=+"  # специальные символы

        # Количество возможных комбинаций
        num_combinations = len(char_set)  length

        # Время для взлома (предполагается, что устройство проверяет 100 миллиардов паролей в секунду)
        guesses_per_second = 10  11  # 100 миллиардов паролей в секунду
        time_seconds = num_combinations / guesses_per_second

        # Переводим время в более удобный формат (секунды, минуты, часы, дни, годы)
        if time_seconds < 60:
            return f"{time_seconds:.2f} секунд"
        elif time_seconds < 3600:
            return f"{(time_seconds / 60):.2f} минут"
        elif time_seconds < 86400:
            return f"{(time_seconds / 3600):.2f} часов"
        elif time_seconds < 31536000:  # меньше года (секунды в году)
            return f"{(time_seconds / 86400):.2f} дней"
        elif time_seconds < 315360000:  # меньше 10 лет
            return f"{(time_seconds / 31536000):.2f} лет"
        else:
            return "Больше 10 лет"

@staticmethod
    def save_password_to_file(password, custom_keywords):
        try:
            # Открываем файл для записи с кодировкой UTF-8
            with open("generated_passwords.txt", "a", encoding="utf-8") as file:
                # Получаем текущую дату и время
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Записываем в файл
                file.write(f"{current_time} | Пароль: {password} | Ключевые слова: {custom_keywords}\n")
        except Exception as e:
            raise ValueError(f"Произошла ошибка при сохранении пароля: {e}")