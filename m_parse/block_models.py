from functools import wraps
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class RichText(BaseModel):
    type: str
    text: dict
    annotations: dict
    plain_text: str
    href: Optional[str]


class ParagraphBlock(BaseModel):
    rich_text: List[RichText]
    color: str


class ChildPageBlock(BaseModel):
    title: str


class CodeBlock(BaseModel):
    caption: List[RichText]
    rich_text: List[RichText]
    language: str


class Heading1Block(BaseModel):
    rich_text: List[RichText]
    color: str
    is_toggleable: Optional[bool] = None


class Heading2Block(BaseModel):
    rich_text: List[RichText]
    color: str
    is_toggleable: Optional[bool] = None


class Heading3Block(BaseModel):
    rich_text: List[RichText]
    color: str
    is_toggleable: Optional[bool] = None


class LinkToPageBlock(BaseModel):
    type: str
    page_id: str


class ParentReference(BaseModel):
    block_id: str
    type: str


class Block(BaseModel):
    object: str
    id: str
    type: str
    paragraph: Optional[ParagraphBlock] = None
    child_page: Optional[ChildPageBlock] = None
    code: Optional[CodeBlock] = None
    heading_1: Optional[Heading1Block] = None
    heading_2: Optional[Heading2Block] = None
    heading_3: Optional[Heading3Block] = None
    link_to_page: Optional[LinkToPageBlock] = None
    # Add other fields and types as necessary
    dynamic_parents: Dict[str, ParentReference] = Field(default_factory=dict)

    class Config:
        extra = "allow"


def validate_block(block_model: BaseModel):
    def decorator(func):
        @wraps(func)
        def wrapper(block_data, *args, **kwargs):
            try:
                # Dynamically select the part of the block to validate based on the block's type
                # Extract the specific part of the block data that matches the model
                block_part = getattr(block_data, block_data.type, None)

                if block_part is None:
                    raise ValueError(f"No matching block part found for type: {block_data.type}")

                # Validate the selected part of the block with the provided block model
                block_model.parse_obj(block_part.dict())

                # Call the decorated function passing the whole object if the validation is successful
                return func(block_data, *args, **kwargs)
            except Exception as e:
                print(f"Error validating or parsing block data: {e}")
                return None

        return wrapper

    return decorator


def add_dynamic_parents(block_data: dict) -> dict:
    """Processes a dictionary representing block data to extract and group all `c_parent_{i}`
    entries into a separate dictionary within the block data under the key `dynamic_parents`.

    This function iterates over each item in the provided dictionary, searching for keys that start with
    `c_parent_`. Each matching item is added to a new dictionary, `dynamic_parents`, which is then added
    back into the original block data under its own key. This is useful for handling blocks with an
    arbitrary number of parent references dynamically in the data structure.

    Parameters:
    - block_data (dict): The original dictionary of block data, potentially containing various `c_parent_{i}` keys.

    Returns:
    - dict: The modified dictionary with `c_parent_{i}` data grouped under a `dynamic_parents` key.

    Example:
    ```
    original_data = {
        "id": "some_id",
        "type": "some_type",
        "c_parent_1": {"block_id": "parent1_id", "type": "parent1_type"},
        "c_parent_2": {"block_id": "parent2_id", "type": "parent2_type"}
    }
    modified_data = add_dynamic_parents(original_data)
    print(modified_data["dynamic_parents"])
    # Output: {
    #   "c_parent_1": {"block_id": "parent1_id", "type": "parent1_type"},
    #   "c_parent_2": {"block_id": "parent2_id", "type": "parent2_type"}
    # }
    ```
    """
    dynamic_parents = {}
    for key, value in block_data.items():
        if key.startswith("c_parent_"):
            dynamic_parents[key] = value
    block_data["dynamic_parents"] = dynamic_parents
    return block_data
