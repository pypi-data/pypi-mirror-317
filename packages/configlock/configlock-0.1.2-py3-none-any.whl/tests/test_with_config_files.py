import os
import unittest
from tests.utils.generate_configs import generate_config_files
from cryptoconfig import EncryptedConfigManager

class TestMainEncryption(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment by generating config files.
        """
        generate_config_files()  # Generate the config files for testing
        self.manager = EncryptedConfigManager()  # Use a temporary key
        self.config_files = [
            "config.ini",
            "config.json",
            "config.yaml",
            "config.properties",
            "config.txt"
        ]

    def tearDown(self):
        """
        Clean up generated and encrypted files after tests.
        """
        for file in self.config_files:
            if os.path.exists(file):
                os.remove(file)

    def test_encryption_and_decryption(self):
        """
        Test that files are correctly encrypted and decrypted.
        """
        # Encrypt all files
        for file in self.config_files:
            if os.path.exists(file):
                try:
                    if file.endswith(".txt"):
                        # Handle plain text files
                        with open(file, "r", encoding="utf-8") as f:
                            content = f.read()
                        self.manager.save(file, content)  # Encrypt plain text file
                    else:
                        # Handle structured formats by parsing raw content
                        with open(file, "r", encoding="utf-8") as f:
                            raw_content = f.read()

                        if file.endswith(".ini"):
                            from cryptoconfig.formats.ini_handler import load
                            data = load(raw_content)
                        elif file.endswith(".json"):
                            import json
                            data = json.loads(raw_content)
                        elif file.endswith(".yaml"):
                            import yaml
                            data = yaml.safe_load(raw_content)
                        elif file.endswith(".properties"):
                            from cryptoconfig.formats.properties_handler import load
                            data = load(raw_content)

                        self.manager.save(file, data)
                except Exception as e:
                    self.fail(f"Encryption failed for {file}: {e}")

        # Decrypt and verify all files
        for file in self.config_files:
            if os.path.exists(file):
                try:
                    decrypted_data = self.manager.load(file)
                    print(f"Decrypted content of {file}: {decrypted_data}")
                except Exception as e:
                    self.fail(f"Decryption failed for {file}: {e}")


if __name__ == "__main__":
    unittest.main()
