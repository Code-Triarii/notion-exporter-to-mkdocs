from m_parse.block_models import ChildPageBlock, ParagraphBlock, validate_block
from m_aux.pretty_print import pretty_print


@validate_block(ParagraphBlock)
def parse_paragraph(block: ParagraphBlock):
    print("Parsing paragraph block")
    pretty_print(block)
    return [{"fake": "data"}, {"fake_child": "data"}, {"fake_child": "data"}]

@validate_block(ChildPageBlock)
def parse_child_page(block: ChildPageBlock):
    print("Parsing child page block")
    pretty_print(block)
    return {"fake_child": "data"}
