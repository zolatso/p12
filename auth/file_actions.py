import json
import os

from . import TOKEN_FILE

def write_token_to_file(token: str):
    """Writes the JWT token and associated username to a local JSON file."""
    try:
        with open(TOKEN_FILE, 'w') as f:
            json.dump({"token": token}, f)
    except IOError as e:
        print(f"Error writing token to file {TOKEN_FILE}: {e}")

def read_token_from_file():
    """Reads the JWT token and username from a local JSON file.
    Returns token or None if not found or error.
    """
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            return data.get("token")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {TOKEN_FILE}: {e}")
        return None
    except IOError as e:
        print(f"Error reading token from file {TOKEN_FILE}: {e}")
        return None
    
def clear_token_file():
    """Removes the local token file."""
    if os.path.exists(TOKEN_FILE):
        try:
            os.remove(TOKEN_FILE)
        except OSError as e:
            print(f"Error removing token file {TOKEN_FILE}: {e}")


