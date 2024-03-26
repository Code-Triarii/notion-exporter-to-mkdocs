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

def is_in_blocks_dict_by_id(blocks, block_id: str, block_type: str = None):
    """Checks if a block is in a list of blocks by its ID."""
    if block_type:
        return any(block_id == block["id"] and block_type == block["type"] for block in blocks)
    return any(block_id == block["id"] for block in blocks)


def is_root_page(block):
    """Checks if a block part of the root page.
    Before renaming

    Parameters:
    - block (dict): The block to check.

    Returns:
    - bool: True if the block is a root page, False otherwise.
    """
    return len(block["path"].split("/")) == 1


def get_root_path(blocks):
    """Fetches the root path of the blocks.
    Before renaming

    Parameters:
    - blocks (list): The blocks to fetch the root path for.

    Returns:
    - dict: The root path of the blocks.
    """
    for block in blocks:
        if is_root_page(block):
            return {"id": block["path"], "name": normalize_string(get_md_content(block))}
    return {}


def get_item_name(blocks_by_id, block_id):
    # TODO: Refactor name to be less confusing because this is not retrieving names for all types of items
    """Fetches the name of an item from the blocks.

    Parameters:
    - blocks (list): The blocks to fetch the item name from.
    - block_id (str): The ID of the item to fetch the name for.

    Returns:
    - str: The name of the item.
    """
    pretty_print(block_id, "blocks_by_id in get name")
    block = blocks_by_id.get(block_id)
    pretty_print(block, "block in get name")
    if block:
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
    blocks_by_id, _blocks = preprocess_blocks(blocks)
    renamed_blocks = []
    for block in _blocks:
        rename_block = block.copy()
        if is_root_page(block):
            rename_block["path"] = root_path["name"]
            rename_block["name"] = root_path["name"]
        else:
            new_path = []
            for item in block["path"].split("/"):
                calculated_name = get_item_name(blocks_by_id, item)
                # To ignore scenarios when parent is not a page (expected)
                if calculated_name == "":
                    continue
                new_path.append(calculated_name)
            rename_block["path"] = "/".join(new_path)
            if block["type"] == "child_page":
                rename_block["name"] = normalize_string(get_md_content(block))
        renamed_blocks.append(rename_block)
    return renamed_blocks

def preprocess_blocks(blocks):
    """
    Preprocess blocks to create a mapping by ID and a list of root blocks.
    """
    blocks_by_id = {block["id"]: block for block in blocks}
    return blocks_by_id, blocks



def get_last_path_occurrence(input_path: str):
    """Fetches the last occurrence of a path in a string.

    Parameters:
    - input_path (str): The path to fetch the last occurrence for.

    Returns:
    - str: The last occurrence of the path.
    """
    return input_path.split("/")[-1]

