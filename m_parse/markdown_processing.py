from m_aux.pretty_print import pretty_print
from m_parse.block_models import ChildPageBlock, ParagraphBlock, CodeBlock, validate_block
from m_parse.markdown_processing_helpers import markdown_headings, markdown_table, markdown_code_block
from m_search.notion_pages import fetch_page_details


@validate_block(ParagraphBlock)
def parse_paragraph(block: ParagraphBlock):
    return [{"fake": "data"}, {"fake_child": "data"}, {"fake_child": "data"}]

@validate_block(CodeBlock)
def parse_code(block: CodeBlock):
    pretty_print(block.code.rich_text[0].text["content"])
    return {
        "id": block.id,
        "md": markdown_code_block(code=block.code.rich_text[0].text["content"], caption=block.code.caption[0].text["content"], language=block.code.language)
    }

def get_page_changelog(page_details: dict) -> str:
    """
    Extracts changelog information from page details and formats it into a markdown table.

    Parameters:
    - page_details (dict): The details of the page.

    Returns:
    - str: A markdown table containing the changelog information.
    """
    owner = (
        page_details.get("properties", {})
        .get("Owner", {})
        .get("people", [{}])[0]
        .get("name", "N/A")
        if page_details.get("properties", {}).get("Owner", {}).get("people")
        else "N/A"
    )
    created_time = (
        page_details.get("properties", {}).get("Created time", {}).get("created_time", "")
    )
    last_edited_time = (
        page_details.get("properties", {}).get("Last edited time", {}).get("last_edited_time", "")
    )
    created_by = page_details.get("created_by", {}).get(
        "id", ""
    )  # Assuming you want the ID; adjust as necessary

    # Organizing data for the markdown_table function
    headers = [" ", " "]
    rows = [
        ["Owner", owner],
        ["Created time", created_time],
        ["Last edited time", last_edited_time],
        ["Created by", created_by],
    ]

    # Using markdown_table to format the changelog
    return markdown_table(headers, rows)


@validate_block(ChildPageBlock)
def parse_child_page(block: ChildPageBlock):
    """
    Parses a ChildPageBlock, fetches the page details, and generates a list of processed blocks.

    This function is decorated with the validate_block decorator, which checks if the block is of the correct type.

    Parameters:
    - block (ChildPageBlock): The block to parse.

    Returns:
    - list: A list of dictionaries, where each dictionary represents a processed block and contains its ID and markdown content.
    """
    page_processed_blocks = []
    page_details = fetch_page_details(block.id)
    changelog = get_page_changelog(page_details)
    page_processed_blocks.append({"id": block.id, "md": markdown_headings(block.child_page.title)})
    page_processed_blocks.append({"id": block.id, "md": changelog})
    return page_processed_blocks
