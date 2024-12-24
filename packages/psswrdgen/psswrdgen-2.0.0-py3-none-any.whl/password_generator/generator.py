import random
import string


class PasswordGenerator:
    def __init__(self, length=12, include_uppercase=True, include_digits=True, include_special=True):
        """
        Инициализация генератора паролей.

        :param length: Длина пароля (по умолчанию 12).
        :param include_uppercase: Включать ли заглавные буквы (по умолчанию True).
        :param include_digits: Включать ли цифры (по умолчанию True).
        :param include_special: Включать ли специальные символы (по умолчанию True).
        """
        self.length = length
        self.include_uppercase = include_uppercase
        self.include_digits = include_digits
        self.include_special = include_special

    def generate(self):
        """
        Генерация пароля в соответствии с заданными настройками.

        :return: Сгенерированный пароль (строка).
        """
        if self.length < 1:
            raise ValueError("Длина пароля должна быть не менее 1 символа.")

        char_pool = string.ascii_lowercase
        if self.include_uppercase:
            char_pool += string.ascii_uppercase
        if self.include_digits:
            char_pool += string.digits
        if self.include_special:
            char_pool += string.punctuation

        if not char_pool:
            raise ValueError("Необходимо выбрать хотя бы один тип символов для генерации пароля.")

        return ''.join(random.choice(char_pool) for _ in range(self.length))
