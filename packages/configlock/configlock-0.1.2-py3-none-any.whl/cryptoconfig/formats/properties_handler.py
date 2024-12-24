def load(content):
    """
    Parses a .properties file from plaintext content.
    :param content: Plaintext content of the file.
    :return: Parsed properties as a dictionary.
    """
    data = {}
    for line in content.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data

def dump(data):
    """
    Converts a dictionary to .properties format.
    :param data: Configuration data.
    :return: Properties format as a string.
    """
    return "\n".join(f"{key}={value}" for key, value in data.items())
