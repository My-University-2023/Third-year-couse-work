from PIL import Image
import numpy as np
import math


def extract_features(image_path):

    image = Image.open(image_path).convert("RGB")
    pixels = np.array(image)

    # -----------------------------
    # entropy
    # -----------------------------
    hist, _ = np.histogram(pixels, bins=256, range=(0, 256))
    probs = hist / hist.sum()

    entropy = -np.sum([
        p * math.log2(p)
        for p in probs if p > 0
    ])

    # -----------------------------
    # LSB ratio
    # -----------------------------
    lsb = pixels & 1
    lsb_ratio = np.mean(lsb)

    # -----------------------------
    # variance
    # -----------------------------
    variance = np.var(pixels)

    # -----------------------------
    # edge density
    # -----------------------------
    gx = np.diff(pixels.astype(float), axis=0)
    gy = np.diff(pixels.astype(float), axis=1)

    edge_density = (
        np.mean(np.abs(gx)) +
        np.mean(np.abs(gy))
    )

    # -----------------------------
    # block noise
    # -----------------------------
    block_size = 8
    block_vars = []

    h, w, _ = pixels.shape

    for y in range(0, h - block_size, block_size):
        for x in range(0, w - block_size, block_size):

            block = pixels[y:y+block_size, x:x+block_size]

            block_vars.append(np.var(block))

    block_noise = np.mean(block_vars)

    return [
        entropy,
        lsb_ratio,
        variance,
        edge_density,
        block_noise
    ]