import os
import re
import shutil


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
    return name.lower()
