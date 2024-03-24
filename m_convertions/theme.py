"""Defines the theme mapping for Notion to markdown"""

def notion_color_to_html(notion_color: str):
    """
    Convert a Notion color name to an HTML color code.

    This function takes a color name as used in Notion, and returns the corresponding HTML color code.
    If the color name is not recognized, it defaults to black.

    Parameters:
    notion_color (str): The name of the color in Notion.

    Returns:
    str: The HTML color code corresponding to the Notion color name.
    """
    # Mapping dictionary of Notion colors to HTML color codes
    color_mapping = {
        "default": "#000000",
        "gray": "#a8a8a8",
        "brown": "#a52a2a",
        "orange": "#ffa500",
        "yellow": "#ffff00",
        "green": "#008000",
        "blue": "#0000ff",
        "purple": "#800080",
        "pink": "#ffc0cb",
        "red": "#ff0000",
    }
    
    # Return the corresponding HTML color code or a default if not found
    return color_mapping.get(notion_color.lower(), "#000000")  # Default to black if the color is not found