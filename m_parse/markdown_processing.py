from m_aux.pretty_print import pretty_print
from m_parse.block_models import (
    ChildPageBlock,
    CodeBlock,
    Heading1Block,
    Heading2Block,
    Heading3Block,
    ParagraphBlock,
    validate_block,
)
from m_parse.markdown_processing_helpers import (
    markdown_code_block,
    markdown_headings,
    markdown_table,
)
from m_search.notion_pages import fetch_page_details


@validate_block(ParagraphBlock)
def parse_paragraph(block: ParagraphBlock):
    return [{"fake": "data"}, {"fake_child": "data"}, {"fake_child": "data"}]


@validate_block(Heading1Block)
def parse_heading_1(block: Heading1Block):
    # Assuming rich_text always has at least one item and you want to use the first one for the heading
    heading_text = block.heading_1.rich_text[0].plain_text if block.heading_1.rich_text else ""
    # We move heading_1 to heading_2 level in the markdown because the page title will be the heading_1
    return {"id": block.id, "md": markdown_headings(heading_text, 2)}


@validate_block(Heading2Block)
def parse_heading_2(block: Heading2Block):
    # Extracting the heading text from the first item of rich_text, if available
    heading_text = block.heading_2.rich_text[0].plain_text if block.heading_2.rich_text else ""
    # Using the markdown_headings function to format as an H2 heading
    return {"id": block.id, "md": markdown_headings(heading_text, 3)}


@validate_block(Heading3Block)
def parse_heading_3(block: Heading3Block):
    heading_text = block.heading_3.rich_text[0].plain_text if block.heading_3.rich_text else ""
    return {"id": block.id, "md": markdown_headings(heading_text, 4)}


@validate_block(CodeBlock)
def parse_code(block: CodeBlock):
    pretty_print(block.code.rich_text[0].text["content"])
    return {
        "id": block.id,
        "md": markdown_code_block(
            code=block.code.rich_text[0].text["content"],
            caption=block.code.caption[0].text["content"],
            language=block.code.language,
        ),
    }


def get_page_changelog(page_details: dict) -> str:
    """Extracts changelog information from page details and formats it into a markdown table.

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
    """Parses a ChildPageBlock, fetches the page details, and generates a list of processed blocks.

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
