import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def generate_key():

    key = get_random_bytes(32)  

    return key


def encrypt_text(message, key):

    cipher = AES.new(key, AES.MODE_CBC)

    iv = cipher.iv

    ciphertext = cipher.encrypt(
        pad(message.encode(), AES.block_size)
    )

    return iv, ciphertext


def decrypt_text(iv, ciphertext, key):

    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

    return plaintext.decode()



def encrypt_file(input_file, output_file, key):

    with open(input_file, "rb") as f:
        data = f.read()

    cipher = AES.new(key, AES.MODE_CBC)

    ciphertext = cipher.encrypt(
        pad(data, AES.block_size)
    )

    with open(output_file, "wb") as f:

        f.write(cipher.iv)
        f.write(ciphertext)


def decrypt_file(input_file, output_file, key):

    with open(input_file, "rb") as f:

        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

    with open(output_file, "wb") as f:
        f.write(plaintext)


# -------------------------------
# Test module
# -------------------------------

if __name__ == "__main__":

    key = generate_key()

    message = "Hello CipherLab AES Encryption"

    print("Original message:")
    print(message)

    iv, encrypted = encrypt_text(message, key)

    print("\nEncrypted (bytes):")
    print(encrypted)

    decrypted = decrypt_text(iv, encrypted, key)

    print("\nDecrypted message:")
    print(decrypted)