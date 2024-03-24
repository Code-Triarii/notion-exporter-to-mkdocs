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
        add_parent_hierarchy(notion_client, current_block, parent_hierarchy.copy())
        
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

def add_parent_hierarchy(notion_client, block, parent_hierarchy=[]):
    """
    Recursively adds parent hierarchy identifiers to a block.
    Parameters:
    - notion_client: Instance of Notion client to fetch blocks.
    - block: The current block being processed (dict).
    - parent_hierarchy: A list of dictionaries each containing parent block_id and type collected up to the current depth.
    """
    # Use .get() to safely access dictionary keys
    parent_block = block.get("parent", {})
    parent_id = parent_block.get("block_id")
    parent_type = block.get("type")

    if parent_id:
        # Append a new dictionary with parent_id and parent_type to the hierarchy list
        parent_hierarchy.append({"block_id": parent_id, "type": parent_type})
        
        # Add c_parent hierarchy information to the block
        for i, parent_info in enumerate(parent_hierarchy):
            key = f"c_parent_{i}" if i > 0 else "c_parent"
            block[key] = parent_info

    # If the block has children, iterate over them and apply the function recursively
    if block.get("has_children", False):
        child_blocks = get_all_children_blocks(notion_client, block["id"])
        for child in child_blocks:
            # Recursive call with the updated list of parent hierarchy
            add_parent_hierarchy(notion_client, child, parent_hierarchy.copy())

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
