# nyx/modules/cleanup.py
import os
import time
from nyx.utils import logger

def cleanup():
    deleted_files = []
    max_retries = 5
    delay_between_retries = 3

    for file_path in created_temp_files:
        if os.path.exists(file_path):
            for attempt in range(max_retries):
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                    break
                except PermissionError:
                    if attempt < max_retries - 1:
                        time.sleep(delay_between_retries)
                    else:
                        display_message(f"❌ Unable to delete file {file_path}: It is still in use.", "error")
        else:
            display_message(f"❌ File not found for cleanup: {file_path}", "warning")

    if deleted_files:
        display_message(f"✅ Deleted {len(deleted_files)} temporary files successfully.")
    else:
        display_message("⚠️ No temporary files were deleted.")
    display_message("Clean up function executed.")

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
