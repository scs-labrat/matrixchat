import cv2
import numpy as np
from PIL import Image
import os
import time

# Matrix-inspired characters for different brightness levels
MATRIX_CHARS = ["@", "#", "$", "%", "&", "0", "1", " "]

# Green ANSI color codes with varying brightness levels
GREEN_ANSI_COLORS = [
    "\033[38;5;22m",  # Dark green
    "\033[38;5;28m", 
    "\033[38;5;34m",
    "\033[38;5;40m",
    "\033[38;5;46m",   # Bright green
    "\033[38;5;82m",   # Neon green
    "\033[38;5;118m",  # Lightest green
]

def resize_image(image, new_width=150):  # Higher resolution for more detail
    width, height = image.size
    aspect_ratio = height / width / 1.65
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))

def grayscale_image(image):
    return image.convert("L")

def map_pixels_to_green_matrix(image):
    pixels = np.array(image)
    ansi_str = ""
    for row in pixels:
        for pixel in row:
            # Map pixel intensity to green ANSI color and Matrix character
            color_code = GREEN_ANSI_COLORS[pixel // (256 // len(GREEN_ANSI_COLORS))]
            matrix_char = MATRIX_CHARS[pixel // (256 // len(MATRIX_CHARS))]
            ansi_str += color_code + matrix_char
        ansi_str += "\033[0m\n"  # Reset color at end of each line
    return ansi_str

def image_to_green_matrix(image, new_width=150):  # Higher resolution parameter
    image = resize_image(image, new_width)
    image = grayscale_image(image)
    ansi_str = map_pixels_to_green_matrix(image)
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

        # Convert frame to green Matrix-style ANSI art
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        ansi_art = image_to_green_matrix(frame_pil)

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
