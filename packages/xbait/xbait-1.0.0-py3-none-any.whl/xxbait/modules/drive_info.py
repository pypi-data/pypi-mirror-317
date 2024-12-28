# nyx/modules/drive_info.py
import psutil
from nyx.utils import logger

def get_drive_info():
    drives_info = []
    try:
        for partition in psutil.disk_partitions(all=False):
            usage = psutil.disk_usage(partition.mountpoint)
            drive_info = {
                "Name": partition.device,
                "Type": partition.fstype,
                "Total Capacity": f"{usage.total / (1024 ** 3):.2f} GB",
                "Used Space": f"{usage.used / (1024 ** 3):.2f} GB",
                "Free Space": f"{usage.free / (1024 ** 3):.2f} GB",
            }
            drives_info.append(drive_info)

        display_message("✅ Drive Info Updated Successfully.")
        return drives_info
    except Exception as e:
        display_message(f"❌ Error Updating Drive Information: {e}", "error")
        return []

def display_message(message, level="info"):
    if level == "info":
        print(f"[+] {message}")
    elif level == "warning":
        print(f"[!] {message}")
    elif level == "error":
        print(f"[-] {message}")
