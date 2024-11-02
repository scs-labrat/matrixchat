import cv2
import socket
import threading
import numpy as np
from PIL import Image
import sounddevice as sd
import time
import json
import os
import subprocess
import sys

# Constants
PORT = 5005
ADDRESS_BOOK_FILE = "address_book.json"
SAMPLE_RATE = 44100  # Audio sample rate in Hz
AUDIO_BUFFER_SIZE = 1024  # Buffer size for audio chunks

# Matrix-inspired characters and ANSI green shades
MATRIX_CHARS = ["@", "#", "$", "%", "&", "0", "1", " "]
GREEN_ANSI_COLORS = ["\033[38;5;22m", "\033[38;5;28m", "\033[38;5;34m", "\033[38;5;40m", "\033[38;5;46m", "\033[38;5;82m", "\033[38;5;118m"]

# Load or create the address book
def load_address_book():
    if os.path.exists(ADDRESS_BOOK_FILE):
        with open(ADDRESS_BOOK_FILE, "r") as file:
            return json.load(file)
    return {}

def save_address_book(address_book):
    with open(ADDRESS_BOOK_FILE, "w") as file:
        json.dump(address_book, file, indent=4)

def view_peers(address_book):
    """Display a list of available peers."""
    print("\nAvailable peers:")
    for idx, (name, ip) in enumerate(address_book.items(), start=1):
        print(f"{idx}. {name} - {ip}")
    print()

def add_peer(address_book):
    """Add a new peer to the address book."""
    name = input("Enter the name for the new peer: ").strip()
    ip_address = input(f"Enter the IP address for {name}: ").strip()
    address_book[name] = ip_address
    save_address_book(address_book)
    print(f"Peer {name} added with IP {ip_address}")

def select_peer(address_book):
    """Select a peer to connect to."""
    view_peers(address_book)
    choice = input("Select a peer by number: ").strip()
    try:
        choice = int(choice) - 1
        peer_name, peer_ip = list(address_book.items())[choice]
        print(f"Selected peer: {peer_name} ({peer_ip})")
        return peer_ip
    except (ValueError, IndexError):
        print("Invalid selection. Try again.")
        return None

def launch_video(peer_ip):
    """Launch the video feed in a new terminal."""
    subprocess.Popen(["gnome-terminal", "--", "python3", "matrix_script.py", "video", peer_ip])

def launch_chat(peer_ip):
    """Launch the chat in a new terminal."""
    subprocess.Popen(["gnome-terminal", "--", "python3", "matrix_script.py", "chat", peer_ip])

def main_menu():
    address_book = load_address_book()
    selected_peer = None
    
    while True:
        print("\n--- Matrix Chat CLI Menu ---")
        print("1. View peers")
        print("2. Add peer")
        print("3. Select peer to connect")
        print("4. Launch video feed")
        print("5. Launch chat")
        print("6. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            view_peers(address_book)
        elif choice == "2":
            add_peer(address_book)
        elif choice == "3":
            selected_peer = select_peer(address_book)
        elif choice == "4":
            if selected_peer:
                launch_video(selected_peer)
            else:
                print("No peer selected. Please select a peer first.")
        elif choice == "5":
            if selected_peer:
                launch_chat(selected_peer)
            else:
                print("No peer selected. Please select a peer first.")
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

# Functions for video feed, chat, and audio
def resize_image(image, new_width=80):
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
            color_code = GREEN_ANSI_COLORS[pixel // (256 // len(GREEN_ANSI_COLORS))]
            matrix_char = MATRIX_CHARS[pixel // (256 // len(MATRIX_CHARS))]
            ansi_str += color_code + matrix_char
        ansi_str += "\033[0m\n"  # Reset color at end of each line
    return ansi_str

def image_to_green_matrix(image, new_width=80):
    image = resize_image(image, new_width)
    image = grayscale_image(image)
    return map_pixels_to_green_matrix(image)

def send_video_feed(PEER_IP):
    ADDRESS = (PEER_IP, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        ansi_art = image_to_green_matrix(frame_pil)
        sock.sendto(ansi_art.encode("utf-8"), ADDRESS)
        time.sleep(0.03)

def receive_video_feed():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))
    while True:
        data, _ = sock.recvfrom(65536)
        try:
            # Attempt to decode as UTF-8
            print("\033[H" + data.decode("utf-8"))  # Print video feed to terminal
        except UnicodeDecodeError:
            # Ignore non-text packets (likely audio)
            continue

def send_audio(PEER_IP):
    ADDRESS = (PEER_IP, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def callback(indata, frames, time, status):
        if status:
            print(status)
        sock.sendto(indata.tobytes(), ADDRESS)
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=AUDIO_BUFFER_SIZE):
        sd.sleep(int(1e9))  # Keep the stream open indefinitely

def receive_audio():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))
    with sd.OutputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', blocksize=AUDIO_BUFFER_SIZE) as stream:
        while True:
            audio_data, _ = sock.recvfrom(AUDIO_BUFFER_SIZE * 2)
            audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            stream.write(audio_array)

def chat_mode(PEER_IP):
    ADDRESS = (PEER_IP, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))

    def send_chat():
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                print("Exiting chat...")
                break
            sock.sendto(message.encode("utf-8"), ADDRESS)

    def receive_chat():
        while True:
            data, _ = sock.recvfrom(65536)
            try:
                message = data.decode("utf-8")
                print("\nPeer:", message)
            except UnicodeDecodeError:
                # Ignore non-text packets
                continue

    threads = [threading.Thread(target=send_chat), threading.Thread(target=receive_chat)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    # Check if the script is run with mode arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        peer_ip = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"

        if mode == "video":
            threading.Thread(target=send_video_feed, args=(peer_ip,)).start()
            threading.Thread(target=receive_video_feed).start()
            threading.Thread(target=send_audio, args=(peer_ip,)).start()
            threading.Thread(target=receive_audio).start()

        elif mode == "chat":
            chat_mode(peer_ip)
    else:
        main_menu()
