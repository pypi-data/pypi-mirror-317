# nyx/modules/system_info.py
import subprocess
from nyx.utils import logger

def gather_system_info():
    info = {}
    try:
        output = subprocess.check_output(["systeminfo"], encoding="utf-8").splitlines()
        for line in output:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                info[key] = value
        display_message("✅ System Info Updated.")
        return info
    except Exception as e:
        display_message(f"❌ Error Updating System Info: {e}", "error")
        return {}

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
