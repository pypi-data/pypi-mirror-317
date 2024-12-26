# smart_library/file_tools.py
import json

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
