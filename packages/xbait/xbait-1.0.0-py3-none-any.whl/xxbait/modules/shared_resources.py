# nyx/modules/shared_resources.py
import os
from nyx.utils import logger

def list_shared_resources():
    shared_resources = []
    try:
        output = os.popen("net share").read().splitlines()
        for line in output:
            if line.strip() and not line.startswith("Share name"):
                shared_resources.append(line.strip())
        display_message("✅ Shared Resources Updated Successfully.")
        return shared_resources
    except Exception as e:
        display_message(f"❌ Error Updating Shared Resources: {e}", "error")
        return []

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
