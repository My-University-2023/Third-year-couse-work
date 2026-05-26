import os
import re
from PIL import Image


def extract_id(path):
    name = os.path.splitext(os.path.basename(path))[0]
    match = re.search(r"\d+", name)
    return match.group() if match else None


def find_stego(stego_dir, idx):
    for f in os.listdir(stego_dir):
        if str(idx) in f:
            return os.path.join(stego_dir, f)
    return None


# -----------------------------
# Індексуємо stego папку
# -----------------------------
def build_stego_index(stego_dir):
    index = {}

    for file in os.listdir(stego_dir):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        idx = extract_id(file)
        if idx:
            index[idx] = os.path.join(stego_dir, file)

    return index


# -----------------------------
# Heatmap (різниця пікселів)
# -----------------------------
def generate_heatmap(original_path, modified_path, output_path):
    original = Image.open(original_path).convert("RGB")
    modified = Image.open(modified_path).convert("RGB")

    if original.size != modified.size:
        raise Exception(f"Розміри не збігаються: {original_path}")

    width, height = original.size
    heatmap = Image.new("RGB", (width, height))

    o = original.load()
    m = modified.load()
    h = heatmap.load()

    for x in range(width):
        for y in range(height):
            h[x, y] = (255, 0, 0) if o[x, y] != m[x, y] else (0, 0, 0)

    heatmap.save(output_path)
    return output_path


# -----------------------------
# Основний процес
# -----------------------------
def process_dataset(dataset_path="dataset"):
    normal_dir = os.path.join(dataset_path, "normal")
    stego_dir = os.path.join(dataset_path, "stego")

    stego_index = build_stego_index(stego_dir)

    results = []

    for file in os.listdir(normal_dir):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        idx = extract_id(file)

        if idx not in stego_index:
            print(f"[WARN] Немає stego для {file}")
            continue

        normal_path = os.path.join(normal_dir, file)
        stego_path = stego_index[idx]

        output_path = os.path.join(dataset_path, f"heatmap_{idx}.png")

        try:
            generate_heatmap(normal_path, stego_path, output_path)
            results.append(output_path)
            print(f"[OK] Pair {idx} → heatmap створено")
        except Exception as e:
            print(f"[ERROR] {file}: {e}")

    return results


# -----------------------------
# Запуск
# -----------------------------
if __name__ == "__main__":
    process_dataset("dataset")