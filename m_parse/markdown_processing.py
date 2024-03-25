from m_aux.pretty_print import pretty_print
from m_parse.block_models import (
    Block,
    ChildPageBlock,
    CodeBlock,
    Heading1Block,
    Heading2Block,
    Heading3Block,
    LinkToPageBlock,
    ParagraphBlock,
    QuoteBlock,
    validate_block,
)
from m_parse.markdown_processing_helpers import (
    markdown_code_block,
    markdown_convert_paragraph_styles,
    markdown_headings,
    markdown_link,
    markdown_note_with_heading,
    markdown_table,
)
from m_search.notion_pages import fetch_page_details

##################################################
#                                                #
#                 AUX FUNCTIONS                  #
#                                                #
##################################################


def calculate_path_on_hierarchy(block: Block) -> str:
    """Calculates the path for a given block based on its hierarchy of parent pages.

    This function iterates through the `dynamic_parents` dictionary of a block, filtering for parents
    that are of type 'child_page'. The resulting path is constructed by concatenating these filtered
    parents' identifiers in order, separated by slashes ('/').

    Parameters:
    - block (Block): The block object for which to calculate the hierarchy path.

    Returns:
    - str: The calculated path, constructed from the block's parent pages.
    """
    # Ensure dynamic_parents exists and is a dictionary; otherwise, default to an empty dict
    dynamic_parents = getattr(block, "dynamic_parents", {})

    # Filter for parents that are of type 'child_page' and collect their block_ids
    page_parents = [
        value.block_id for key, value in dynamic_parents.items() if value.type == "child_page"
    ]

    # Construct the path from filtered parent pages
    path = "/".join(page_parents)

    return path


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


def parsing_block_return(block_id: str, md: str, item_type:str, path: str) -> dict:
    """Returns a dictionary with the block id and markdown content.

    Parameters:
    - block_id (str): The ID of the block.
    - md (str): The markdown content generated for the block.
    - path (str): The calculated path for the block.

    Returns:
    - dict: A dictionary containing the block ID and markdown content.
    """
    return {"id": block_id, "md": md, "type": item_type, "path": path}


##################################################
#                                                #
#                 MAIN PARSING                   #
#                                                #
##################################################


@validate_block(ParagraphBlock)
def parse_paragraph(block: ParagraphBlock) -> str:
    """Parses a paragraph block to Markdown, considering text styles."""
    # Initialize an empty list to hold Markdown-converted rich texts
    markdown_parts = []

    # Convert each rich text to Markdown and add it to the list
    for rich_text in block.paragraph.rich_text:
        markdown_parts.append(
            markdown_convert_paragraph_styles(rich_text.text["content"], rich_text.annotations)
        )

    # Join all parts into a single Markdown string
    markdown_paragraph = " ".join(markdown_parts)

    return parsing_block_return(block.id, markdown_paragraph, block.type, calculate_path_on_hierarchy(block))


@validate_block(Heading1Block)
def parse_heading_1(block: Heading1Block):
    # Assuming rich_text always has at least one item and you want to use the first one for the heading
    heading_text = block.heading_1.rich_text[0].plain_text if block.heading_1.rich_text else ""
    # We move heading_1 to heading_2 level in the markdown because the page title will be the heading_1
    return parsing_block_return(
        block.id, markdown_headings(heading_text, 2), block.type, calculate_path_on_hierarchy(block)
    )


@validate_block(Heading2Block)
def parse_heading_2(block: Heading2Block):
    # Extracting the heading text from the first item of rich_text, if available
    heading_text = block.heading_2.rich_text[0].plain_text if block.heading_2.rich_text else ""
    # Using the markdown_headings function to format as an H2 heading
    return parsing_block_return(
        block.id, markdown_headings(heading_text, 3), block.type, calculate_path_on_hierarchy(block)
    )


@validate_block(Heading3Block)
def parse_heading_3(block: Heading3Block):
    heading_text = block.heading_3.rich_text[0].plain_text if block.heading_3.rich_text else ""
    return parsing_block_return(
        block.id, markdown_headings(heading_text, 4), block.type, calculate_path_on_hierarchy(block)
    )


@validate_block(CodeBlock)
def parse_code(block: CodeBlock):
    md = markdown_code_block(
        code=block.code.rich_text[0].text["content"],
        caption=block.code.caption[0].text["content"],
        language=block.code.language,
    )
    return parsing_block_return(block.id, md, block.type, calculate_path_on_hierarchy(block))


@validate_block(QuoteBlock)
def parse_quote(block: Block) -> str:
    """Parses a quote block into a Markdown formatted note with a specific heading."""
    heading = "NOTE"

    # Initialize an empty string to build the note content
    note_content = ""

    # Iterate through each rich text segment in the quote
    for rich_text in block.quote.rich_text:
        # Append plain text to the note_content string
        note_content += markdown_convert_paragraph_styles(
            rich_text.plain_text, rich_text.annotations
        )

    # Use the markdown_note_with_heading helper to format the entire quote
    markdown_note = markdown_note_with_heading(note_content.strip(), heading)

    return parsing_block_return(block.id, markdown_note, block.type, calculate_path_on_hierarchy(block))


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
    path_hierarchy = calculate_path_on_hierarchy(block)
    page_processed_blocks.append(
        parsing_block_return(block.id, markdown_headings(block.child_page.title), block.type, path_hierarchy)
    )
    page_processed_blocks.append(parsing_block_return(block.id, changelog, block.type, path_hierarchy))
    return page_processed_blocks


@validate_block(LinkToPageBlock)
def parse_link_to_page(block: LinkToPageBlock):
    # TODO: Implement this function
    md = f"[Linked Page](https://www.notion.so/hell)"
    return parsing_block_return(block.id, md, block.type, calculate_path_on_hierarchy(block))
