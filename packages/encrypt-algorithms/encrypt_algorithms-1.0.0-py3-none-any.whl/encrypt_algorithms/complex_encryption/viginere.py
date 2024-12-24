import random
from string import ascii_uppercase, ascii_lowercase


def Vigenere_encrypt(message, key):
    encrypted_text = ''
    key_repeated = (key * (len(message) // len(key))) + key[:len(message) % len(key)]
    for i in range(len(message)):
        if message[i].isalpha():
            shift = ord(key_repeated[i].upper()) - ord('A')
            if message[i].isupper():
                encrypted_text += chr((ord(message[i]) + shift - ord('A')) % 26 + ord('A'))
            else:
                encrypted_text += chr((ord(message[i]) + shift - ord('a')) % 26 + ord('a'))
        else:
            encrypted_text += message[i]
    return encrypted_text

def Vigenere_decrypt(cipher, key):
    decrypted_text = ''
    key_repeated = (key * (len(cipher) // len(key))) + key[:len(cipher) % len(key)]
    for i in range(len(cipher)):
        if cipher[i].isalpha():
            shift = ord(key_repeated[i].upper()) - ord('A')
            if cipher[i].isupper():
                decrypted_text += chr((ord(cipher[i]) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted_text += chr((ord(cipher[i]) - shift - ord('a')) % 26 + ord('a'))
        else:
            decrypted_text += cipher[i]
    return decrypted_text


def Vigenere_generate_key(length):
    return ''.join(random.choice(ascii_uppercase + ascii_lowercase) for _ in range(length))
