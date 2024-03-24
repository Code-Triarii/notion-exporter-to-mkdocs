"""Helper functions for processing markdown content. Only those repeatedly used in the markdown processing functions are included here."""
from typing import List

def markdown_headings(title: str, level: int = 1) -> str:
    """
    Generates a markdown heading with the specified level.

    Parameters:
    - title (str): The title text of the heading.
    - level (int): The level of the heading (1 for largest, 6 for smallest). Defaults to 1.

    Returns:
    - str: The formatted markdown heading string.
    """
    # Ensure the heading level is within the markdown limit of 1-6
    if level < 1:
        level = 1
    elif level > 6:
        level = 6

    # Generate the heading with the appropriate number of hash marks
    heading = f"{'#' * level} {title}"

    return heading

def markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    """
    Generates a markdown table from headers and row values.

    Parameters:
    - headers (List[str]): A list of column headers.
    - rows (List[List[str]]): A list of rows, where each row is a list of values.

    Returns:
    - str: The markdown-formatted table as a string.
    """
    # Generate the header row
    header_row = "| " + " | ".join(headers) + " |"
    # Generate the separator row
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    # Generate each data row
    data_rows = ["| " + " | ".join(row) + " |" for row in rows]

    # Combine all parts and return
    return "\n".join([header_row, separator_row] + data_rows)

def markdown_code_block(code: str, caption: str = None, language: str = "") -> str:
    """
    Generates a markdown code block with optional language specification.

    Parameters:
    - code (str): The code content to include in the code block.
    - language (str): The language identifier for syntax highlighting. Defaults to an empty string.

    Returns:
    - str: The formatted markdown code block string.
    """
    language_mapping = {
        "JSON": "json",
        "CSS": "css",
        "Go": "go",
        "Python": "python",
        "YAML": "yaml",
        "PowerShell": "powershell",
        "JavaScript": "javascript",
        "HTML": "html",
        "Docker": "dockerfile",
        "bash": "bash",
    }

    # Get the Markdown code identifier or default to no specific language
    markdown_language = language_mapping.get(language, "")

    # Format the code block for Markdown
    markdown_code_block = f'```{markdown_language}\n{f"#{caption}" if caption else ""}{code}\n```'
    return markdown_code_block