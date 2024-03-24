from typing import Any, List, Optional

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


class Block(BaseModel):
    object: str
    id: str
    type: str
    paragraph: Optional[ParagraphBlock] = None
    child_page: Optional[ChildPageBlock] = None
