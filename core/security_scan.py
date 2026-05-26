from PIL import Image, ImageDraw
import math
from collections import Counter
import matplotlib.pyplot as plt

def image_entropy(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.getdata())
    values = [val for pixel in pixels for val in pixel]
    
    freq = Counter(values)
    total = len(values)
    return -sum((count/total) * math.log2(count/total) for count in freq.values())

def lsb_ratio(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.getdata())
    bits = [val & 1 for pixel in pixels for val in pixel]
    return sum(bits) / len(bits)

def chi_square_analysis(image_path):
    image = Image.open(image_path).convert("L")
    hist = image.histogram()
    chi_square = 0
    for i in range(0, 256, 2):
        obs1, obs2 = hist[i], hist[i+1]
        exp = (obs1 + obs2) / 2
        if exp > 0:
            chi_square += ((obs1 - exp)**2 / exp) + ((obs2 - exp)**2 / exp)
    return chi_square

def plot_histogram(image_path):
    image = Image.open(image_path).convert("L")
    plt.figure(figsize=(10, 5))
    plt.plot(image.histogram(), color='black')
    plt.title("Гістограма інтенсивності (Grayscale)")
    plt.xlabel("Значення пікселя")
    plt.ylabel("Частота")
    plt.grid(True)
    plt.show()

def show_bit_plane(image_path, bit=0, output_path="bit_plane.png"):
    image = Image.open(image_path).convert("L")
    pixels = image.load()
    output = Image.new("L", image.size)
    out_pixels = output.load()

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            out_pixels[x, y] = 255 if (pixels[x, y] >> bit) & 1 else 0

    output.save(output_path)
    return output_path

def security_scan(image_path):
    entropy = image_entropy(image_path)
    ratio = lsb_ratio(image_path)
    chi_square = chi_square_analysis(image_path)
    
    score = 0
    if entropy > 7.5: score += 25
    if 0.45 <= ratio <= 0.55: score += 25
    if chi_square < 500: score += 50

    result = "SAFE" if score < 30 else "WARNING" if score < 70 else "SUSPICIOUS"
    return {
        "entropy": round(entropy, 4),
        "lsb_ratio": round(ratio, 4),
        "chi_square": round(chi_square, 4),
        "suspicion_score": score,
        "result": result
    }


# -----------------------------
# BASIC FEATURES
# -----------------------------

def entropy(block):
    freq = {}
    for px in block:
        for v in px:
            freq[v] = freq.get(v, 0) + 1

    ent = 0
    total = len(block) * 3

    for p in freq.values():
        p = p / total
        ent -= p * math.log2(p)

    return ent


def lsb_ratio(block):
    bits = []
    for r, g, b in block:
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

    return sum(bits) / len(bits)


def chi_square(block):

    even = 0
    odd = 0

    for r, g, b in block:
        for v in (r, g, b):
            if v % 2 == 0:
                even += 1
            else:
                odd += 1

    total = even + odd
    if total == 0:
        return 0

    expected = total / 2

    return ((even - expected) ** 2 + (odd - expected) ** 2) / expected


def variance(block):

    vals = []
    for px in block:
        for v in px:
            vals.append(v)

    mean = sum(vals) / len(vals)
    return sum((x - mean) ** 2 for x in vals) / len(vals)


# -----------------------------
# BASELINE MODEL (IMPORTANT)
# -----------------------------

def estimate_baseline(image_path, block_size=8):

    image = Image.open(image_path).convert("RGB")
    pixels = image.load()

    w, h = image.size

    ent = []
    lsb = []
    chi = []
    var = []

    for x in range(0, w, block_size):
        for y in range(0, h, block_size):

            block = []

            for i in range(block_size):
                for j in range(block_size):
                    if x+i < w and y+j < h:
                        block.append(pixels[x+i, y+j])

            if not block:
                continue

            ent.append(entropy(block))
            lsb.append(lsb_ratio(block))
            chi.append(chi_square(block))
            var.append(variance(block))

    return {
        "entropy": sum(ent)/len(ent),
        "lsb": sum(lsb)/len(lsb),
        "chi": sum(chi)/len(chi),
        "var": sum(var)/len(var)
    }


# -----------------------------
# MAIN v4 SCANNER
# -----------------------------

def analyze_image_v4(image_path, block_size=8):

    image = Image.open(image_path).convert("RGB")
    pixels = image.load()

    w, h = image.size

    baseline = estimate_baseline(image_path, block_size)

    risk_scores = []

    for x in range(0, w, block_size):
        for y in range(0, h, block_size):

            block = []

            for i in range(block_size):
                for j in range(block_size):
                    if x+i < w and y+j < h:
                        block.append(pixels[x+i, y+j])

            if not block:
                continue

            e = entropy(block)
            l = lsb_ratio(block)
            c = chi_square(block)
            v = variance(block)

            score = 0

            # entropy deviation
            if abs(e - baseline["entropy"]) > 0.8:
                score += 0.25

            # LSB anomaly (IMPORTANT)
            if abs(l - 0.5) > 0.08:
                score += 0.35

            # chi-square (STRONG SIGNAL)
            if c > baseline["chi"] * 1.5:
                score += 0.25

            # variance anomaly
            if abs(v - baseline["var"]) > 500:
                score += 0.15

            risk_scores.append(score)

    # FINAL RISK
    risk = (sum(risk_scores) / len(risk_scores)) * 100 if risk_scores else 0

    # DECISION
    if risk < 25:
        decision = "SAFE"
    elif risk < 55:
        decision = "SUSPICIOUS"
    else:
        decision = "HIGH RISK"

    return {
        "risk": round(risk, 2),
        "decision": decision
    }