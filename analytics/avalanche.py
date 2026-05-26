import matplotlib.pyplot as plt
from core.aes_logic import generate_key, encrypt_text


# -----------------------------
# Convert bytes to binary string
# -----------------------------

def bytes_to_bits(data):

    return ''.join(format(byte, '08b') for byte in data)


# -----------------------------
# Compare two bit strings
# -----------------------------

def bit_difference(bits1, bits2):

    diff = 0

    for b1, b2 in zip(bits1, bits2):
        if b1 != b2:
            diff += 1

    return diff / len(bits1)


# -----------------------------
# Avalanche effect test (AES)
# -----------------------------

def avalanche_test(text1, text2):

    key = generate_key()

    iv1, enc1 = encrypt_text(text1, key)
    iv2, enc2 = encrypt_text(text2, key)

    bits1 = bytes_to_bits(enc1)
    bits2 = bytes_to_bits(enc2)

    ratio = bit_difference(bits1, bits2)

    return ratio, bits1, bits2


# -----------------------------
# Plot avalanche result
# -----------------------------

def plot_avalanche(bits1, bits2):

    differences = [1 if b1 != b2 else 0 for b1, b2 in zip(bits1, bits2)]

    plt.figure()

    plt.plot(differences)

    plt.title("Avalanche Effect (bit differences)")
    plt.xlabel("Bit position")
    plt.ylabel("Changed (1 = yes)")

    plt.show()


# -----------------------------
# Test module
# -----------------------------

if __name__ == "__main__":

    text1 = "HELLO CIPHERLAB"
    text2 = "HELLo CIPHERLAB"  

    ratio, bits1, bits2 = avalanche_test(text1, text2)

    print("Avalanche ratio:", ratio)

    plot_avalanche(bits1, bits2)