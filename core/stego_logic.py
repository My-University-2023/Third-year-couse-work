from PIL import Image
import struct
import os

# Шлях, куди завжди зберігатимуться файли
TARGET_DIR = "/home/andreiko/Documents/taskUniversity/thirdYearWork/dataset/stego"

# Створюємо папку, якщо її не існує
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

# --- ДОПОМІЖНІ ФУНКЦІЇ ---

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        if len(byte) < 8: break
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def file_to_binary(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# --- ОСНОВНІ ФУНКЦІЇ (ЯКІ ШУКАЄ ТВОЯ UI) ---

def hide_message(input_image_path, output_image_path, message):
    image = Image.open(input_image_path).convert("RGB")
    pixels = list(image.getdata())
    binary_message = text_to_binary(message) + "1111111111111110"
    
    # Виправляємо шлях: завжди в stego і завжди .png
    file_name = os.path.splitext(os.path.basename(output_image_path))[0] + ".png"
    final_output_path = os.path.join(TARGET_DIR, file_name)

    new_pixels = []
    binary_index = 0
    total_bits = len(binary_message)

    for pixel in pixels:
        res_pixel = list(pixel)
        for i in range(3):
            if binary_index < total_bits:
                res_pixel[i] = (res_pixel[i] & 254) | int(binary_message[binary_index])
                binary_index += 1
        new_pixels.append(tuple(res_pixel))

    new_image = Image.new("RGB", image.size)
    new_image.putdata(new_pixels)
    new_image.save(final_output_path, "PNG")
    return final_output_path

def extract_message(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.getdata())
    binary_data = ""

    for pixel in pixels:
        for channel in pixel:
            binary_data += str(channel & 1)

    bytes_data = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    message = ""
    for byte in bytes_data:
        if byte == "11111110": break 
        if len(byte) < 8: break
        message += chr(int(byte, 2))
    return message

def hide_file(input_image_path, output_image_path, secret_file_path):
    image = Image.open(input_image_path).convert("RGB")
    pixels = list(image.getdata())
    
    file_name = os.path.splitext(os.path.basename(output_image_path))[0] + ".png"
    final_output_path = os.path.join(TARGET_DIR, file_name)

    secret_data = file_to_binary(secret_file_path)
    header = struct.pack('>I', len(secret_data))
    payload = header + secret_data
    binary_payload = ''.join(format(byte, '08b') for byte in payload)

    new_pixels = []
    binary_index = 0
    for pixel in pixels:
        res_pixel = list(pixel)
        for i in range(3):
            if binary_index < len(binary_payload):
                res_pixel[i] = (res_pixel[i] & 254) | int(binary_payload[binary_index])
                binary_index += 1
        new_pixels.append(tuple(res_pixel))

    new_image = Image.new("RGB", image.size)
    new_image.putdata(new_pixels)
    new_image.save(final_output_path, "PNG")
    return final_output_path

def extract_file(image_path, output_file_path):
    """
    Витягує прихований файл із зображення.
    """
    try:
        # Відкриваємо стего-зображення
        image = Image.open(image_path).convert("RGB")
        pixels = list(image.getdata())
        
        # 1. Збираємо всі LSB (останні біти) з кожного каналу
        binary_bits = []
        for pixel in pixels:
            for channel in pixel:
                binary_bits.append(str(channel & 1))
        
        binary_str = "".join(binary_bits)
        
        # 2. Групуємо біти у байти
        bytes_data = bytearray()
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i + 8]
            if len(byte) < 8:
                break
            bytes_data.append(int(byte, 2))

        # 3. Читаємо заголовок (перші 4 байти), щоб дізнатися розмір файлу
        if len(bytes_data) < 4:
            print("Помилка: Дані не знайдено або файл пошкоджено")
            return None
            
        # Розпаковуємо розмір файлу (структура '>I' означає unsigned int, 4 байти)
        file_size = struct.unpack('>I', bytes_data[:4])[0]
        
        # 4. Вирізаємо саме ті дані, що належать файлу
        extracted_data = bytes_data[4:4 + file_size]

        # 5. Записуємо результат у файл
        with open(output_file_path, 'wb') as f:
            f.write(extracted_data)
            
        print(f"Файл успішно витягнуто: {output_file_path}")
        return output_file_path

    except Exception as e:
        print(f"Сталася критична помилка: {e}")
        return None