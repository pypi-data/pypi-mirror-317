# nyx/modules/disclaimer.py
import sys

# COLORS
green_text = "\033[92m"  # ANSI escape code for green text
red_text = "\033[91m"   # ANSI escape code for red text
yellow_text = "\033[93m" # ANSI escape code for yellow text
reset_text = "\033[0m"   # ANSI escape code to reset to default text color

def display_message(message, level="info"):
    color_codes = {
        "info": green_text,
        "warning": yellow_text,
        "error": red_text
    }
    reset_code = reset_text
    color_code = color_codes.get(level, "")
    print(f"{color_code}{message}{reset_code}")

def display_disclaimer():
    nyx_ascii = f"""
{green_text}                ███╗   ██╗██╗   ██╗██╗  ██╗
                ████╗  ██║╚██╗ ██╔╝╚██╗██╔╝
                ██╔██╗ ██║ ╚████╔╝  ╚███╔╝
                ██║╚██╗██║  ╚██╔╝   ██╔██╗
                ██║ ╚████║   ██║   ██╔╝ ██╗
                ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝{reset_text}
"""

    disclaimer = f"""{nyx_ascii}
{green_text}==================== NYX DISCLAIMER ====================

This script was created by NYX with the intent to foster
EDUCATION, ETHICAL LEARNING, and CYBERSECURITY AWARENESS.

WARNING!!!

- This tool is STRICTLY for legal and ethical purposes.
- Unauthorized use, exploitation, or distribution is STRICTLY PROHIBITED.
- The developer assumes NO LIABILITY for misuse or illegal activity.

By using this script, you confirm:
1. You understand and accept the terms outlined here.
2. You will use the tool responsibly and adhere to all applicable laws.

Do you agree to these terms?
[Y] Yes, I agree and will use responsibly
[N] No, I do not agree

=================== END OF DISCLAIMER ===================

{reset_text}"""  # Reset text color after the disclaimer

    print(disclaimer)

    while True:
        user_response = input("\rEnter your choice (Y/N): ").strip().upper()
        if user_response == "Y":
            print()
            display_message("✅ Disclaimer accepted. Proceeding...")
            return True
        elif user_response == "N":
            print()
            display_message("❌ Declined. Exiting safely...", "error")
            sys.exit(0)
        else:
            display_message("Invalid input. Please type Y or N.", "error")

def select_platform():
    while True:
        display_message("\n[+] ✅ SELECT A PLATFORM TO PROCEED\n", "info")

        print("[1] WINDOWS    [2] LINUX    [3] MAC")
        user_choice = input("Enter the number of your choice: ").strip()

        if user_choice == "1":
            display_message("\n[+] ✅ PROCEEDING TO WINDOWS OPTIONS\n", "info")
            return "1"
        elif user_choice in ["2", "3"]:
            print()
            display_message("[!] This Section is still under development. Please select another option.", "warning")
        else:
            display_message("[!] Invalid input. Please select a number from the options.", "error")
