# nyx/modules/file_finder.py
import os
from nyx.utils import logger

def find_files_with_extensions(allowed_extensions):
    search_dirs = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
    ]
    matching_files = []
    try:
        for directory in search_dirs:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if os.path.splitext(file)[1].lower() in allowed_extensions:
                        matching_files.append(os.path.join(root, file))
        display_message("✅ Data Captured and Updated.")
        return matching_files
    except Exception as e:
        display_message(f"❌ Error Finding Files: {e}", "error")
        return []

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
