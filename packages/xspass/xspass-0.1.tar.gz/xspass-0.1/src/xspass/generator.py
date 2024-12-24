import string
import random

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate(self, length=12, use_upper=True, use_digits=True, 
                use_special=True, min_of_each=1):
        """
        Генерирует случайный пароль с заданными параметрами
        
        Args:
            length (int): Длина пароля
            use_upper (bool): Использовать заглавные буквы
            use_digits (bool): Использовать цифры
            use_special (bool): Использовать специальные символы
            min_of_each (int): Минимальное количество символов каждого типа
            
        Returns:
            str: Сгенерированный пароль
        """
        chars = self.lowercase
        required_chars = [random.choice(self.lowercase)]
        
        if use_upper:
            chars += self.uppercase
            required_chars.extend([random.choice(self.uppercase)] * min_of_each)
            
        if use_digits:
            chars += self.digits
            required_chars.extend([random.choice(self.digits)] * min_of_each)
            
        if use_special:
            chars += self.special
            required_chars.extend([random.choice(self.special)] * min_of_each)

        remaining_length = length - len(required_chars)
        if remaining_length < 0:
            raise ValueError("Длина пароля слишком мала для указанных требований")
            
        password_chars = required_chars + [random.choice(chars) for _ in range(remaining_length)]
        random.shuffle(password_chars)
        
        return ''.join(password_chars) 