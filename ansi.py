import cv2
import numpy as np
from PIL import Image
import os
import time

# More granular block characters for better detail
BLOCK_CHARS = ["█", "▓", "▒", "░", " "]

# ANSI color codes for finer brightness levels
ANSI_COLORS = [
    "\033[38;5;232m", "\033[38;5;233m", "\033[38;5;234m", "\033[38;5;235m", "\033[38;5;236m",
    "\033[38;5;237m", "\033[38;5;238m", "\033[38;5;239m", "\033[38;5;240m", "\033[38;5;241m",
    "\033[38;5;242m", "\033[38;5;243m", "\033[38;5;244m", "\033[38;5;245m", "\033[38;5;246m",
    "\033[38;5;247m", "\033[38;5;248m", "\033[38;5;249m", "\033[38;5;250m", "\033[38;5;251m"
]

def resize_image(image, new_width=120):  # Higher resolution for more detail
    width, height = image.size
    aspect_ratio = height / width / 1.65
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))

def grayscale_image(image):
    return image.convert("L")

def map_pixels_to_ansi_blocks(image):
    pixels = np.array(image)
    ansi_str = ""
    for row in pixels:
        for pixel in row:
            # Map pixel intensity to finer ANSI color and block character
            color_code = ANSI_COLORS[pixel // (256 // len(ANSI_COLORS))]
            block_char = BLOCK_CHARS[pixel // (256 // len(BLOCK_CHARS))]
            ansi_str += color_code + block_char
        ansi_str += "\033[0m\n"  # Reset color at end of each line
    return ansi_str

def image_to_ansi_blocks(image, new_width=150):  # Higher resolution parameter
    image = resize_image(image, new_width)
    image = grayscale_image(image)
    ansi_str = map_pixels_to_ansi_blocks(image)
    return ansi_str

# Capture video from camera
cap = cv2.VideoCapture(0)

# Verify camera capture
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

try:
    previous_art = ""
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Convert frame to high-resolution ANSI blocks
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        ansi_art = image_to_ansi_blocks(frame_pil)

        # Only print if the art has changed
        if ansi_art != previous_art:
            print("\033[H" + ansi_art)  # Move cursor to top and print
            previous_art = ansi_art

        # Reduce CPU usage and flickering by adding a slight delay
        time.sleep(0.03)  # Adjust for smoother experience

        # Stop with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
