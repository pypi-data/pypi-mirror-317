# nyx/modules/users.py
import os
import subprocess
from nyx.utils import logger

def list_users():
    users_list = []
    try:
        current_user = os.getlogin()
        output = os.popen("net user").read().splitlines()
        for line in output:
            if (
                line.strip()
                and not line.startswith("The command")
                and "User    accounts" not in line
            ):
                users_list.append(line.strip())
        display_message("✅ User Info Verified.")
        return current_user, users_list
    except Exception as e:
        display_message(f"❌ Error Getting User Info: {e}", "error")
        return "Current User Name", ["User1", "User2"]

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
