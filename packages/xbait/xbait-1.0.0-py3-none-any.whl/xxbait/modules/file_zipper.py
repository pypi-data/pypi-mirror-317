# nyx/modules/file_zipper.py
import os
import zipfile
from nyx.utils import logger

def zip_files(files):
    zip_filename = os.path.join(os.path.expanduser("~/Desktop"), "zipped_files.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for file in files:
            zip_file.write(file, os.path.relpath(file, os.path.dirname(file)))
    display_message("✅ Files zipped successfully.")
    return zip_filename

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
