# nyx/modules/installed_programs.py
import os
import subprocess
from nyx.utils import logger

def list_installed_programs():
    programs = []
    try:
        output = os.popen("wmic product get name,version").read().splitlines()
        for line in output:
            if (
                line.strip()
                and not line.startswith("Name")
                and not line.startswith("----")
            ):
                programs.append(line.strip())
        display_message("✅ Programs Logged and Updated.")
        return programs
    except Exception as e:
        display_message(f"❌ Error Logging Programs: {e}", "error")
        return []

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
