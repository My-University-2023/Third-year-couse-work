from core.security_scan import show_bit_plane
import os

def generate_bit_planes(image_path):
    paths = []
    if not os.path.exists("analytics_out"):
        os.makedirs("analytics_out")
    
    for bit in range(8):
        out = f"analytics_out/bit_plane_{bit}.png"
        show_bit_plane(image_path, bit, out)
        paths.append(out)
    return paths