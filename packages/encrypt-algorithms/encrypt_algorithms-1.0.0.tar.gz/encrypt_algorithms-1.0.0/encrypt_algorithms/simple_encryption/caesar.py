import re

def caesar_cipher(message, shift):
    if re.search('[а-яА-Я]', message):
        raise ValueError("Текст содержит кириллицу. Шифр поддерживает только латинские символы.")

    result = ""
    for char in message:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
            else:
                result += chr((ord(char) + shift - ord('a')) % 26 + ord('a'))
        else:
            result += char
    return result



def caesar_decipher(message, shift):
    return caesar_cipher(message, -shift)



