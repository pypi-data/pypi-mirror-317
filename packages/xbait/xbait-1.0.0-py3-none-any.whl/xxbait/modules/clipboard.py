# nyx/modules/clipboard.py
import pyperclip
from nyx.utils import logger

def get_clipboard_content():
    try:
        content = pyperclip.paste()
        display_message("✅ Clipboard Updated Successfully.")
        return content
    except Exception as e:
        display_message(f"❌ Error Updating Clipboard: {e}", "error")
        return ""

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
