import math
from collections import Counter
import matplotlib.pyplot as plt


# -----------------------------
# Clean text (optional)
# -----------------------------

def clean_text(text):
    return text.lower()


# -----------------------------
# Character frequency
# -----------------------------

def char_frequency(text):

    text = clean_text(text)

    freq = Counter(text)

    total = len(text)

    result = {}

    for char in freq:
        result[char] = freq[char] / total

    return result


# -----------------------------
# Shannon entropy
# -----------------------------

def shannon_entropy(text):

    freq = char_frequency(text)

    entropy = 0

    for p in freq.values():
        entropy -= p * math.log2(p)

    return entropy


# -----------------------------
# Frequency histogram
# -----------------------------

def plot_frequency(text):

    freq = char_frequency(text)

    letters = list(freq.keys())
    values = list(freq.values())

    plt.figure()
    plt.bar(letters, values)

    plt.title("Character Frequency")
    plt.xlabel("Character")
    plt.ylabel("Frequency")

    plt.show()


# -----------------------------
# Compare entropy
# -----------------------------

def compare_entropy(text1, text2):

    e1 = shannon_entropy(text1)
    e2 = shannon_entropy(text2)

    print("Text 1 entropy:", round(e1, 4))
    print("Text 2 entropy:", round(e2, 4))


# -----------------------------
# Pretty report
# -----------------------------

def full_analysis(text):

    print("----- ANALYSIS -----")
    print("Text:", text)
    print("Length:", len(text))

    entropy = shannon_entropy(text)
    print("Entropy:", round(entropy, 4))

    print("\nTop frequencies:")

    freq = char_frequency(text)

    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    for char, value in sorted_freq[:10]:
        print(f"{repr(char)}: {round(value, 4)}")

    plot_frequency(text)


# -----------------------------
# Test module
# -----------------------------

if __name__ == "__main__":

    text_plain = "This is a simple example message for CipherLab"
    text_random = "asdh1239as8d7a9sd8a7s9d8a7sd98as7d98as7d"

    print("---- Plain Text ----")
    full_analysis(text_plain)

    print("\n---- Random / Encrypted ----")
    full_analysis(text_random)

    print("\n---- Comparison ----")
    compare_entropy(text_plain, text_random)