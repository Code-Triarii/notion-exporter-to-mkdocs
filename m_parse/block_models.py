from functools import wraps
from typing import List, Optional
from pydantic import BaseModel
from m_aux.pretty_print import pretty_print


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


class Block(BaseModel):
    object: str
    id: str
    type: str
    paragraph: Optional[ParagraphBlock] = None
    child_page: Optional[ChildPageBlock] = None
    code: Optional[CodeBlock] = None
    # Add other fields and types as necessary


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
