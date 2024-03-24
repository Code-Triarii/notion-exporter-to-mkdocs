"""Auxiliar functions to work with Notion API blocks."""
from notion_client import Client
from m_aux.pretty_print import pretty_print

def get_all_children_blocks(notion_client:Client,page_id: str):
    """
    Get the children blocks of a given block (page_id).
    
    Parameters:
    block (dict): The block from which to extract children.
    
    Returns:
    list: A list of children blocks.
    """
    blocks = notion_client.blocks.children.list(block_id=page_id)
    pretty_print(blocks)
    return blocks.get("results",[])

def get_block_type(block:dict):
    """
    Get the type of a block.
    
    Parameters:
    block (dict): The block from which to extract the type.
    
    Returns:
    str: The type of the block.
    """
    pretty_print(f'Block: {block.get("id")}, Type: {block.get("type")}')
    return block.get("type")
    