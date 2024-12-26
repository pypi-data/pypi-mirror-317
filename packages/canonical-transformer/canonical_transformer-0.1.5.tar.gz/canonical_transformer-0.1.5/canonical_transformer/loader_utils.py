import json

def load_json_file(file_name):
    """
    Load a JSON file and return its contents as a Python object.

    Args:
        file_name (str): The path to the JSON file to be loaded.

    Returns:
        dict: The contents of the JSON file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
