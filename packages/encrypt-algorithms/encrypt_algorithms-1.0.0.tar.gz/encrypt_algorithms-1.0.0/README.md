# Шифрование текста

`encrypt_algorithms` — это библиотека на Python для реализации шифрования и дешифрования. В ней содержится три модуля: 

- `complex_encryption` - модуль содержащий функции шифра с помощью сложной замены
- `simple_encryption`- модуль содержащий функции шифра с помощью простой замены
- `rsa_encryption`- модуль шифра с помощью алгоритма RSA

## Функции модуля `complex_encryption`

Каждая функция имеет свою реализацию и для шифрования(`encrypt`), и для дешифрования(`decrypt`)

- Алгоритм Гросфельда.
- Алгоритм Виженера.

## Функции модуля `simple_encryption`

Каждая функция имеет свою реализацию и для шифрования(`encrypt`), и для дешифрования(`decrypt`)

- Алгоритм Цезаря.
- Алгоритм простой замены.

## Установка

Установите библиотеку с помощью pip:

```bash
pip install encrypt_algorithms
```

## Использование

Пример использования библиотеки:

```python
from encrypt_algorithms import complex_encryption

# Генерируем ключ шифрования
key = Gronsfeld_generate_key(length):

# Зашифруем сообщение
cypher = Gronsfeld_encrypt("message", key)

# Расшифруем сообщение
message = Gronsfeld_encrypt(cypher, key)
```

## Лицензия

Этот проект лицензирован на условиях MIT License. Подробнее см. файл [LICENSE](LICENSE).
