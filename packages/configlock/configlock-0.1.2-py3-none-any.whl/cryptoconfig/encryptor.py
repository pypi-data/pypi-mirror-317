import os
from cryptography.fernet import Fernet

class ConfigEncryptor:
    """
    Handles encryption and decryption of configuration files, with optional key persistence.
    """
    def __init__(self, key=None, key_file=None):
        """
        Initialize the encryptor with a key or key file.
        :param key: Encryption/decryption key (optional).
        :param key_file: Path to the key file (optional).
        """
        if key_file and os.path.exists(key_file):
            self.key = self._load_key(key_file)
        else:
            self.key = key or Fernet.generate_key()
            if key_file:
                self._save_key(key_file)
        self.fernet = Fernet(self.key)

    def _save_key(self, key_file):
        """
        Saves the key to a file.
        :param key_file: Path to save the key.
        """
        with open(key_file, "wb") as file:
            file.write(self.key)

    def _load_key(self, key_file):
        """
        Loads the key from a file.
        :param key_file: Path to the key file.
        :return: The loaded key.
        """
        with open(key_file, "rb") as file:
            return file.read()

    def encrypt(self, file_path, plaintext=None):
        """
        Encrypts a file or plaintext content.
        :param file_path: Path to the file to encrypt.
        :param plaintext: Optional plaintext content (string).
        """
        if plaintext is None:
            with open(file_path, "rb") as file:
                plaintext = file.read()
        # Ensure plaintext is bytes
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        encrypted_data = self.fernet.encrypt(plaintext)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)

    def decrypt(self, file_path):
        """
        Decrypts a file and returns the plaintext content.
        :param file_path: Path to the encrypted file.
        :return: Decrypted content as a string.
        """
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        return self.fernet.decrypt(encrypted_data).decode()
