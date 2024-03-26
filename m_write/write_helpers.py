import os

from m_aux.outputs import find_relative_path, normalize_string
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


def rename_to_pages(blocks):
    """Renames blocks to 'pages' and processes them based on their type.

    This function takes a list of blocks as input. Each block is a dictionary that includes an 'id' and a 'type'.
    The function first pre processes the blocks to create a mapping of block IDs to blocks.

    It then iterates over the blocks. For each block, it creates a copy and fetches its renamed path.
    The renamed path is a string of block names separated by slashes ("/"), which is fetched by calling the
    'get_renamed_path' function with the block ID.

    The function then processes the block based on its type by calling the 'process_block_type' function.
    The processed block is then appended to the list of renamed blocks.

    Finally, the function pre processes the renamed blocks again to create a new mapping of block IDs to blocks,
    and returns this mapping along with the list of renamed blocks.

    Args:
        blocks (list): The blocks to rename.

    Returns:
        tuple: A tuple containing a dictionary mapping block IDs to blocks and a list of renamed blocks.
    """
    blocks_by_id, _blocks = preprocess_blocks(blocks)
    renamed_blocks = []
    for block in _blocks:
        rename_block = block.copy()
        rename_block["named_path"] = get_renamed_path(blocks_by_id, block["id"])
        renamed_blocks.append(rename_block)
    return preprocess_blocks(renamed_blocks)


def preprocess_blocks(blocks):
    """Preprocess blocks to create a mapping by ID and a list of root blocks.

    Ensures the parent root block (the one above the automation if it does exist) is inserted as
    well for further checks and easy access
    """
    blocks_by_id = {}
    for block in blocks:
        # The empty check handles the "edge case" of non-parent root (the root of your wiki in Notion)
        # This adds trace of "parent_root_block" so it is ignored in the writing process
        if block.get("root") and block.get("path") != "" and block.get("type") == "child_page":
            parent_root_block = block.copy()
            parent_root_block["id"] = parent_root_block["path"]
            parent_root_block["type"] = "parent_root_page"
            blocks_by_id[block["path"]] = parent_root_block

        blocks_by_id[block["id"]] = block
    return blocks_by_id, blocks


def get_renamed_path(blocks_by_id, block_id):
    """Fetches the renamed path for a block by its ID.

    This function takes a dictionary mapping block IDs to blocks and a block ID as input.
    It then fetches the block corresponding to the given ID and retrieves its path.
    The path is a string of block IDs separated by slashes ("/").

    The function then splits the path into individual block IDs and iterates over them.
    For each block ID in the path, it fetches the corresponding block and checks its type.
    If the block type is "child_page", it appends the block's name to the result path.
    If the block type is "parent_root_page" and the path contains only one block ID,
    it also appends the block's name to the result path.

    Finally, the function joins the result path back into a string, with block names separated by slashes,
    and returns this string.

    Args:
        blocks_by_id (dict): A dictionary mapping block IDs to blocks.
        block_id (str): The ID of the block for which to fetch the renamed path.

    Returns:
        str: The renamed path for the block, with block names separated by slashes.
    """
    block = blocks_by_id.get(block_id)
    result_path = []
    splitted_path = block.get("path").split("/")

    for path_ref in splitted_path:
        block_ref = blocks_by_id.get(path_ref)
        if block_ref:
            if block_ref.get("type") == "child_page":
                result_path.append(block_ref["name"])
            # We would like to substitute only for the root block for the "parent_root_page" type
            elif block_ref.get("type") == "parent_root_page" and len(splitted_path) == 1:
                result_path.append(block_ref["name"])
    return "/".join(result_path)


def get_last_path_occurrence(input_path: str):
    """Fetches the last occurrence of a path in a string.

    Parameters:
    - input_path (str): The path to fetch the last occurrence for.

    Returns:
    - str: The last occurrence of the path.
    """
    return input_path.split("/")[-1]


##################################################
#                                                #
#         SPECIFIC BLOCKS PROCESSING             #
#                                                #
##################################################


def process_block_type(blocks_by_id, block):
    """Dispatches the block to the appropriate processing function based on its type."""
    # Map of block types to their processing functions
    type_processing_map = {
        "link_to_page": process_link_to_page,
    }

    # Get the processing function from the map using the block's type
    process_func = type_processing_map.get(block["type"])

    # If a processing function is found, call it, otherwise return the block unchanged
    if process_func:
        return process_func(blocks_by_id, block)
    else:
        return block


def process_link_to_page(blocks_by_id, block):
    """Processes a 'link_to_page' block."""
    reference_block_id = block.get("external_url")
    if reference_block_id:
        # Based on Notion structure of urls. Sample: https://www.notion.so/<page-name>-328968aac13d4b19b2a6e2b9c257e05c
        reference_block = blocks_by_id.get(reference_block_id.split("-")[-1])
        if reference_block:
            relative_path = find_relative_path(block["named_path"], reference_block["named_path"])
            block["md"] = f"[{reference_block['name']}]({relative_path}/{reference_block['name']})"
    return block
