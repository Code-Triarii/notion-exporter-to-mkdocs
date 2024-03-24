"""Auxiliar module to pretty print data structures."""

import json

def pretty_print(obj, label:str=None):
    """
    Pretty prints the input object. Supports dictionaries, valid JSON strings, lists of dictionaries, and other objects by converting them to strings.
    
    Parameters:
    - obj: The object to print. Can be a dict, a JSON string, a list of dicts, or any object.
    - label (optional): A label to print before the object. The label will be printed in yellow.
    """
    # Define ANSI color codes for yellow text and reset
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    
    # Print the label in yellow if provided
    if label:
        print(f"{YELLOW}{label}{RESET}\n")
    
    # Check the type of obj and handle accordingly
    if isinstance(obj, dict):
        # Object is a dictionary, convert to JSON string for pretty printing
        print(json.dumps(obj, indent=2))
    elif isinstance(obj, list) and all(isinstance(i, dict) for i in obj):
        # Object is a list of dictionaries, convert each dictionary to JSON string for pretty printing
        print(json.dumps(obj, indent=2))
    elif isinstance(obj, str):
        try:
            # Attempt to parse the string as JSON
            parsed_json = json.loads(obj)
            # If successful, pretty print the JSON string
            print(json.dumps(parsed_json, indent=2))
        except json.JSONDecodeError:
            # If the string is not valid JSON, print it directly
            print(obj)
    else:
        # For any other type, convert to string and print
        print(str(obj))