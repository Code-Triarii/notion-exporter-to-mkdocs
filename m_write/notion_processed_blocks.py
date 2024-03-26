"""Module for processing and writing Notion blocks to Markdown files."""

import os

from m_aux.outputs import normalize_string
from m_aux.pretty_print import pretty_print
from m_write.write_helpers import (
    ensure_dir,
    get_last_path_occurrence,
    process_block_type,
    rename_to_pages,
    write_or_append_md_file,
)


def process_and_write(blocks, root_dir):
    """Processes the blocks and writes them to markdown files and directories."""
    ensure_dir(root_dir)  # Ensure the root directory exists

    # Sort blocks by path length to ensure parent directories are created first
    blocks.sort(key=lambda x: x["path"].count("/"))
    renamed_blocks_id, renamed_blocks = rename_to_pages(blocks)
    pretty_print(renamed_blocks, "Renamed Blocks")

    for block in renamed_blocks:
        block = process_block_type(renamed_blocks_id, block)
        # Creates the appropriate directory structure and files based on pages only
        if block.get("type") == "child_page":
            # If the path and md matches, then it is the root
            if block.get("root"):
                # Create a directory for the block
                block_dir = os.path.join(root_dir, block["named_path"])
            else:
                # For any other pages it appends the name (of the page) to the root path
                block_dir = os.path.join(root_dir, block["named_path"], block["name"])
            ensure_dir(block_dir)
            file_path = os.path.join(block_dir, f"{block['name']}.md")
            write_or_append_md_file(file_path, block.get("md", ""))
        elif block.get("type") == "parent_root_page":
            continue
        else:
            target_file_name = get_last_path_occurrence(block["named_path"])
            file_path = os.path.join(root_dir, block["named_path"], f"{target_file_name}.md")
            write_or_append_md_file(file_path, block.get("md", ""))
