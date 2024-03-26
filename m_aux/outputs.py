import os
import re
import shutil

import requests


def is_folder(path):
    """Check if the given path points to a folder.

    Parameters:
    - path (str): The path to check.

    Returns:
    - bool: True if the path points to a folder, False otherwise.
    """
    # Check if the path exists and is a directory
    return os.path.exists(path) and os.path.isdir(path)


def prepare_output_folder(folder_path):
    """Prepare the output folder by ensuring the specified folder exists and is empty.

    Parameters:
    - folder_path (str): The path to the folder to prepare.
    """
    # Check if the path is indeed a folder
    if not is_folder(folder_path):
        if os.path.exists(folder_path):
            # Path exists but is not a folder (likely a file), operation is aborted
            print(f"Error: The path '{folder_path}' is not a folder.")
            return
        else:
            # Path does not exist, create the folder
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
            return

    # If the folder exists, empty it
    try:
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' was emptied and recreated.")
    except Exception as e:
        print(f"An error occurred while preparing the folder: {e}")


def normalize_string(name):
    """Normalizes names for files and directories."""
    # Replace spaces with dashes, remove special characters, trim, and lowercase
    name = re.sub(r"\s+", "-", name)  # Spaces to dashes
    name = re.sub(r"[^\w\-]", "", name)  # Remove non-word characters except dashes
    name = name.strip("-")  # Trim leading and trailing dashes
    name = name.replace("-", "")  # Replace remaining dashes with nothing
    return name.lower()


def find_relative_path(from_path, to_path):
    """Finds the relative path from one path to another.

    :param from_path: The starting path.
    :param to_path: The target path.
    :return: The relative path from the start to the target.
    """
    # Split paths into components
    from_parts = from_path.split("/")
    to_parts = to_path.split("/")

    # Find the common prefix length
    common_length = 0
    for from_part, to_part in zip(from_parts, to_parts):
        if from_part == to_part:
            common_length += 1
        else:
            break

    # Calculate the number of directory levels to go up from the from_path
    up_levels = len(from_parts) - common_length

    # Construct the relative path
    relative_parts = [".."] * up_levels + to_parts[common_length:]
    relative_path = "/".join(relative_parts)

    return relative_path


def download_and_save_image_or_video(url: str, type: str, dest_file: str):
    """Downloads content from a URL and saves it to a specific path with an appropriate extension.

    Parameters:
    - url (str): The URL to download the content from.
    - type (str): The type of the content ('image' or 'video').
    - dest_file (str): The destination path to save the content, without the file extension.

    Raises:
    - ValueError: If the type is not 'image' or 'video'.
    - requests.RequestException: For issues encountered during the request for downloading the content.
    """
    # Validate the type
    if type not in ["image", "video"]:
        raise ValueError("Type must be either 'image' or 'video'")

    # Determine the file extension based on the type
    extension = ".png" if type == "image" else ".mp4"
    full_path = f"{dest_file}{extension}"

    # Make the request and check for a successful response
    try:
        response = requests.get(url, stream=True, timeout=180)
        response.raise_for_status()  # Will raise an exception for 4XX/5XX responses

        # Save the content to the specified file
        with open(full_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Content downloaded and saved to {full_path}")
        return True
    except requests.RequestException as e:
        print(f"Failed to download content from {url}: {e}")
    return False
