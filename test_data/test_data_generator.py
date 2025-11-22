import random
import string


class CreateUsers:

    @staticmethod
    def get_email():
        # Генерирует уникальный email для каждого вызова
        return f"BoardUser{random.randint(1000, 100000)}@example.com"
    
    @staticmethod
    def get_password():
        # Генерирует пароль для каждого вызова
        return str(random.randint(10, 20))


class CreateAnnouncement:

    @staticmethod
    def get_name():
        # Генерирует уникальное имя объявления для каждого вызова
        return f"Тест - {random.randint(1, 100)}"
    
    @staticmethod
    def get_description():
        # Генерирует описание объявления для каждого вызова
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    
    @staticmethod
    def get_price():
        # Генерирует цену для каждого вызова
        return str(random.randint(10, 999))

