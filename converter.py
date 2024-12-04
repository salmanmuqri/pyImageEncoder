from PIL import Image

def encode_text_in_image(image_path, text, output_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    encoded = img.copy()
    width, height = img.size
    text += "\0"  
    binary_text = ''.join([format(ord(char), '08b') for char in text])
    data_index = 0
    binary_len = len(binary_text)

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3): 
                if data_index < binary_len:
                    pixel[i] = pixel[i] & ~1 | int(binary_text[data_index])  
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= binary_len:
                encoded.save(output_path)
                print(f"Text encoded and saved to {output_path}")
                return


def decode_text_from_image(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    binary_text = ""
    width, height = img.size

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3): 
                binary_text += str(pixel[i] & 1)

    # Convert binary to text
    chars = [binary_text[i:i + 8] for i in range(0, len(binary_text), 8)]
    decoded_text = ""
    for char in chars:
        decoded_char = chr(int(char, 2))
        if decoded_char == "\0":  
            break
        decoded_text += decoded_char

    return decoded_text



if __name__ == "__main__":
    print("Choose an option:\n1. Encode Text\n2. Decode Text")
    choice = input("Enter choice: ")

    if choice == "1":
        img_path = input("Enter image path: ").strip().strip("'\"")
        secret_text = input("Enter text to encode: ")
        output_img = input("Enter output image path: ").strip().strip("'\"")
        encode_text_in_image(img_path, secret_text, output_img)
    elif choice == "2":
        img_path = input("Enter image path: ").strip().strip("'\"")
        print("Decoded text: ", decode_text_from_image(img_path))
