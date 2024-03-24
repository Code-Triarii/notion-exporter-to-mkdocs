def notion_code_to_markdown(code_content: str, notion_language: str):
    """Convert a Notion code block to a Markdown code block. This function takes the content of a
    code block and its language as used in Notion, and returns the corresponding Markdown formatted
    code block with proper syntax highlighting. If the language is not recognized, it defaults to a
    generic code block without language-specific highlighting.

    Parameters:
    code_content (str): The content of the code block.
    notion_language (str): The programming language of the code block in Notion.

    Returns:
    str: The Markdown formatted code block.
    """
    # Mapping dictionary of Notion code languages to Markdown code identifiers
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
    }

    # Get the Markdown code identifier or default to no specific language
    markdown_language = language_mapping.get(notion_language, "")

    # Format the code block for Markdown
    markdown_code_block = f"```{markdown_language}\n{code_content}\n```"
    return markdown_code_block
