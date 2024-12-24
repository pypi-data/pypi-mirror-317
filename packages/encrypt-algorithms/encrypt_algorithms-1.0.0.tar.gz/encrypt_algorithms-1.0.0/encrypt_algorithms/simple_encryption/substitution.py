import string
from random import shuffle
import re

alphabet = string.ascii_letters


def create_key(alphabet):
    alphabet = list(alphabet)
    shuffle(alphabet)
    return "".join(alphabet)


def encrypt_substitution(message, key):
    # Проверяем, что сообщение содержит только допустимые символы
    if re.search(r"[^\s" + re.escape(string.ascii_letters + string.punctuation) + "]", message):
        raise ValueError("Ошибка: Сообщение содержит недопустимые символы (например, кириллицу).")

    key_map = dict(zip(alphabet, key))
    return "".join(key_map.get(char, char) for char in message)


def decrypt_substitution(encrypted_message, key):
    # Проверяем, что зашифрованное сообщение содержит только допустимые символы
    if re.search(r"[^\s" + re.escape(string.ascii_letters + string.punctuation) + "]", encrypted_message):
        raise ValueError("Ошибка: Зашифрованное сообщение содержит недопустимые символы.")

    reverse_key_map = dict(zip(key, alphabet))
    return "".join(reverse_key_map.get(char, char) for char in encrypted_message)
