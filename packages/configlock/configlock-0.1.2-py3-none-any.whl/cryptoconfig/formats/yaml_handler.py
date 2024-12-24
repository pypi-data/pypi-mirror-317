import yaml

def load(content):
    """
    Parses a YAML file from plaintext content.
    :param content: Plaintext content of the file.
    :return: Parsed YAML data.
    """
    return yaml.safe_load(content)

def dump(data):
    """
    Converts a dictionary to YAML format.
    :param data: Data to convert.
    :return: YAML format as a string.
    """
    return yaml.safe_dump(data)
