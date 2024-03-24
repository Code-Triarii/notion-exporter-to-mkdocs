"""Auxiliar functions to work with Notion API blocks."""
from notion_client import Client
from m_aux.pretty_print import pretty_print

def fetch_and_process_block_hierarchy(notion_client, root_block_id):
    """
    Fetches a block by its ID and processes its hierarchy, including all nested children.

    Parameters:
    - notion_client: The Notion client used to fetch blocks.
    - root_block_id: The ID of the root block to start processing from.

    Returns:
    - list: A list of all processed blocks, each with added parent hierarchy information.
    """
    processed_blocks = []

    def process_block(block_id, parent_hierarchy=[]):
        """
        Recursively processes a block and its children, adding parent hierarchy information.
        
        Parameters:
        - block_id: The ID of the current block being processed.
        - parent_hierarchy: The accumulated parent hierarchy for the current block.
        """
        # Fetch the current block's details (assuming a function or method exists to do this)
        current_block = fetch_block_details(notion_client, block_id)
        if not current_block:
            return
        
        # Add parent hierarchy information to the current block
        add_parent_hierarchy(current_block, parent_hierarchy.copy())
        
        # Add the processed block to the list
        processed_blocks.append(current_block)

        # If the block has children, process each child
        if current_block.get("has_children", False):
            child_blocks = get_all_children_blocks(notion_client, block_id)
            for child in child_blocks:
                # Construct new parent hierarchy for the child
                new_parent_hierarchy = parent_hierarchy.copy()
                new_parent_hierarchy.append({"block_id": block_id, "type": current_block.get("type")})
                process_block(child["id"], new_parent_hierarchy)

    # Start processing from the root block
    process_block(root_block_id)
    return processed_blocks

def add_parent_hierarchy(block, parent_hierarchy=[]):
    """
    Adds parent hierarchy identifiers to a block, ensuring no duplications and starting labeling from c_parent_1.

    Parameters:
    - block: The current block being processed (dict).
    - parent_hierarchy: A list of dictionaries each containing parent block_id and type collected up to the current depth.
    """
    parent_block = block.get("parent", {})
    parent_id = (parent_block.get("block_id") or parent_block.get("page_id")).strip()
    parent_type = block.get("type")

    # Normalize block_id before comparison
    normalized_parent_id = parent_id.replace("-", "")

    # Check the entire hierarchy for duplication
    is_duplicate = any((parent.get("block_id").replace("-", "") == normalized_parent_id) for parent in parent_hierarchy)

    if not is_duplicate and parent_id:
        parent_hierarchy.append({"block_id": parent_id, "type": parent_type})

    # Assign the parent hierarchy to the block with adjusted keys starting from c_parent_1
    for i, parent_info in enumerate(parent_hierarchy, start=1):
        key = f"c_parent_{i}"
        block[key] = parent_info


def get_all_children_blocks(notion_client:Client,page_id: str):
    """
    Get the children blocks of a given block (page_id).
    
    Parameters:
    block (dict): The block from which to extract children.
    
    Returns:
    list: A list of children blocks.
    """
    blocks = notion_client.blocks.children.list(block_id=page_id)
    return blocks.get("results",[])

def fetch_block_details(notion_client, block_id):
    """
    Fetches the details of a block given its ID. Placeholder for actual implementation.
    
    Parameters:
    - notion_client: The Notion client used to fetch blocks.
    - block_id: The ID of the block to fetch.

    Returns:
    - dict: The details of the fetched block.
    """
    return notion_client.blocks.retrieve(block_id=block_id) if block_id else None 
