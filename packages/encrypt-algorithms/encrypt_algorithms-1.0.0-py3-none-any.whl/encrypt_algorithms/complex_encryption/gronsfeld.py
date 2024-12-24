import random
import re
from string import ascii_uppercase, ascii_lowercase


def Gronsfeld_encrypt(message, key):
    if not re.match("^[A-Za-z\\s,.;!?]*$", message):
        raise ValueError("Сообщение должно содержать только латинские буквы, пробелы и знаки препинания.")

    key = str(key)
    key_len = len(key)
    encrypted_text = ""
    keys = [int(char) for char in key]

    ascii_len = len(ascii_uppercase)
    key_index = 0

    for char in message:
        if char.isupper():
            new_position = (ascii_uppercase.index(char) + keys[key_index % key_len]) % ascii_len
            encrypted_text += ascii_uppercase[new_position]
            key_index += 1
        elif char.islower():
            new_position = (ascii_lowercase.index(char) + keys[key_index % key_len]) % len(ascii_lowercase)
            encrypted_text += ascii_lowercase[new_position]
            key_index += 1
        else:
            encrypted_text += char

    return encrypted_text


def Gronsfeld_decrypt(cipher, key):
    if not re.match("^[A-Za-z\\s,.;!?]*$", cipher):
        raise ValueError("Шифротекст должен содержать только латинские буквы, пробелы и знаки препинания.")

    key = str(key)
    key_len = len(key)
    decrypted_text = ""
    keys = [int(char) for char in key]

    ascii_len = len(ascii_uppercase)
    key_index = 0

    for char in cipher:
        if char.isupper():
            new_position = (ascii_uppercase.index(char) - keys[key_index % key_len]) % ascii_len
            decrypted_text += ascii_uppercase[new_position]
            key_index += 1
        elif char.islower():
            new_position = (ascii_lowercase.index(char) - keys[key_index % key_len]) % len(ascii_lowercase)
            decrypted_text += ascii_lowercase[new_position]
            key_index += 1
        else:
            decrypted_text += char

    return decrypted_text


def Gronsfeld_generate_key(length):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))