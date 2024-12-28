# nyx/modules/recent_files.py
import os
from nyx.utils import logger

def list_recent_files():
    recent_files = []
    try:
        recent_folder = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Recent")
        for file in os.listdir(recent_folder):
            if file.endswith(".lnk"):
                recent_files.append(file)
        display_message("✅ Recent Files Updated Successfully.")
        return recent_files
    except Exception as e:
        display_message(f"❌ Error Updating Recent Files: {e}", "error")
        return []

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
