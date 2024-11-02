import sys
import socket
import threading

# Retrieve peer IP from command-line arguments
PEER_IP = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5005
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

# Run threads for sending and receiving chat
threads = [
    threading.Thread(target=send_chat),
    threading.Thread(target=receive_chat)
]

for t in threads:
    t.start()

for t in threads:
    t.join()
