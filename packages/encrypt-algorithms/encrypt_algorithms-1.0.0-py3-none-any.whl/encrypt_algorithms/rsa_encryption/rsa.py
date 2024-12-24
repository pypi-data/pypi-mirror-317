import random

def extended_gcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def modular_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("e не обратим по модулю phi")
    return x % phi


def is_prime(n):
    return n > 1 and all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))


def generate_prime(min_value, max_value):
    while True:
        num = random.randint(min_value, max_value)
        if is_prime(num):
            return num

def generate_keys():
    p = generate_prime(100, 300)
    q = generate_prime(100, 300)
    while p == q:
        q = generate_prime(100, 300)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    while extended_gcd(e, phi)[0] != 1:
        e = random.randint(2, phi - 1)

    d = modular_inverse(e, phi)

    return (e, n), (d, n)


def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result


def encrypt(public_key, plaintext):
    e, n = public_key
    return [mod_exp(ord(char), e, n) for char in plaintext]


def decrypt(private_key, ciphertext):
    d, n = private_key
    return ''.join([chr(mod_exp(char, d, n)) for char in ciphertext])
