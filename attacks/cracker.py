import string


ALPHABET = string.ascii_lowercase


# -----------------------------
# Caesar decrypt (shift)
# -----------------------------

def caesar_decrypt(text, shift):

    result = ""

    for char in text.lower():

        if char in ALPHABET:
            index = ALPHABET.index(char)
            new_index = (index - shift) % 26
            result += ALPHABET[new_index]
        else:
            result += char

    return result


# -----------------------------
# Brute force attack
# -----------------------------

def crack_caesar(text):

    results = []

    for shift in range(26):
        decrypted = caesar_decrypt(text, shift)
        results.append((shift, decrypted))

    return results


# -----------------------------
# Simple scoring (English)
# -----------------------------

COMMON_WORDS = ["the", "and", "is", "to", "of"]


def score_text(text):

    score = 0

    for word in COMMON_WORDS:
        if word in text:
            score += 1

    return score


def best_candidate(results):

    best = None
    best_score = -1

    for shift, text in results:
        score = score_text(text)

        if score > best_score:
            best_score = score
            best = (shift, text)

    return best


# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    encrypted = "khoor flskhuode"  # hello cipherlab

    results = crack_caesar(encrypted)

    for shift, text in results:
        print(f"Shift {shift}: {text}")

    print("\nBest guess:")
    print(best_candidate(results))