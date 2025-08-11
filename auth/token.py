import jwt
import datetime

from .file_actions import write_token_to_file, read_token_from_file, clear_token_file
from .exc import AuthExpiredError, AuthInvalidError
from . import SECRET_KEY

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

def verify_jwt(token: str) -> dict | None:
    """
    Verifies a JWT token and returns its decoded payload if valid.

    Args:
        token (str): The JWT string to verify.

    Returns:
        dict | None: The decoded payload if valid, None otherwise.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as e:
        clear_token_file()
        raise AuthExpiredError("JWT expired") from e
    except jwt.InvalidTokenError as e:
        clear_token_file()
        raise AuthInvalidError("JWT invalid") from e


