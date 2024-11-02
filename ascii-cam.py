import cv2
import numpy as np
from PIL import Image
import os

# ASCII characters representing different brightness levels
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width / 1.65
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))

def grayscale_image(image):
    return image.convert("L")

def map_pixels_to_ascii(image, ascii_chars=ASCII_CHARS):
    pixels = np.array(image)
    ascii_str = ""
    for row in pixels:
        ascii_row = "".join([ascii_chars[pixel // (256 // len(ascii_chars))] for pixel in row])
        ascii_str += ascii_row + "\n"
    return ascii_str

def image_to_ascii(image, new_width=100):
    image = resize_image(image, new_width)
    image = grayscale_image(image)
    ascii_str = map_pixels_to_ascii(image)
    return ascii_str

# Capture video from camera
cap = cv2.VideoCapture(0)

# Verify camera capture
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

try:
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Convert frame to ASCII
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        ascii_art = image_to_ascii(frame_pil)

        # Clear console and print ASCII art
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)

        # Stop with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
