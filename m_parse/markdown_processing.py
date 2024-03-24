from m_aux.pretty_print import pretty_print
from m_parse.block_models import ChildPageBlock, ParagraphBlock, validate_block
from m_parse.markdown_processing_helpers import markdown_headings, markdown_table
from m_search.notion_pages import fetch_page_details


@validate_block(ParagraphBlock)
def parse_paragraph(block: ParagraphBlock):
    pretty_print(block)
    return [{"fake": "data"}, {"fake_child": "data"}, {"fake_child": "data"}]


def get_page_changelog(page_details: dict) -> str:
    # Extracting necessary information
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
    headers = ["Key", "Value"]
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
    page_processed_blocks = []
    page_details = fetch_page_details(block.id)
    changelog = get_page_changelog(page_details)
    page_processed_blocks.append({"id": block.id, "md": markdown_headings(block.child_page.title)})
    page_processed_blocks.append({"id": block.id, "md": changelog})
    pretty_print(page_processed_blocks)
    return page_processed_blocks
