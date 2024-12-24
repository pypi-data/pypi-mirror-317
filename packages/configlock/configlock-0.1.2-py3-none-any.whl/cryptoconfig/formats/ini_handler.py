import configparser
from io import StringIO

def load(content):
    """
    Parses an INI file from plaintext content.
    :param content: Plaintext content of the file.
    :return: Parsed configuration as a dictionary.
    """
    parser = configparser.ConfigParser()
    parser.read_string(content)
    return {section: dict(parser.items(section)) for section in parser.sections()}

def dump(data):
    """
    Converts a dictionary to INI format.
    :param data: Configuration dictionary.
    :return: INI format as a string.
    """
    parser = configparser.ConfigParser()
    for section, values in data.items():
        parser[section] = values
    with StringIO() as stream:
        parser.write(stream)
        return stream.getvalue()
