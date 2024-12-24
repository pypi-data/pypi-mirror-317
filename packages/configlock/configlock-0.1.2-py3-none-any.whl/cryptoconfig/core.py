import os
from .encryptor import ConfigEncryptor
from .formats import ini_handler, json_handler, yaml_handler, txt_handler, properties_handler

class EncryptedConfigManager:
    """
    Manages encrypted configuration files with support for multiple formats.
    """
    def __init__(self, key=None, key_file=None):
        """
        Initializes the configuration manager.
        :param key: Encryption/decryption key (optional).
        :param key_file: Path to the key file (optional).
        """
        self.encryptor = ConfigEncryptor(key, key_file)

    def _get_handler(self, file_path):
        """
        Determines the correct handler based on the file extension.
        :param file_path: Path to the file.
        :return: Corresponding handler module.
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".ini":
            return ini_handler
        elif ext == ".json":
            return json_handler
        elif ext in [".yml", ".yaml"]:
            return yaml_handler
        elif ext == ".txt":
            return txt_handler
        elif ext == ".properties":
            return properties_handler
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def load(self, file_path):
        """
        Loads a configuration file (decrypted).
        :param file_path: Path to the file.
        :return: Configuration data.
        """
        handler = self._get_handler(file_path)
        decrypted_content = self.encryptor.decrypt(file_path)
        return handler.load(decrypted_content)

    def save(self, file_path, data):
        """
        Saves a configuration file (encrypted).
        :param file_path: Path to the file.
        :param data: Configuration data to save.
        """
        handler = self._get_handler(file_path)
        plaintext = handler.dump(data)
        self.encryptor.encrypt(file_path, plaintext)
