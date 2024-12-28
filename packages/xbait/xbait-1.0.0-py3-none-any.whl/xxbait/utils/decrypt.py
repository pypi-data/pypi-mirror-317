# nyx/utils/decrypt.py
import win32crypt
import base64

def decrypt_password(encrypted_password):
    try:
        return win32crypt.CryptUnprotectData(encrypted_password)[1].decode()
    except Exception:
        pass
    try:
        return base64.b64decode(encrypted_password).decode()
    except Exception:
        pass
    return "Error decrypting password"
