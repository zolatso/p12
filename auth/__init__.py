import os

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
TOKEN_FILE = 'auth_token.json'