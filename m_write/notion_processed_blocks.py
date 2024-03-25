"""Module for processing and writing Notion blocks to Markdown files."""

import os
from m_write.write_helpers import ensure_dir, write_md_file, find_page_title
from m_aux.outputs import normalize_string
from m_aux.pretty_print import pretty_print

# def process_blocks(blocks, root_dir, parent_id=None):
#     """Processes and writes blocks to the appropriate .md files and directories, with improvements."""
#     for block in blocks:
#         # Handle 'child_page' blocks differently to use their title for naming
#         if block['type'] == 'child_page':
#             page_title = find_page_title(blocks, block['id'])
#             # Normalize the page title for use in file and directory names
#             normalized_title = normalize_string(page_title)
#             output_path = os.path.join(root_dir, block['path'].replace('/', os.sep), normalized_title)
#             ensure_dir(output_path)  # Ensure the directory for the page exists
#             output_file = os.path.join(output_path, normalized_title + ".md")
#         else:
#             # Find the title of the parent page for non-'child_page' blocks
#             if parent_id:
#                 parent_title = find_page_title(blocks, parent_id)
#                 normalized_title = normalize_string(parent_title)
#                 output_path = os.path.join(root_dir, block['path'].replace('/', os.sep), normalized_title)
#             else:
#                 output_path = os.path.join(root_dir, block['path'].replace('/', os.sep))
#             ensure_dir(output_path)
#             output_file = os.path.join(output_path, normalize_string(block['md'][:50]) + ".md")  # Use first 50 chars of md as filename
        
#         write_md_file(output_file, block['md'])

#         # Recursively process subpages for 'child_page' blocks
#         if block['type'] == 'child_page':
#             subpages = [b for b in blocks if b['path'].startswith(block['path']) and b['id'] != block['id']]
#             if subpages:
#                 process_blocks(subpages, output_path, block['id'])


def process_blocks(blocks, root_dir):
  pretty_print(blocks, "Processed blocks")