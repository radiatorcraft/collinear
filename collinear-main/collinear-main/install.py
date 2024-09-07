import requests
import os
import zipfile
import json

def download_and_extract_repo(repo_url, destination_dir):
    """Downloads the latest zip archive from a GitHub repository and extracts it to a specified directory.

    Args:
        repo_url (str): The URL of the GitHub repository.
        destination_dir (str): The directory where the files will be downloaded and extracted.
    """

    # Get the zipball URL (assuming the latest release)
    zipball_url = repo_url + "/archive/refs/heads/main.zip"

    # Download confirmation
    print(f"Downloading repository archive from: {zipball_url}")

    # Download the zipball
    try:
        response = requests.get(zipball_url, stream=True)
        response.raise_for_status()

        # Create a temporary directory for download and extraction
        temp_dir = os.path.join(destination_dir, "collinear_temp")
        os.makedirs(temp_dir, exist_ok=True)

        with open(os.path.join(temp_dir, "collinear-main.zip"), "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Downloaded repository archive to: {os.path.join(temp_dir, 'collinear-main.zip')}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading repository: {e}")
        return

    # Extract the zipball
    try:
        with zipfile.ZipFile(os.path.join(temp_dir, "collinear-main.zip"), "r") as zip_ref:
            zip_ref.extractall(destination_dir)
            print("Extracted repository contents successfully.")
    except zipfile.ZipException as e:
        print(f"Error extracting repository: {e}")
    finally:
        # Cleanup - remove the temporary directory and downloaded zipball
        os.remove(os.path.join(temp_dir, "collinear-main.zip"))
        os.rmdir(temp_dir)

    # Get username and password from user
    username = input("Enter your scratch username: ")
    password = input("Enter your scratch password: ")

    # Create the JSON configuration file
    config_path = os.path.join(destination_dir, "collinear-main", "paths.json")
    config_data = {
        "log_path": os.path.join(destination_dir, "collinear-main", "log.txt"),
        "settings_path": os.path.join(destination_dir, "collinear-main", "settings.json"),
        "username": username,
        "password": password,
        "user_list": os.path.join(destination_dir, "collinear-main", "usernames.txt"),
        "error_path": os.path.join(destination_dir, "collinear-main", "error.log")
    }

    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4)

    print(f"Created configuration file at: {config_path}")

if __name__ == "__main__":
    # Replace with the actual URL of your GitHub repository
    repo_url = "https://github.com/radiatorcraft/collinear"
    destination_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory of the script

    # Confirmation for installation location
    print(f"Installing repository to: {destination_dir}")
    user_confirmation = input("Are you sure you want to overwrite existing files? (y/n): ")
    if user_confirmation.lower() == "y":
        download_and_extract_repo(repo_url, destination_dir)
    else:
        print("Installation cancelled.")