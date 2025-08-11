import os
import json
import jwt
from .exc import AuthError
import datetime

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
TOKEN_FILE = 'auth_token.json'

def write_token_to_file(token: str):
    """Writes the JWT token and associated username to a local JSON file."""
    try:
        with open(TOKEN_FILE, 'w') as f:
            json.dump({"token": token}, f)
    except IOError as e:
        print(f"Error writing token to file {TOKEN_FILE}: {e}")

def get_stored_jwt_from_file() -> str | None:
    """
    Retrieves the stored JWT from the local file.
    """
    return read_token_from_file()

def generate_and_store_jwt(user_details: dict) -> str | None:
    """
    Generates a JWT for the given username, role, and permissions, and stores it in a local file.

    Args:
        username (str): The username for whom to generate the token.
        role (str): The role to include in the token payload.
        permissions (list): A list of permissions to include

    Returns:
        str | None: The encoded JWT string if successful, None otherwise.
    """
    try:
        time_concepts = {
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4),
            "iat": datetime.datetime.now(datetime.timezone.utc)
        }
        user_details.update(time_concepts)
        payload = user_details
        print(payload)
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # Store the token in the local file
        write_token_to_file(encoded_jwt)
        return encoded_jwt
    except Exception as e:
        print(f"An error occurred during JWT generation and storage: {e}")
        return None

def read_token_from_file():
    """Reads the JWT token and username from a local JSON file.
    Returns (username, token) tuple, or (None, None) if not found or error.
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
            print(f"🗑️ Cleared token file: {TOKEN_FILE}")
        except OSError as e:
            print(f"Error removing token file {TOKEN_FILE}: {e}")

def verify_jwt(token: str) -> dict | None:
    """
    Verifies a JWT token and returns its decoded payload if valid.

    Args:
        token (str): The JWT string to verify.

    Returns:
        dict | None: The decoded payload if valid, None otherwise.
    """
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("❌ JWT has expired.")
        clear_token_file()
        return None
    except jwt.InvalidTokenError:
        print("❌ Invalid JWT (e.g., tampered or incorrect signature).")
        clear_token_file()
        return None
    except Exception as e:
        print(f"An unexpected error occurred during JWT verification: {e}")
        return None

