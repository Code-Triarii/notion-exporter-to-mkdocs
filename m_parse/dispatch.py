from m_parse.block_models import Block
from m_parse.markdown_processing import *

def dispatch_block_parsing(block_data: dict):
    try:
        validated_block = Block.parse_obj(block_data)
        # Dynamically get the parsing function based on block type
        parse_func_name = f"parse_{validated_block.type}"
        parse_func = globals().get(parse_func_name)
        
        if parse_func and getattr(validated_block, validated_block.type):
            parse_func(getattr(validated_block, validated_block.type))
        else:
            print(f"Unsupported block type or missing data for type: {validated_block.type}")
    except Exception as e:
        print(f"Error validating or parsing block data: {e}")


def dispatch_blocks_parsing(blocks_data: list):
    """
    Dispatches the parsing of a list of blocks.

    Parameters:
    - blocks_data (list): A list of block data dictionaries to be parsed.

    Returns:
    - None
    """
    for block_data in blocks_data:
        dispatch_block_parsing(block_data)