import random
import math


def miller_rabin(n, k=40):
    if n == 2 or n == 3:
        return True

    if n <= 1 or n % 2 == 0:
        return False

    r = 0
    d = n - 1

    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):

        a = random.randrange(2, n - 2)

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):

            x = pow(x, 2, n)

            if x == n - 1:
                break
        else:
            return False

    return True


def generate_prime(bits=512):

    while True:

        num = random.getrandbits(bits)

        num |= (1 << bits - 1) | 1

        if miller_rabin(num):
            return num


def extended_gcd(a, b):

    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y



def mod_inverse(e, phi):

    gcd, x, y = extended_gcd(e, phi)

    if gcd != 1:
        raise Exception("Modular inverse does not exist")

    return x % phi


def generate_keys(bits=1024):

    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)

    n = p * q

    phi = (p - 1) * (q - 1)

    e = 65537

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


def encrypt(message, public_key):

    e, n = public_key

    cipher = [pow(ord(char), e, n) for char in message]

    return cipher


def decrypt(cipher, private_key):

    d, n = private_key

    message = ''.join([chr(pow(char, d, n)) for char in cipher])

    return message


# -------------------------------
# Test RSA
# -------------------------------

if __name__ == "__main__":

    print("Generating keys...")

    public_key, private_key = generate_keys()

    message = "Hello CipherLab"

    print("Original:", message)

    encrypted = encrypt(message, public_key)

    print("Encrypted:", encrypted)

    decrypted = decrypt(encrypted, private_key)

    print("Decrypted:", decrypted)