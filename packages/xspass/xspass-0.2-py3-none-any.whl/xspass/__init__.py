from .generator import PasswordGenerator

__version__ = "0.2"

default_generator = PasswordGenerator()

def generate(length=12, **kwargs):
    return default_generator.generate(length=length, **kwargs)

def generate_pin(length=4):
    return default_generator.generate_pin(length)

def generate_memorable(num_words=3):
    return default_generator.generate_memorable(num_words)

def check_strength(password):
    return default_generator.check_strength(password) 