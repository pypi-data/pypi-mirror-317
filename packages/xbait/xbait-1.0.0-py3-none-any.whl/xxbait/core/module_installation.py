# nyx/core/module_installation.py
import importlib
import subprocess
import sys
from nyx.utils import logger

def install_missing_modules():
    display_message("[+] 🔃 INSTALLING REQUIRED WINDOWS MODULES")
    required_modules = [
        "requests",
        "sqlite3",
        "psutil",
        "pyautogui",
        "pyperclip",
        "pywin32",
    ]
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            display_message(f"🔃 Module check in progress: {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", module])
            display_message(f"✅ Module {module} installed successfully.")
        else:
            display_message(f"✅ Module {module} is already available.")

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
