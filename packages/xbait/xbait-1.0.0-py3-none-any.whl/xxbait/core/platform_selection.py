# iscout/core/platform_selection.py
import sys

def select_platform():
    while True:
        print("\n\033[92m[+] ✅ SELECT A PLATFORM TO PROCEED\033[0m")
        print("[1] WINDOWS    [2] LINUX    [3] MAC")
        user_choice = input("Enter the number of your choice: ").strip()

        if user_choice == "1":
            print("\n\033[92m[+] ✅ PROCEEDING TO WINDOWS OPTIONS\033[0m")
            return "1"
        elif user_choice in ["2", "3"]:
            print("\n[-] \033[91mThis Section is still under development. Please select another option.\033[0m")
        else:
            print("\n[!] \033[91mInvalid input. Please select a number from the options.\033[0m")
