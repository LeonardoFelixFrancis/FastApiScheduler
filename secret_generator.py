import secrets

SECRET_KEY = secrets.token_hex(32)

print("Your secure key", SECRET_KEY)