from m_parse.block_models import ParagraphBlock, ChildPageBlock

def parse_paragraph(block: ParagraphBlock):
    print("Parsing paragraph block")
    return [{"fake": "data"},{"fake_child": "data"},{"fake_child": "data"}]

def parse_child_page(block: ChildPageBlock):
    print("Parsing child page block")
    # Implement the parsing logic
    return {"fake_child": "data"}
