import os

from m_aux.outputs import normalize_string
from m_aux.pretty_print import pretty_print


def ensure_dir(directory):
    """Ensures that a directory exists. If the directory does not exist, it is created.

    Parameters:
    - directory (str): The path of the directory to ensure.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_or_append_md_file(file_path, content):
    """Writes or appends Markdown content to a file.

    If the file exists, appends the content to it with a preceding newline character.
    Otherwise, creates a new file and writes the content.

    Parameters:
    - file_path (str): The path of the file to write to or append.
    - content (str): The Markdown content to write or append.
    """
    mode = "a" if os.path.exists(file_path) else "w"
    with open(file_path, mode, encoding="utf-8") as md_file:
        if mode == "a":
            md_file.write("\n")
        md_file.write(content + "\n")


def get_md_content(block):
    """Fetches the Markdown content for a block by its ID.

    Parameters:
    - block (dict): The block to fetch the Markdown content for.

    Returns:
    - str: The Markdown content of the block.
    """
    return block.get("md", "")


def is_root_page(block):
    """Checks if a block is a root page.

    Parameters:
    - block (dict): The block to check.

    Returns:
    - bool: True if the block is a root page, False otherwise.
    """
    return block.get("type") == "child_page" and len(block["path"].split("/")) == 1


def get_root_path(blocks):
    """Fetches the root path of the blocks.

    Parameters:
    - blocks (list): The blocks to fetch the root path for.

    Returns:
    - dict: The root path of the blocks.
    """
    for block in blocks:
        if is_root_page(block):
            return {"id": block["path"], "name": normalize_string(get_md_content(block))}
    return {}


def get_item_name(blocks, block_id):
    """Fetches the name of an item from the blocks.

    Parameters:
    - blocks (list): The blocks to fetch the item name from.
    - block_id (str): The ID of the item to fetch the name for.

    Returns:
    - str: The name of the item.
    """
    for block in blocks:
        if block["id"] == block_id:
            return normalize_string(get_md_content(block))
    return ""


def rename_to_pages(blocks, root_path):
    """Renames blocks to 'pages'.

    Parameters:
    - blocks (list): The blocks to rename.
    - root_path (dict): The root path of the blocks.

    Returns:
    - list: The renamed blocks.
    """
    renamed_blocks = []
    for block in blocks:
        rename_block = block.copy()
        if is_root_page(block):
            print("root page")
            rename_block["path"] = root_path["name"]
            rename_block["name"] = root_path["name"]
        else:
            new_path = []
            for i, item in enumerate(block["path"].split("/")):
                if i == 0:
                    new_path.append(root_path["name"])
                else:
                    calculated_name = get_item_name(blocks, item)
                    # To ignore scenarios when parent is not a page (expected)
                    if calculated_name == "":
                        continue
                    new_path.append(calculated_name)
            rename_block["path"] = "/".join(new_path)
            if block["type"] == "child_page":
                rename_block["name"] = normalize_string(get_md_content(block))
        renamed_blocks.append(rename_block)
    return renamed_blocks


def get_last_path_occurrence(input_path: str):
    """Fetches the last occurrence of a path in a string.

    Parameters:
    - input_path (str): The path to fetch the last occurrence for.

    Returns:
    - str: The last occurrence of the path.
    """
    return input_path.split("/")[-1]
