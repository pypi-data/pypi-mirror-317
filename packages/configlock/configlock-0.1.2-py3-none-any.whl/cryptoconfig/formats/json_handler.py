import json

def load(content):
    """
    Parses a JSON file from plaintext content.
    :param content: Plaintext content of the file.
    :return: Parsed JSON data.
    """
    return json.loads(content)

def dump(data):
    """
    Converts a dictionary to JSON format.
    :param data: Data to convert.
    :return: JSON format as a string.
    """
    return json.dumps(data, indent=4)
