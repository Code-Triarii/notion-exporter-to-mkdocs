import os
from m_aux.outputs import normalize_string

def ensure_dir(directory):
    """Ensures that a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_md_file(file_path, content):
    """Writes Markdown content to a file."""
    with open(file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(content)

def find_page_title(blocks, block_id):
    """Finds a page title given a block ID."""
    for block in blocks:
        if block['id'] == block_id and 'md' in block:
            return normalize_string(block['md'].strip('# ').strip())
    return None

def get_md_content(blocks, block_id):
    """Fetches the Markdown content for a block by its ID."""
    for block in blocks:
        if block['id'] == block_id:
            return block['md']
    return None

def is_page(blocks, block_id):
    """Checks if a block is of type 'child_page'."""
    for block in blocks:
        if block['id'] == block_id:
            return block['type'] == 'child_page'
    return False