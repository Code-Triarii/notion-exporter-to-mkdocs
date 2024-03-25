"""Module for processing and writing Notion blocks to Markdown files."""

import os

from m_aux.outputs import normalize_string
from m_aux.pretty_print import pretty_print
from m_write.write_helpers import (
    ensure_dir,
    get_last_path_occurrence,
    get_root_path,
    rename_to_pages,
    write_or_append_md_file,
)


def process_and_write(blocks, root_dir):
    """Processes the blocks and writes them to markdown files and directories."""
    ensure_dir(root_dir)  # Ensure the root directory exists

    # Sort blocks by path length to ensure parent directories are created first
    blocks.sort(key=lambda x: x["path"].count("/"))
    # This is the parent of the root passed as parameter from CLI if any
    root_path = get_root_path(blocks)
    pretty_print(root_path, "Root path")
    renamed_blocks = rename_to_pages(blocks, root_path)
    pretty_print(renamed_blocks, "renamed_blocks")

    for block in renamed_blocks:
        # Creates the appropriate directory structure and files based on pages only
        if block.get("type") == "child_page":
            # If the path and md matches, then it is the root
            if normalize_string(block.get("md")) == block.get("path"):
                # Create a directory for the block
                block_dir = os.path.join(root_dir, block["path"])
                # For any other pages it appends the name to the root path
            else:
                block_dir = os.path.join(root_dir, block["path"], block["name"])

            ensure_dir(block_dir)
            file_path = os.path.join(block_dir, f"{block['name']}.md")
            write_or_append_md_file(file_path, block.get("md", ""))

        else:
            target_file_name = get_last_path_occurrence(block["path"])
            file_path = os.path.join(root_dir, block["path"], f"{target_file_name}.md")
            write_or_append_md_file(file_path, block.get("md", ""))
