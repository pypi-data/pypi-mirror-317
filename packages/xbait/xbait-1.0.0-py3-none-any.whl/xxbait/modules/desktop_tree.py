# nyx/modules/desktop_tree.py
import os
from nyx.utils import logger

def map_desktop_tree():
    desktop_path = os.path.expanduser("~/Desktop")
    tree_structure = []

    def traverse(directory, prefix=""):
        items = os.listdir(directory)
        for i, item in enumerate(items):
            path = os.path.join(directory, item)
            connector = "├── " if i < len(items) - 1 else "└── "
            tree_structure.append(f"{prefix}{connector}{item}")
            if os.path.isdir(path):
                traverse(path, prefix + ("│   " if i < len(items) - 1 else "    "))

    try:
        traverse(desktop_path)
        display_message("✅ Desktop Visual Setup Analyzed.")
        return "\n".join(tree_structure)
    except Exception as e:
        display_message(f"❌ Error Analyzing Desktop Visuals: {e}", "error")
        return "Error mapping desktop."

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
