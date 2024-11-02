import json
import os
import subprocess
from colorama import Fore, Style, init
from pyfiglet import Figlet

# Initialize colorama
init(autoreset=True)

ADDRESS_BOOK_FILE = "address_book.json"
PORT = 5005

def show_banner():
    """Display the banner using pyfiglet."""
    f = Figlet(font="slant")
    print(Fore.GREEN + f.renderText("Matrix Chat CLI") + Style.RESET_ALL)

def load_address_book():
    """Load the address book from a JSON file."""
    if os.path.exists(ADDRESS_BOOK_FILE):
        with open(ADDRESS_BOOK_FILE, "r") as file:
            return json.load(file)
    return {}

def save_address_book(address_book):
    """Save the address book to a JSON file."""
    with open(ADDRESS_BOOK_FILE, "w") as file:
        json.dump(address_book, file, indent=4)

def view_peers(address_book):
    """Display a list of available peers."""
    print(Fore.YELLOW + "\nAvailable peers:" + Style.RESET_ALL)
    for idx, (name, ip) in enumerate(address_book.items(), start=1):
        print(Fore.CYAN + f"{idx}. {name} - {ip}" + Style.RESET_ALL)
    print()

def add_peer(address_book):
    """Add a new peer to the address book."""
    name = input(Fore.YELLOW + "Enter the name for the new peer: " + Style.RESET_ALL).strip()
    ip_address = input(Fore.YELLOW + f"Enter the IP address for {name}: " + Style.RESET_ALL).strip()
    address_book[name] = ip_address
    save_address_book(address_book)
    print(Fore.GREEN + f"Peer {name} added with IP {ip_address}" + Style.RESET_ALL)

def select_peer(address_book):
    """Select a peer to connect to."""
    view_peers(address_book)
    choice = input(Fore.YELLOW + "Select a peer by number: " + Style.RESET_ALL).strip()
    try:
        choice = int(choice) - 1
        peer_name, peer_ip = list(address_book.items())[choice]
        print(Fore.GREEN + f"Selected peer: {peer_name} ({peer_ip})" + Style.RESET_ALL)
        return peer_ip
    except (ValueError, IndexError):
        print(Fore.RED + "Invalid selection. Try again." + Style.RESET_ALL)
        return None

def launch_video(peer_ip):
    """Launch the video feed in a new terminal."""
    print(Fore.GREEN + "Launching video feed..." + Style.RESET_ALL)
    subprocess.Popen(["gnome-terminal", "--", "python3", "matrix_video.py", peer_ip])

def launch_chat(peer_ip):
    """Launch the chat in a new terminal."""
    print(Fore.GREEN + "Launching chat..." + Style.RESET_ALL)
    subprocess.Popen(["gnome-terminal", "--", "python3", "matrix_chat.py", peer_ip])

def run_matrix():
    """Run matrix.py in a new terminal."""
    print(Fore.GREEN + "Launching Matrix..." + Style.RESET_ALL)
    subprocess.Popen(["gnome-terminal", "--", "python3", "matrix.py"])

def main():
    show_banner()
    address_book = load_address_book()
    selected_peer = None
    
    while True:
        print(Fore.MAGENTA + "--- Matrix Chat CLI Menu ---" + Style.RESET_ALL)
        print(Fore.YELLOW + "1." + Fore.CYAN + " View peers")
        print(Fore.YELLOW + "2." + Fore.CYAN + " Add peer")
        print(Fore.YELLOW + "3." + Fore.CYAN + " Select peer to connect")
        print(Fore.YELLOW + "4." + Fore.CYAN + " Launch video feed")
        print(Fore.YELLOW + "5." + Fore.CYAN + " Launch chat")
        print(Fore.YELLOW + "6." + Fore.CYAN + " Run Matrix")
        print(Fore.YELLOW + "7." + Fore.CYAN + " Exit" + Style.RESET_ALL)
        
        choice = input(Fore.YELLOW + "Select an option: " + Style.RESET_ALL).strip()
        
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
                print(Fore.RED + "No peer selected. Please select a peer first." + Style.RESET_ALL)
        elif choice == "5":
            if selected_peer:
                launch_chat(selected_peer)
            else:
                print(Fore.RED + "No peer selected. Please select a peer first." + Style.RESET_ALL)
        elif choice == "6":
            run_matrix()
        elif choice == "7":
            print(Fore.GREEN + "Exiting..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid option. Try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
