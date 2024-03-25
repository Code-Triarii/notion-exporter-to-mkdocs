"""Module for processing and writing Notion blocks to Markdown files."""

import os
from m_write.write_helpers import ensure_dir, write_md_file, find_page_title
from m_aux.pretty_print import pretty_print

def process_and_write(blocks, root_dir):
    """
    Processes the blocks and writes them to markdown files and directories.
    """
    ensure_dir(root_dir)  # Ensure the root directory exists

    # Sort blocks by path length to ensure parent directories are created first
    blocks.sort(key=lambda x: x['path'].count('/'))

    for block in blocks:
        # Extract directory path from the block's path and title for filename
        dir_path_parts = block['path'].split('/')
        if block['type'] == 'child_page':
            # The title of the page becomes the name of the directory
            page_title = find_page_title(blocks, block['id'])
            dir_path = os.path.join(root_dir, *dir_path_parts, page_title)
            file_path = os.path.join(dir_path, f"{page_title}.md")
            ensure_dir(dir_path)  # Ensure the directory exists
        else:
            parent_page_title = find_page_title(blocks, dir_path_parts[-1])
            parent_dir_path = os.path.join(root_dir, *dir_path_parts[:-1])
            file_path = os.path.join(parent_dir_path, f"{parent_page_title}.md")

        # Append or write the content to the markdown file
        if os.path.exists(file_path):
            mode = 'a'  # Append if the file exists
        else:
            mode = 'w'  # Create a new file if it does not exist
        with open(file_path, mode, encoding='utf-8') as md_file:
            if mode == 'a':
                md_file.write('\n\n')  # Add some space between content blocks
            md_file.write(block['md'])