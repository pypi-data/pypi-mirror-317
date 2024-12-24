import string
import random
import secrets
import re
from typing import List, Dict, Optional

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.similar_chars = "iI1loO0"
        self.ambiguous = "`{}[]()/\'\"\\~,;:.<>"
        
    def generate(self, 
                length: int = 12, 
                use_upper: bool = True,
                use_digits: bool = True, 
                use_special: bool = True,
                min_of_each: int = 1,
                avoid_similar: bool = False,
                avoid_ambiguous: bool = False,
                use_secrets: bool = True) -> str:
        """
        Расширенная генерация пароля с дополнительными опциями
        
        Args:
            length: Длина пароля
            use_upper: Использовать заглавные буквы
            use_digits: Использовать цифры
            use_special: Использовать специальные символы
            min_of_each: Минимальное количество символов каждого типа
            avoid_similar: Избегать похожих символов (1,l,I,0,O,o)
            avoid_ambiguous: Избегать неоднозначных символов
            use_secrets: Использовать модуль secrets вместо random
        """
        chars = self.lowercase
        required_chars = []
        
        # Удаляем похожие символы если нужно
        if avoid_similar:
            chars = ''.join(c for c in chars if c not in self.similar_chars)
            
        # Удаляем неоднозначные символы
        if avoid_ambiguous:
            chars = ''.join(c for c in chars if c not in self.ambiguous)
            
        # Добавляем обязательные символы нижнего регистра
        required_chars.extend(self._get_random_chars(chars, min_of_each, use_secrets))
            
        if use_upper:
            upper_chars = self.uppercase
            if avoid_similar:
                upper_chars = ''.join(c for c in upper_chars if c not in self.similar_chars)
            chars += upper_chars
            required_chars.extend(self._get_random_chars(upper_chars, min_of_each, use_secrets))
            
        if use_digits:
            digit_chars = self.digits
            if avoid_similar:
                digit_chars = ''.join(c for c in digit_chars if c not in self.similar_chars)
            chars += digit_chars
            required_chars.extend(self._get_random_chars(digit_chars, min_of_each, use_secrets))
            
        if use_special:
            special_chars = self.special
            if avoid_ambiguous:
                special_chars = ''.join(c for c in special_chars if c not in self.ambiguous)
            chars += special_chars
            required_chars.extend(self._get_random_chars(special_chars, min_of_each, use_secrets))

        remaining_length = length - len(required_chars)
        if remaining_length < 0:
            raise ValueError("Длина пароля слишком мала для указанных требований")
            
        # Добавляем оставшиеся символы
        if use_secrets:
            password_chars = required_chars + [secrets.choice(chars) for _ in range(remaining_length)]
            secrets.SystemRandom().shuffle(password_chars)
        else:
            password_chars = required_chars + [random.choice(chars) for _ in range(remaining_length)]
            random.shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def _get_random_chars(self, chars: str, count: int, use_secrets: bool) -> List[str]:
        """Получить случайные символы из строки"""
        if use_secrets:
            return [secrets.choice(chars) for _ in range(count)]
        return [random.choice(chars) for _ in range(count)]
    
    def generate_memorable(self, num_words: int = 3, separator: str = "-", capitalize: bool = True) -> str:
        """Генерация запоминающегося пароля из слов"""
        # Здесь можно добавить свой словарь слов или использовать библиотеку words
        words = ["apple", "banana", "orange", "grape", "lemon", "mango", "kiwi", "plum"]
        selected_words = []
        
        for _ in range(num_words):
            word = random.choice(words)
            if capitalize:
                word = word.capitalize()
            selected_words.append(word)
            
        return separator.join(selected_words)
    
    def generate_pin(self, length: int = 4) -> str:
        """Генерация PIN-кода"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    def check_strength(self, password: str) -> Dict[str, any]:
        """Проверка надежности пароля"""
        strength = {
            'length': len(password) >= 12,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'digits': bool(re.search(r'\d', password)),
            'special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', password)),
            'score': 0
        }
        
        # Подсчет общего балла
        strength['score'] = sum([
            len(password) >= 12,
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'\d', password)),
            bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', password))
        ])
        
        return strength
    
    def generate_by_pattern(self, pattern: str) -> str:
        """
        Генерация пароля по шаблону
        A - заглавная буква
        a - строчная буква
        # - цифра
        ? - специальный символ
        Пример: 'Aa##??'
        """
        result = []
        for char in pattern:
            if char == 'A':
                result.append(secrets.choice(self.uppercase))
            elif char == 'a':
                result.append(secrets.choice(self.lowercase))
            elif char == '#':
                result.append(secrets.choice(self.digits))
            elif char == '?':
                result.append(secrets.choice(self.special))
            else:
                result.append(char)
        return ''.join(result)

    def generate_passphrase(self, 
                          words: int = 4, 
                          separator: str = " ", 
                          add_number: bool = True,
                          add_special: bool = True) -> str:
        """Генерация парольной фразы"""
        # Здесь можно добавить большой словарь слов
        word_list = ["correct", "horse", "battery", "staple", "apple", "banana"]
        passphrase = []
        
        for _ in range(words):
            word = secrets.choice(word_list)
            if random.random() > 0.5:
                word = word.capitalize()
            passphrase.append(word)
            
        if add_number:
            passphrase.append(str(random.randint(0, 999)))
            
        if add_special:
            passphrase.append(secrets.choice(self.special))
            
        return separator.join(passphrase)