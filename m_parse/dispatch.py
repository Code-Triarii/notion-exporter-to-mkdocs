from m_aux.pretty_print import pretty_print
from m_parse.block_models import Block, add_dynamic_parents
from m_parse.markdown_processing import *


def dispatch_block_parsing(block_data: dict):
    """Dynamically dispatches block parsing based on the block type.

    This function dynamically selects and invokes a parsing function specific to the block type
    indicated in the `block_data`. It relies on consistent naming conventions between the block type
    (as specified in the 'type' field of `block_data`), and the corresponding parsing functions,
    which must be named following the pattern 'parse_{block_type}'. For example, a block type of
    'paragraph' expects a parsing function named 'parse_paragraph'.

    The function first validates the input `block_data` using the Pydantic `Block` model, ensuring
    that the data structure adheres to expected schema. It then constructs the name of the parsing
    function based on the block type and attempts to retrieve this function from the global namespace.
    If the function exists and the corresponding block type data is present, the parsing function is
    called with the block type data as its argument.

    Parameters:
    - block_data (dict): A dictionary containing the block data to parse. This data should include
      at least the 'object', 'id', 'type', and the data corresponding to the block type (e.g., 'paragraph',
      'child_page').

    Returns:
    - None: The function does not return any value. Instead, it directly invokes the relevant parsing
      functions which are responsible for handling the parsed data.

    Raises:
    - Exception: If there is an issue with validating the block data against the Pydantic model or
      if the expected parsing function does not exist or fails, an error message is printed to the console.

    Note:
    - It is crucial to maintain a consistent naming convention between block types and parsing functions
      to ensure the dynamic dispatch mechanism works correctly. Any new block type should be accompanied
      by a corresponding Pydantic model field in the `Block` model and a parsing function following the
      naming convention.
    """
    try:
        validated_block = Block.parse_obj(add_dynamic_parents(block_data))
        parse_func_name = f"parse_{validated_block.type}"
        parse_func = globals().get(parse_func_name)

        if parse_func and getattr(validated_block, validated_block.type):
            return parse_func(validated_block)
        else:
            print(f"Unsupported block type or missing data for type: {validated_block.type}")
    except Exception as e:
        print(f"Error validating or parsing block data: {e}")


def dispatch_blocks_parsing(blocks_data: list):
    """Dispatches the parsing of a list of blocks and aggregates the results, handling both single
    blocks and lists of blocks as return values from parsing functions.

    Parameters:
    - blocks_data (list): A list of block data dictionaries to be parsed.

    Returns:
    - A list of all processed blocks returned by their respective parsing functions,
      aggregated into a single list regardless of whether individual parsing functions
      return a single block or a list of blocks.
    """
    processed_blocks = []
    for block_data in blocks_data:
        result = dispatch_block_parsing(block_data)

        # Check if the parsing function returned a list of blocks or a single block
        # and append accordingly
        if isinstance(result, list):
            processed_blocks.extend(result)
        elif result is not None:
            processed_blocks.append(result)

    return processed_blocks
