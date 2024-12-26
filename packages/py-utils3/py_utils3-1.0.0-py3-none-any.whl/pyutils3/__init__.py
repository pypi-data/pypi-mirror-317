# smart_library/__init__.py
from .file_tools import write_file, read_file
from .network_tools import check_internet
from .security_tools import generate_password, encrypt_data, decrypt_data
from .text_tools import analyze_text, extract_keywords
from .database_tools import save, load
from .calculate_tools import calculate
from .ddos_tools import udp, botnet, layer_type
from .web_tools import app, host, port